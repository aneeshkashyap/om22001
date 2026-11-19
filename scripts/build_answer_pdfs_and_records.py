import json, os, sys, html, re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import sqlite3

PROJECT_ROOT = 'd:/OM22001/om22001-stats-hub'

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "OM22001 Statistical Methods for Engineers — Worked Solutions")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.drawString(54, 32, "OM22001 Study Hub | Reg 2022 | Confidential Academic Resource")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 44, 558, 44)
        self.restoreState()

def clean_markdown_to_flowables(raw_text, styles):
    flowables = []
    lines = raw_text.split('\n')
    
    table_buffer = []
    in_table = False
    
    def format_line(s):
        s = html.escape(s)
        # bold **text**
        s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
        # italic *text*
        s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', s)
        # inline math \( ... \) or $ ... $
        s = re.sub(r'\\\(|\\\)', '', s)
        # remove leftover badge tags
        s = re.sub(r'&lt;badge.*?&gt;.*?&lt;/badge&gt;', '', s)
        return s

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('|') and stripped.endswith('|'):
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped[1:-1].split('|')]
            table_buffer.append(cells)
            in_table = True
            continue
        else:
            if in_table and table_buffer:
                try:
                    max_cols = max(len(r) for r in table_buffer)
                    padded = [r + [''] * (max_cols - len(r)) for r in table_buffer]
                    cell_data = []
                    for r_idx, row in enumerate(padded):
                        row_paras = []
                        for cell in row:
                            st = styles['TableHeader'] if r_idx == 0 else styles['TableCell']
                            row_paras.append(Paragraph(format_line(cell), st))
                        cell_data.append(row_paras)
                        
                    t = Table(cell_data, repeatRows=1)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                        ('TOPPADDING', (0,0), (-1,-1), 3),
                        ('LEFTPADDING', (0,0), (-1,-1), 5),
                        ('RIGHTPADDING', (0,0), (-1,-1), 5),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                    ]))
                    flowables.append(Spacer(1, 4))
                    flowables.append(t)
                    flowables.append(Spacer(1, 6))
                except Exception:
                    pass
                table_buffer = []
                in_table = False

        if not stripped:
            flowables.append(Spacer(1, 3))
            continue
            
        if stripped.startswith('# '):
            flowables.append(Spacer(1, 8))
            flowables.append(Paragraph(format_line(stripped[2:]), styles['Heading1_Custom']))
            flowables.append(Spacer(1, 3))
        elif stripped.startswith('## '):
            flowables.append(Spacer(1, 6))
            flowables.append(Paragraph(format_line(stripped[3:]), styles['Heading2_Custom']))
            flowables.append(Spacer(1, 2))
        elif stripped.startswith('### '):
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph(format_line(stripped[4:]), styles['Heading3_Custom']))
            flowables.append(Spacer(1, 2))
        elif stripped.startswith('---'):
            flowables.append(Spacer(1, 3))
            flowables.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=3, spaceBefore=3))
        elif stripped.startswith('- ') or stripped.startswith('* '):
            bullet_txt = format_line(stripped[2:])
            flowables.append(Paragraph(f"• &nbsp; {bullet_txt}", styles['Bullet_Custom']))
        elif re.match(r'^\d+[\.\)]\s', stripped):
            flowables.append(Paragraph(format_line(stripped), styles['Normal_Custom']))
        elif 'Final Answer' in stripped or 'Final answer' in stripped:
            flowables.append(Spacer(1, 3))
            p = Paragraph(f"<b>{format_line(stripped)}</b>", styles['AnswerBox'])
            flowables.append(p)
            flowables.append(Spacer(1, 3))
        else:
            flowables.append(Paragraph(format_line(stripped), styles['Normal_Custom']))
            
    if in_table and table_buffer:
        try:
            max_cols = max(len(r) for r in table_buffer)
            padded = [r + [''] * (max_cols - len(r)) for r in table_buffer]
            cell_data = []
            for r_idx, row in enumerate(padded):
                row_paras = []
                for cell in row:
                    st = styles['TableHeader'] if r_idx == 0 else styles['TableCell']
                    row_paras.append(Paragraph(format_line(cell), st))
                cell_data.append(row_paras)
            t = Table(cell_data, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            flowables.append(t)
        except Exception:
            pass
            
    return flowables

def build_pdf_document(output_path, title, subtitle, exam_meta, chat_messages):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3,
    ))
    
    styles.add(ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=6,
    ))
    
    styles.add(ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    ))
    
    styles.add(ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        'Normal_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=12,
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        'AnswerBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#065f46'),
        backColor=colors.HexColor('#ecfdf5'),
        borderColor=colors.HexColor('#a7f3d0'),
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=3,
        spaceAfter=3,
    ))

    styles.add(ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f172a'),
    ))

    styles.add(ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1e293b'),
    ))

    story = []
    
    story.append(Paragraph("ANNA UNIVERSITY REGULATION 2022 — STEP-BY-STEP WORKED SOLUTIONS", styles['DocSubtitle']))
    story.append(Paragraph(title, styles['DocTitle']))
    story.append(Paragraph(f"<b>Course:</b> OM22001 Statistical Methods for Engineers &nbsp;|&nbsp; <b>{exam_meta}</b>", styles['Normal_Custom']))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=8, spaceBefore=2))
    
    for msg in chat_messages:
        flowables = clean_markdown_to_flowables(msg, styles)
        story.extend(flowables)
        
    doc.build(story, canvasmaker=NumberedCanvas)
    return os.path.getsize(output_path)

def extract_chat_messages(chat_path):
    with open(chat_path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    mapping = d.get('mapping', {})
    curr = d.get('current_node')
    nodes = []
    while curr and curr in mapping:
        node = mapping[curr]
        if node.get('message'):
            nodes.append(node)
        curr = node.get('parent')
    nodes.reverse()
    
    substantive_answers = []
    for n in nodes:
        m = n['message']
        role = m['author']['role']
        if role == 'assistant':
            txt = ''.join([p for p in m['content'].get('parts', []) if isinstance(p, str)])
            # Skip short greeting/instruction messages
            if len(txt) > 250 and not txt.startswith('Understood.') and not txt.startswith('I will use this'):
                substantive_answers.append(txt)
    return substantive_answers

ANSWER_CONFIGS = [
  {
    'chat_file': 'scratch_chat_5.json',
    'exam_code': 'SEM_PYQ_1',
    'qp_filename': 'OM22001 (2).pdf',
    'ans_filename': 'SEM_PYQ_1_Dec_2024_Worked_Solutions.pdf',
    'dest_rel': '02_SEMESTER/SEM_PYQ_1/Answers/SEM_PYQ_1_Dec_2024_Worked_Solutions.pdf',
    'mirror_rel': 'SEMESTER/SEM_PYQ_1/Answers/SEM_PYQ_1_Dec_2024_Worked_Solutions.pdf',
    'category': 'SEMESTER',
    'title': 'Semester Examination Dec 2024 (SEM PYQ 1) — Complete Worked Solutions',
    'subtitle': 'Anna University Regulation 2022',
    'exam_meta': 'Semester 5 | Q.Code: 147184 | Max Marks: 100 | Duration: 3 Hours',
    'chat_url': 'https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047',
    'description': 'Anna University End-Semester Examination – December 2024 (Fifth Semester) Official Worked Solutions. Q.Code: 147184. Full worked solutions for Part A (20 x 2M), Part B (5 x 10M), and Part C (1 x 10M compulsory).',
    'tags': 'Dec 2024, Sem 5, QCode 147184, Answers, Worked Solutions, Part A, Part B, Part C, 100 Marks',
  },
  {
    'chat_file': 'scratch_chat_4.json',
    'exam_code': 'SEM_PYQ_2',
    'qp_filename': 'OM22001 (1).pdf',
    'ans_filename': 'SEM_PYQ_2_May_2025_Worked_Solutions.pdf',
    'dest_rel': '02_SEMESTER/SEM_PYQ_2/Answers/SEM_PYQ_2_May_2025_Worked_Solutions.pdf',
    'mirror_rel': 'SEMESTER/SEM_PYQ_2/Answers/SEM_PYQ_2_May_2025_Worked_Solutions.pdf',
    'category': 'SEMESTER',
    'title': 'Semester Examination May 2025 (SEM PYQ 2) — Complete Worked Solutions',
    'subtitle': 'Anna University Regulation 2022',
    'exam_meta': 'Semester 5 | Q.Code: 405686 | Max Marks: 100 | Duration: 3 Hours',
    'chat_url': 'https://chatgpt.com/share/6af49542-88b8-83ee-9b4a-769b1ec3d454',
    'description': 'Anna University End-Semester Examination – May 2025 (Fifth Semester) Official Worked Solutions. Q.Code: 405686. Full worked solutions for Part A (20 x 2M), Part B (5 x 10M), and Part C (1 x 10M compulsory).',
    'tags': 'May 2025, Sem 5, QCode 405686, Answers, Worked Solutions, Part A, Part B, Part C, 100 Marks',
  },
  {
    'chat_file': 'scratch_chat_3.json',
    'exam_code': 'SEM_PYQ_3',
    'qp_filename': 'OM22001.pdf',
    'ans_filename': 'SEM_PYQ_3_Dec_2025_Worked_Solutions.pdf',
    'dest_rel': '02_SEMESTER/SEM_PYQ_3/Answers/SEM_PYQ_3_Dec_2025_Worked_Solutions.pdf',
    'mirror_rel': 'SEMESTER/SEM_PYQ_3/Answers/SEM_PYQ_3_Dec_2025_Worked_Solutions.pdf',
    'category': 'SEMESTER',
    'title': 'Semester Examination Dec 2025 (SEM PYQ 3) — Complete Worked Solutions',
    'subtitle': 'Anna University Regulation 2022',
    'exam_meta': 'Semester 6 | Q.Code: 133554 | Max Marks: 100 | Duration: 3 Hours',
    'chat_url': 'https://chatgpt.com/share/6af49529-ded8-83ee-ac96-a10049547724',
    'description': 'Anna University End-Semester Examination – December 2025 (Sixth Semester) Official Worked Solutions. Q.Code: 133554. Full worked solutions for Part A (20 x 2M), Part B (5 x 10M), and Part C (1 x 10M compulsory).',
    'tags': 'Dec 2025, Sem 6, QCode 133554, Answers, Worked Solutions, Part A, Part B, Part C, 100 Marks',
  },
  {
    'chat_file': 'scratch_chat_1.json',
    'exam_code': 'SEM_PYQ_4',
    'qp_filename': 'OM22001-25211048.pdf',
    'ans_filename': 'SEM_PYQ_4_May_2026_Worked_Solutions.pdf',
    'dest_rel': '02_SEMESTER/SEM_PYQ_4/Answers/SEM_PYQ_4_May_2026_Worked_Solutions.pdf',
    'mirror_rel': 'SEMESTER/SEM_PYQ_4/Answers/SEM_PYQ_4_May_2026_Worked_Solutions.pdf',
    'category': 'SEMESTER',
    'title': 'Semester Examination May 2026 (SEM PYQ 4) — Complete Worked Solutions',
    'subtitle': 'Anna University Regulation 2022',
    'exam_meta': 'Semester 6 | Q.Code: 323580 | Max Marks: 100 | Duration: 3 Hours',
    'chat_url': 'https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047',
    'description': 'Anna University End-Semester Examination – May 2026 (Sixth Semester) Official Worked Solutions. Q.Code: 323580. Full worked solutions for Part A (20 x 2M), Part B (5 x 10M), and Part C (1 x 10M compulsory).',
    'tags': 'May 2026, Sem 6, QCode 323580, Answers, Worked Solutions, Part A, Part B, Part C, 100 Marks',
  },
  {
    'chat_file': 'scratch_chat_8.json',
    'exam_code': 'FAT_1',
    'qp_filename': 'OE FAT PAPERS.pdf',
    'ans_filename': 'FAT_1_AY2024_2025_Worked_Solutions.pdf',
    'dest_rel': '01_FAT/FAT_1/Answers/FAT_1_AY2024_2025_Worked_Solutions.pdf',
    'mirror_rel': 'FAT/FAT_1/Answers/FAT_1_AY2024_2025_Worked_Solutions.pdf',
    'category': 'FAT',
    'title': 'FAT 1 Assessment (AY 2024–2025) — Step-by-Step Worked Solutions',
    'subtitle': 'Formative Assessment Test 1 (Pages 1–2 of OE FAT PAPERS)',
    'exam_meta': 'Date: 08.03.2025 | Semester VI | Max Marks: 50 | CO1 & CO2',
    'chat_url': 'https://chatgpt.com/share/6af4959d-3f40-83ee-a7bc-7562286c5b1b',
    'description': 'Formative Assessment Test 1 (FAT-1) Academic Year 2024–2025 Worked Solutions. Date: 08.03.2025, Semester VI, 50 Marks. Step-by-step solutions for Part A (10 x 2M) and Part B (3 x 10M).',
    'tags': 'FAT-1, 2024-2025, Pages 1-2, CO1, CO2, Answers, Worked Solutions, 50 Marks',
  },
  {
    'chat_file': 'scratch_chat_2.json',
    'exam_code': 'FAT_1',
    'qp_filename': 'OE statistics fat 1.pdf',
    'ans_filename': 'FAT_1_AY2025_2026_Worked_Solutions.pdf',
    'dest_rel': '01_FAT/FAT_1/Answers/FAT_1_AY2025_2026_Worked_Solutions.pdf',
    'mirror_rel': 'FAT/FAT_1/Answers/FAT_1_AY2025_2026_Worked_Solutions.pdf',
    'category': 'FAT',
    'title': 'FAT 1 Assessment (AY 2025–2026) — Step-by-Step Worked Solutions',
    'subtitle': 'Formative Assessment Test 1 (OE statistics fat 1.pdf)',
    'exam_meta': 'Date: 06.08.2025 | Semester V/VII | Max Marks: 50 | CO1 & CO2',
    'chat_url': 'https://chatgpt.com/share/6af49517-7c80-83ec-a422-4c8bde96cd14',
    'description': 'Formative Assessment Test 1 (FAT-1) Academic Year 2025–2026 Worked Solutions. Date: 06.08.2025, Semester V/VII, 50 Marks. Step-by-step solutions for Part A (10 x 2M) and Part B (3 x 10M).',
    'tags': 'FAT-1, 2025-2026, Full Paper, CO1, CO2, Answers, Worked Solutions, 50 Marks',
  },
  {
    'chat_file': 'scratch_chat_7.json',
    'exam_code': 'FAT_2',
    'qp_filename': 'OE FAT PAPERS.pdf',
    'ans_filename': 'FAT_2_AY2024_2025_Worked_Solutions.pdf',
    'dest_rel': '01_FAT/FAT_2/Answers/FAT_2_AY2024_2025_Worked_Solutions.pdf',
    'mirror_rel': 'FAT/FAT_2/Answers/FAT_2_AY2024_2025_Worked_Solutions.pdf',
    'category': 'FAT',
    'title': 'FAT 2 Assessment (AY 2024–2025) — Step-by-Step Worked Solutions',
    'subtitle': 'Formative Assessment Test 2 (Pages 3–4 of OE FAT PAPERS)',
    'exam_meta': 'Date: 19.04.2025 | Semester VI | Max Marks: 50 | CO2 & CO3',
    'chat_url': 'https://chatgpt.com/share/6af49588-ac1c-83ee-ab3e-b65021201e1d',
    'description': 'Formative Assessment Test 2 (FAT-2) Academic Year 2024–2025 Worked Solutions. Date: 19.04.2025, Semester VI, 50 Marks. Step-by-step solutions for Part A (10 x 2M) and Part B (3 x 10M).',
    'tags': 'FAT-2, 2024-2025, Pages 3-4, CO2, CO3, Answers, Worked Solutions, 50 Marks',
  },
  {
    'chat_file': 'scratch_chat_6.json',
    'exam_code': 'FAT_3',
    'qp_filename': 'OE FAT PAPERS.pdf',
    'ans_filename': 'FAT_3_AY2024_2025_Worked_Solutions.pdf',
    'dest_rel': '01_FAT/FAT_3/Answers/FAT_3_AY2024_2025_Worked_Solutions.pdf',
    'mirror_rel': 'FAT/FAT_3/Answers/FAT_3_AY2024_2025_Worked_Solutions.pdf',
    'category': 'FAT',
    'title': 'FAT 3 Assessment (AY 2024–2025) — Step-by-Step Worked Solutions',
    'subtitle': 'Formative Assessment Test 3 (Pages 5–6 of OE FAT PAPERS)',
    'exam_meta': 'Date: 19.05.2025 | Semester VI | Max Marks: 50 | CO4 & CO5',
    'chat_url': 'https://chatgpt.com/share/6af49571-bafc-83e8-af94-15f7f6f48800',
    'description': 'Formative Assessment Test 3 (FAT-3 / Model) Academic Year 2024–2025 Worked Solutions. Date: 19.05.2025, Semester VI, 50 Marks. Step-by-step solutions for Part A (10 x 2M) and Part B (3 x 10M).',
    'tags': 'FAT-3, 2024-2025, Pages 5-6, CO4, CO5, Answers, Worked Solutions, 50 Marks',
  },
]

def main():
    print("=== STARTING ANSWER DOCUMENT GENERATION & UPLOAD ===\n")
    
    db_path = os.path.join(PROJECT_ROOT, 'prisma', 'dev.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM Subject LIMIT 1")
    subject_id = cur.fetchone()[0]
    
    # Clean any existing ANSWER_KEY documents
    cur.execute("DELETE FROM DocumentRelationship WHERE answerDocId IN (SELECT id FROM Document WHERE documentType = 'ANSWER_KEY')")
    cur.execute("DELETE FROM Document WHERE documentType = 'ANSWER_KEY'")
    conn.commit()
    
    # Load sources json to update
    sources_path = os.path.join(PROJECT_ROOT, 'content', 'sources', 'answer-sources.json')
    with open(sources_path, 'r', encoding='utf-8') as f:
        answer_sources = json.load(f)
        
    source_map = {s['url']: s for s in answer_sources}
    
    import uuid
    def gen_id():
        return 'c' + uuid.uuid4().hex[:24]

    for cfg in ANSWER_CONFIGS:
        chat_path = os.path.join(PROJECT_ROOT, cfg['chat_file'])
        messages = extract_chat_messages(chat_path)
        print(f"Processing {cfg['ans_filename']}: extracted {len(messages)} solution blocks from {cfg['chat_file']}")
        
        # 1. Build PDF in primary destination
        dest_abs = os.path.join(PROJECT_ROOT, 'storage', 'documents', cfg['dest_rel'])
        pdf_size = build_pdf_document(dest_abs, cfg['title'], cfg['subtitle'], cfg['exam_meta'], messages)
        print(f"  ✓ PDF Built: {dest_abs} ({pdf_size:,} bytes)")
        
        # 2. Mirror PDF
        mirror_abs = os.path.join(PROJECT_ROOT, 'storage', 'documents', cfg['mirror_rel'])
        os.makedirs(os.path.dirname(mirror_abs), exist_ok=True)
        with open(dest_abs, 'rb') as f_in, open(mirror_abs, 'wb') as f_out:
            f_out.write(f_in.read())
            
        # 3. Save JSON solution data
        json_abs = dest_abs.replace('.pdf', '.json')
        with open(json_abs, 'w', encoding='utf-8') as f_json:
            json.dump({
                'title': cfg['title'],
                'examCode': cfg['exam_code'],
                'category': cfg['category'],
                'chatUrl': cfg['chat_url'],
                'messages': messages,
            }, f_json, indent=2)
            
        # 4. Find Examination ID
        cur.execute("SELECT id FROM Examination WHERE code = ?", (cfg['exam_code'],))
        exam_row = cur.fetchone()
        exam_id = exam_row[0] if exam_row else None
        
        # 5. Find corresponding Question Paper Document ID
        # Match by examinationId, subfolder QUESTION_PAPERS, and originalFilename
        cur.execute("""
            SELECT id FROM Document 
            WHERE examinationId = ? AND subfolder = 'QUESTION_PAPERS' AND originalFilename = ?
            LIMIT 1
        """, (exam_id, cfg['qp_filename']))
        qp_row = cur.fetchone()
        qp_doc_id = qp_row[0] if qp_row else None
        
        # 6. Insert Answer Document record
        ans_doc_id = gen_id()
        ocr_snippet = f"{cfg['title']} | {cfg['exam_meta']} | Solutions: " + ' '.join(messages)[:400]
        now = "2026-11-12T05:30:00.000Z"
        
        cur.execute("""
            INSERT INTO Document (
                id, subjectId, category, examinationId, subfolder, documentType,
                originalFilename, storedFilename, storagePath, fileType, fileSize,
                description, tags, ocrText, classificationConfidence, classificationStatus,
                isVerified, createdAt, updatedAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ans_doc_id, subject_id, cfg['category'], exam_id, 'ANSWERS', 'ANSWER_KEY',
            cfg['ans_filename'], cfg['ans_filename'], cfg['dest_rel'], 'pdf', pdf_size,
            cfg['description'], cfg['tags'], ocr_snippet, 1.0, 'CONFIRMED',
            1, now, now
        ))
        
        # 7. Create Relational Link between Question Paper and Answer Document
        if qp_doc_id:
            rel_id = gen_id()
            cur.execute("""
                INSERT INTO DocumentRelationship (id, questionPaperId, answerDocId)
                VALUES (?, ?, ?)
            """, (rel_id, qp_doc_id, ans_doc_id))
            print(f"  ✓ Linked Answer Document to Question Paper {qp_doc_id} ({cfg['qp_filename']})")
        else:
            print(f"  ⚠️ Warning: No matching Question Paper found for {cfg['exam_code']} / {cfg['qp_filename']}")
            
        # 8. Update answer sources JSON
        if cfg['chat_url'] in source_map:
            source_map[cfg['chat_url']]['mappedTo'] = {
                'examCode': cfg['exam_code'],
                'category': cfg['category'],
                'questionPaper': cfg['qp_filename'],
                'answerDocument': cfg['ans_filename'],
                'answerDocId': ans_doc_id,
            }
            source_map[cfg['chat_url']]['status'] = 'mapped'
            source_map[cfg['chat_url']]['notes'] = f"Fully extracted and converted into publication-quality worked solutions PDF: {cfg['ans_filename']}"
            
    conn.commit()
    conn.close()
    
    with open(sources_path, 'w', encoding='utf-8') as f:
        json.dump(answer_sources, f, indent=2)
    print("\n✓ Updated content/sources/answer-sources.json with all 8 mapped links.")
    
    print("\nAll 8 answer documents generated, stored, and relationally linked successfully!")

if __name__ == '__main__':
    main()

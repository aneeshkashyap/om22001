================================================================================
OM22001 - STATISTICAL METHODS FOR ENGINEERS
Academic Repository & Study Materials Hub (Anna University Reg 2022)
================================================================================

1. SYSTEM OVERVIEW & ARCHITECTURE
--------------------------------------------------------------------------------
This website is a simple, clean, responsive academic repository built specifically
for OM22001 – Statistical Methods for Engineers (Anna University Regulation 2022).

It is organized into four distinct, isolated sections:
1. FAT Question Papers & Answers (/fat)
2. Semester Question Papers & Answers (/semester)
3. Study Materials (/study-materials)
4. Formula Sheets (/formulas)

Plus:
- Top horizontal navigation bar (TopNavbar with Home, FAT Papers, Semester Papers, Study Materials) replacing the sidebar
- Clean minimal home page (/)
- All Documents repository (/documents)
- Document upload, preview, download, rename, and deletion operations


2. PHYSICAL & RELATIONAL FOLDER HIERARCHY
--------------------------------------------------------------------------------
om22001-stats-hub/
  storage/
    documents/
      01_FAT/
        FAT_1/
          Question_Papers/  (OE statistics fat 1 (2024-2025).pdf, OE statistics fat 1.pdf)
          Answers/          (Answers hosted on ChatGPT)
        FAT_2/
          Question_Papers/  (OE statistics fat 2.pdf - AY 2024-2025, Date: 19.04.2025)
          Answers/          (Answers hosted on ChatGPT)
        FAT_3/
          Question_Papers/  (OE statistics fat 3.pdf - AY 2024-2025, Date: 19.05.2025)
          Answers/          (Answers hosted on ChatGPT)
      02_SEMESTER/
        SEM_PYQ_1/
          Question_Papers/  (OM22001 (2).pdf - Dec 2024, Sem 5, QCode 147184)
          Answers/          (Answers hosted on ChatGPT)
        SEM_PYQ_2/
          Question_Papers/  (OM22001 (1).pdf - May 2025, Sem 5, QCode 405686)
          Answers/          (Answers hosted on ChatGPT)
        SEM_PYQ_3/
          Question_Papers/  (OM22001.pdf - Dec 2025, Sem 6, QCode 133554)
          Answers/          (Answers hosted on ChatGPT)
        SEM_PYQ_4/
          Question_Papers/  (OM22001-25211048.pdf - May 2026, Sem 6, QCode 323580)
          Answers/          (Answers hosted on ChatGPT)
        SEM_PYQ_5/ ... (Dynamically created via "Add New PYQ")
      STUDY_MATERIALS/
        Complete_Notes/
        Unit_1_Descriptive_Statistics/
          (OM22001_Unit_1_Descriptive_Statistics_Complete_Notes.pdf - 32 Pages Handwritten Notes)
        Unit_2_Large_Sample_Tests/
          (OM22001_Unit_2_Large_Sample_Tests_Complete_Notes.pdf - 14 Pages Handwritten Notes)
        Unit_3_Small_Sample_Tests/
          (OM22001_Unit_3_Small_Sample_Tests_Complete_Notes.pdf - 18 Pages Handwritten Notes)
        Unit_4_Design_of_Experiments/
        Unit_5_Statistical_Quality_Control/
      FORMULA_SHEETS/
        Unit_1_Descriptive_Statistics/
        Unit_2_Testing_of_Hypothesis_Large_Samples/
        Unit_3_Testing_of_Hypotheses_Small_Samples/
        Unit_4_Analysis_of_Variance/
        Unit_5_Statistical_Quality_Control/
  content/
    materials/
      formula-sheets.json   (Unit 1 to 5 verified formulas with LaTeX math)
    sem/                    (Semester question papers and worked answers)
    fat/                    (FAT 1, 2, 3 question papers and worked answers)


3. SECTION-BY-SECTION CAPABILITIES
--------------------------------------------------------------------------------

A. FAT Question Papers & Answers (/fat):
   - Clean folder navigation tabs for FAT 1, FAT 2, and FAT 3.
   - Question Papers and Answers kept strictly separate.
   - Bulky cards, unit syllabus subheadings, and extraneous 2-mark/10-mark tabs removed.
   - Question Papers view with PDF Preview, Download, and direct ChatGPT Answer button (clean view without 'Answers not uploaded' warning notices).
   - Answers folder directly opens the corresponding solved ChatGPT thread.
   - Displays original filename, file size, and upload date.
   - File renaming and deletion with confirmation prompt.

B. Semester Question Papers & Answers (/semester):
   - Clean examination selector strictly containing the 4 actual semester exams:
     SEM PYQ 1 (Dec 2024), SEM PYQ 2 (May 2025), SEM PYQ 3 (Dec 2025), and SEM PYQ 4 (May 2026).
   - Removed test entry SEM PYQ 5.
   - Separate subfolders for Question Papers and Answers.
   - Direct "Answers on ChatGPT" buttons for each semester session.
   - File renaming and deletion with confirmation prompt.

C. Study Materials (/study-materials):
   - Six dedicated unit folders:
     1. Complete Subject Notes
     2. Unit 1 – Descriptive Statistics (Includes complete 32-page handwritten class notes PDF covering Central Tendency, Dispersion, Moments, Skewness, Kurtosis, and university solved problems)
     3. Unit 2 – Testing of Hypothesis (Large Samples) (Includes complete 14-page handwritten class notes PDF covering Z-tests for Single Mean, Difference of Means, Proportions, Standard Error, and university solved problems)
     4. Unit 3 – Testing of Hypotheses (Small Samples) (Includes complete 18-page handwritten class notes PDF covering Student's t-test, Paired t-test, F-test, Chi-square Goodness of Fit, Independence of Attributes, Contingency Tables, and university solved problems)
     5. Unit 4 – Analysis of Variance
     6. Unit 5 – Statistical Quality Control
   - Supports upload of PDF, DOC, DOCX, and image formats.
   - File preview, download, rename, and deletion.

D. Formula Sheets (/formulas):
   - Dedicated Formula Sheets section with 5 separate unit cards:
     * Unit 1 – Descriptive Statistics
     * Unit 2 – Testing of Hypothesis (Large Samples)
     * Unit 3 – Testing of Hypotheses (Small Samples)
     * Unit 4 – Analysis of Variance
     * Unit 5 – Statistical Quality Control
   - Separate formula sheet for every unit.
   - View mode: Clear KaTeX mathematical rendering supporting Greek letters,
     equations, subscripts, superscripts, fractions, and matrices.
   - Edit mode: Interactive editor allows adding, modifying, or removing formulas
     directly on the website with live LaTeX rendering preview, saved to storage.
   - Upload PDF option: Upload unit-specific formula sheets as PDFs.
   - Print / Download PDF: Formatted layout for clean printing or PDF saving.

E. Simple Home Page (/):
   - Clean academic header: OM22001 - STATISTICAL METHODS FOR ENGINEERS
   - Direct cards for FAT Papers & Semester Papers.
   - Quick action buttons: "Preview QP" (inline modal preview) and green "Answers on ChatGPT" buttons linking directly to the solved answer threads.

F. Direct ChatGPT Solved Answers Integration:
   Every question paper is linked to its exact solved answers ChatGPT thread:
   1. SEM PYQ 1 (Dec 2024, Q.Code: 147184) -> https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047
   2. SEM PYQ 2 (May 2025, Q.Code: 405686) -> https://chatgpt.com/share/6af49529-ded8-83ee-ac96-a10049547724
   3. SEM PYQ 3 (Dec 2025, Q.Code: 133554) -> https://chatgpt.com/share/6af49542-88b8-83ee-9b4a-769b1ec3d454
   4. SEM PYQ 4 (May 2026, Q.Code: 323580) -> https://chatgpt.com/share/6af4955a-b0f0-83ec-bfa4-a3257b13a4de
   5. FAT 1 (AY 2024-2025, OE statistics fat 1 (2024–2025).pdf) -> https://chatgpt.com/share/6af4959d-3f40-83ee-a7bc-7562286c5b1b
   6. FAT 1 (AY 2025-2026, OE statistics fat 1) -> https://chatgpt.com/share/6af49517-7c80-83ec-a422-4c8bde96cd14
   7. FAT 2 (AY 2024-2025, OE statistics fat 2.pdf) -> https://chatgpt.com/share/6af49588-ac1c-83ee-ab3e-b65021201e1d
   8. FAT 3 (AY 2024-2025, OE statistics fat 3.pdf) -> https://chatgpt.com/share/6af49571-bafc-83e8-af94-15f7f6f48800

G. KaTeX Mathematical Formula Parsing:
   - Fixed math parser in MathView component to handle punctuation attached to delimiters (e.g. "$.", "$,", "$:").
   - Strips delimiting $ signs before passing formulas to KaTeX, preventing "Can't use function '$' in math mode" parse error (#cc0000 red text).
   - Added global fallback style ensuring math errors never display in red text.

   - Simple search bar for fast lookup.
   - List of recently uploaded files with instant Preview and Download.

F. Integrated Document Viewer:
   - Opens PDFs and images inside the website.
   - "Back" button to return to the active section.
   - Zoom controls: Zoom In (+), Zoom Out (-), Reset (100%).
   - Page navigation and search controls.
   - Direct download button.
   - Q&A association panel: Shows linked worked answers for question papers.


4. API ENDPOINTS
--------------------------------------------------------------------------------
- GET  /api/examinations        : List all examinations (FAT & Semester)
- POST /api/examinations        : Create a new examination folder (e.g. SEM PYQ 5)
- GET  /api/formulas            : Get formula sheets and uploaded PDFs for Units 1-5
- POST /api/formulas            : Save edited formula sheets for any unit
- GET  /api/documents           : Search and filter documents
- GET  /api/documents/[id]      : Retrieve document details and Q&A relationships
- PATCH /api/documents/[id]     : Rename document (originalFilename)
- DELETE /api/documents/[id]    : Delete document from database and disk
- GET  /api/documents/[id]/preview  : Stream document for inline preview
- GET  /api/documents/[id]/download : Download original document file
- POST /api/upload              : Stage uploaded files and classify
- POST /api/documents/confirm   : Save staged file to organized folder & database


5. RUNNING LOCALLY
--------------------------------------------------------------------------------
1. Start development server:
   npm.cmd run dev

2. Open in your browser:
   http://localhost:3000

3. Production build & start:
   npm.cmd run build
   npm.cmd run start
================================================================================

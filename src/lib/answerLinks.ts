/**
 * Direct ChatGPT Solved Answers Mapping for OM22001 Examination Papers
 */

export interface ChatGptLinkInfo {
  examCode: string;
  examTitle: string;
  questionPaperName: string;
  chatGptUrl: string;
}

export const CHATGPT_ANSWER_LINKS: Record<string, ChatGptLinkInfo> = {
  // Semester Question Papers
  SEM_PYQ_1: {
    examCode: "SEM_PYQ_1",
    examTitle: "Semester Examination – Dec 2024 (Sem 5, Q.Code: 147184)",
    questionPaperName: "OM22001 (2).pdf",
    chatGptUrl: "https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047",
  },
  SEM_PYQ_2: {
    examCode: "SEM_PYQ_2",
    examTitle: "Semester Examination – May 2025 (Sem 5, Q.Code: 405686)",
    questionPaperName: "OM22001 (1).pdf",
    chatGptUrl: "https://chatgpt.com/share/6af49529-ded8-83ee-ac96-a10049547724",
  },
  SEM_PYQ_3: {
    examCode: "SEM_PYQ_3",
    examTitle: "Semester Examination – Dec 2025 (Sem 6, Q.Code: 133554)",
    questionPaperName: "OM22001.pdf",
    chatGptUrl: "https://chatgpt.com/share/6af49542-88b8-83ee-9b4a-769b1ec3d454",
  },
  SEM_PYQ_4: {
    examCode: "SEM_PYQ_4",
    examTitle: "Semester Examination – May 2026 (Sem 6, Q.Code: 323580)",
    questionPaperName: "OM22001-25211048.pdf",
    chatGptUrl: "https://chatgpt.com/share/6af4955a-b0f0-83ec-bfa4-a3257b13a4de",
  },

  // FAT Examination Papers
  FAT_1_AY2025_2026: {
    examCode: "FAT_1",
    examTitle: "FAT 1 (Academic Year 2025–2026, 06.08.2025, Sem 5)",
    questionPaperName: "OE statistics fat 1.pdf",
    chatGptUrl: "https://chatgpt.com/share/6af49517-7c80-83ec-a422-4c8bde96cd14",
  },
  FAT_1_AY2024_2025: {
    examCode: "FAT_1",
    examTitle: "FAT 1 (Academic Year 2024–2025, 08.03.2025, Sem 6)",
    questionPaperName: "OE statistics fat 1 (2024-2025).pdf",
    chatGptUrl: "https://chatgpt.com/share/6af4959d-3f40-83ee-a7bc-7562286c5b1b",
  },
  FAT_2_AY2024_2025: {
    examCode: "FAT_2",
    examTitle: "FAT 2 (Academic Year 2024–2025, 19.04.2025, Sem 6)",
    questionPaperName: "OE statistics fat 2.pdf",
    chatGptUrl: "https://chatgpt.com/share/6af49588-ac1c-83ee-ab3e-b65021201e1d",
  },
  FAT_3_AY2024_2025: {
    examCode: "FAT_3",
    examTitle: "FAT 3 (Academic Year 2024–2025, 19.05.2025, Sem 6)",
    questionPaperName: "OE statistics fat 3.pdf",
    chatGptUrl: "https://chatgpt.com/share/6af49571-bafc-83e8-af94-15f7f6f48800",
  },
};

export function getChatGptAnswerUrl(doc: {
  originalFilename?: string;
  storagePath?: string;
  examination?: { code?: string } | null;
  subfolder?: string;
}): string | null {
  const filename = doc.originalFilename || "";
  const examCode = doc.examination?.code || "";

  // Semester check by exam code or filename
  if (examCode === "SEM_PYQ_1" || filename.includes("OM22001 (2)")) {
    return CHATGPT_ANSWER_LINKS.SEM_PYQ_1.chatGptUrl;
  }
  if (examCode === "SEM_PYQ_2" || filename.includes("OM22001 (1)")) {
    return CHATGPT_ANSWER_LINKS.SEM_PYQ_2.chatGptUrl;
  }
  if (examCode === "SEM_PYQ_3" || (filename.includes("OM22001.pdf") && !filename.includes("-"))) {
    return CHATGPT_ANSWER_LINKS.SEM_PYQ_3.chatGptUrl;
  }
  if (examCode === "SEM_PYQ_4" || filename.includes("25211048") || filename.includes("323580")) {
    return CHATGPT_ANSWER_LINKS.SEM_PYQ_4.chatGptUrl;
  }

  // FAT check
  if (filename.toLowerCase().includes("fat 1") || filename.includes("AY2025_2026") || filename.includes("AY2024_2025")) {
    if (filename.includes("2024") || filename.includes("AY2024_2025")) {
      return CHATGPT_ANSWER_LINKS.FAT_1_AY2024_2025.chatGptUrl;
    }
    return CHATGPT_ANSWER_LINKS.FAT_1_AY2025_2026.chatGptUrl;
  }
  if (examCode === "FAT_1" || filename.includes("AY2024_2025")) {
    return CHATGPT_ANSWER_LINKS.FAT_1_AY2024_2025.chatGptUrl;
  }
  if (examCode === "FAT_2" || filename.toLowerCase().includes("fat 2")) {
    return CHATGPT_ANSWER_LINKS.FAT_2_AY2024_2025.chatGptUrl;
  }
  if (examCode === "FAT_3" || filename.toLowerCase().includes("fat 3")) {
    return CHATGPT_ANSWER_LINKS.FAT_3_AY2024_2025.chatGptUrl;
  }

  return null;
}


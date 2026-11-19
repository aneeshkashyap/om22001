"use client";

import React, { useState } from "react";
import { MathView } from "@/components/papers/MathView";
import { 
  Code, 
  Copy, 
  Check, 
  Eye, 
  ExternalLink, 
  FileJson
} from "lucide-react";

const CHATGPT_LINKS = [
  "https://chatgpt.com/share/6af49506-0a44-83ec-85c1-6ecbbadda047",
  "https://chatgpt.com/share/6af49517-7c80-83ec-a422-4c8bde96cd14",
  "https://chatgpt.com/share/6af49529-ded8-83ee-ac96-a10049547724",
  "https://chatgpt.com/share/6af49542-88b8-83ee-9b4a-769b1ec3d454",
  "https://chatgpt.com/share/6af4955a-b0f0-83ec-bfa4-a3257b13a4de",
  "https://chatgpt.com/share/6af49571-bafc-83e8-af94-15f7f6f48800",
  "https://chatgpt.com/share/6af49588-ac1c-83ee-ab3e-b65021201e1d",
  "https://chatgpt.com/share/6af4959d-3f40-83ee-a7bc-7562286c5b1b",
];

const PAPERS = [
  { id: "2024-dec-sem5-147184", label: "Dec 2024, Sem 5 (Q.147184)" },
  { id: "2025-may-sem5-405686", label: "May 2025, Sem 5 (Q.405686)" },
  { id: "2025-dec-sem6-133554", label: "Dec 2025, Sem 6 (Q.133554)" },
  { id: "2026-may-sem6-323580", label: "May 2026, Sem 6 (Q.323580)" },
  { id: "fat-1", label: "FAT-1 Assessment" },
  { id: "fat-2", label: "FAT-2 Assessment" },
  { id: "fat-3", label: "FAT-3 Assessment" },
];

export default function AdminImportPage() {
  const [paperId, setPaperId] = useState("2024-dec-sem5-147184");
  const [part, setPart] = useState("A");
  const [qNum, setQNum] = useState("1");
  const [marks, setMarks] = useState(2);
  const [co, setCo] = useState(1);
  const [rbt, setRbt] = useState(2);
  const [unit, setUnit] = useState(1);
  const [topic, setTopic] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [stepsRaw, setStepsRaw] = useState("");
  const [finalAnswer, setFinalAnswer] = useState("");
  const [tableValuesUsed, setTableValuesUsed] = useState("");
  const [sourceLink, setSourceLink] = useState(CHATGPT_LINKS[0]);
  const [needsReview, setNeedsReview] = useState(false);
  const [copied, setCopied] = useState(false);

  const stepsList = stepsRaw
    .split("\n")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);


  const generatedQuestionObject = {
    id: `${paperId}-q${qNum.toLowerCase().replace(/[^a-z0-9]/g, "")}`,
    paperId,
    part,
    number: qNum,
    marks: Number(marks),
    co: Number(co),
    rbt: Number(rbt),
    unit: Number(unit),
    topic: topic || "Statistical Concepts",
    questionText: questionText.trim(),
    tables: [],
    answer: {
      status: stepsList.length > 0 ? "complete" : "pending",
      steps: stepsList,
      finalAnswer: finalAnswer.trim(),
      tableValuesUsed: tableValuesUsed.trim() || "None",
      sourceLink,
    },
    needsReview,
    tags: ["om22001"],
  };

  const jsonString = JSON.stringify(generatedQuestionObject, null, 2);

  const handleCopyJson = () => {
    navigator.clipboard.writeText(jsonString).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="space-y-8 pb-12 max-w-5xl mx-auto">
      {/* Header */}
      <div className="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-5">
        <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary-100 dark:bg-primary-950 text-primary-700 dark:text-primary-300">
          <Code className="w-3.5 h-3.5" />
          <span>Local Admin Helper (Hidden in Production Menu)</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Answer & Question JSON Generator
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
          Paste answers from your ChatGPT shared threads or solution notes. Preview mathematical formulas rendered via KaTeX in real-time, then copy the generated JSON entry to paste into your paper file.
        </p>
      </div>

      {/* ChatGPT Sources List */}
      <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-soft space-y-3">
        <h3 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <span>Registered ChatGPT Solution Threads (8 Links):</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          {CHATGPT_LINKS.map((link, idx) => (
            <div
              key={link}
              className="flex items-center justify-between p-2 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800"
            >
              <div className="flex items-center gap-2 truncate">
                <span className="font-mono text-primary-600 dark:text-primary-400 font-bold">#{idx + 1}</span>
                <span className="truncate text-slate-600 dark:text-slate-400">{link}</span>
              </div>
              <a
                href={link}
                target="_blank"
                rel="noreferrer"
                className="text-primary-600 hover:text-primary-700 p-1 shrink-0"
                title="Open thread in browser"
              >
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          ))}
        </div>
      </div>

      {/* Main Grid: Input Form & Live Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Col: Input Controls */}
        <div className="space-y-4">
          <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            1. Metadata & Question Details
          </h2>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Paper:
              </label>
              <select
                value={paperId}
                onChange={(e) => setPaperId(e.target.value)}
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              >
                {PAPERS.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Part:
              </label>
              <select
                value={part}
                onChange={(e) => {
                  setPart(e.target.value);
                  setMarks(e.target.value === "A" ? 2 : 10);
                }}
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              >
                <option value="A">Part A (2 Marks)</option>
                <option value="B">Part B (10 Marks)</option>
                <option value="C">Part C (10 Marks Compulsory)</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-4 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Q. No:
              </label>
              <input
                type="text"
                value={qNum}
                onChange={(e) => setQNum(e.target.value)}
                placeholder="21(a)"
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Unit (1-5):
              </label>
              <input
                type="number"
                min={1}
                max={5}
                value={unit}
                onChange={(e) => {
                  setUnit(Number(e.target.value));
                  setCo(Number(e.target.value));
                }}
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                CO:
              </label>
              <input
                type="number"
                min={1}
                max={5}
                value={co}
                onChange={(e) => setCo(Number(e.target.value))}
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                RBT:
              </label>
              <input
                type="number"
                min={1}
                max={4}
                value={rbt}
                onChange={(e) => setRbt(Number(e.target.value))}
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Topic Name:
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Student's t-Test for Difference of Two Means"
              className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Question Text (use $...$ for KaTeX formulas):
            </label>
            <textarea
              rows={3}
              value={questionText}
              onChange={(e) => setQuestionText(e.target.value)}
              placeholder="Paste exact question statement here..."
              className="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white font-serif leading-relaxed"
            />
          </div>

          <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider pt-3">
            2. Worked Solution Steps
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Solution Steps (Enter one step per line):
            </label>
            <textarea
              rows={6}
              value={stepsRaw}
              onChange={(e) => setStepsRaw(e.target.value)}
              placeholder="Step 1: State hypotheses $H_0: \mu_1 = \mu_2$ vs $H_1: \mu_1 \neq \mu_2$&#10;Step 2: Formula $t = \frac{\bar{x}_1 - \bar{x}_2}{S_p \sqrt{1/n_1 + 1/n_2}}$&#10;Step 3: Substitution and calculation..."
              className="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white font-mono leading-relaxed"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Final Answer:
              </label>
              <input
                type="text"
                value={finalAnswer}
                onChange={(e) => setFinalAnswer(e.target.value)}
                placeholder="e.g. Accept $H_0$ ($t = 1.92 < 2.26$)"
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Table Values Cited:
              </label>
              <input
                type="text"
                value={tableValuesUsed}
                onChange={(e) => setTableValuesUsed(e.target.value)}
                placeholder="e.g. $t$ at 5% with df=9 is 2.262"
                className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Mapped ChatGPT Source Thread:
            </label>
            <select
              value={sourceLink}
              onChange={(e) => setSourceLink(e.target.value)}
              className="w-full text-xs p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white font-mono"
            >
              {CHATGPT_LINKS.map((link, idx) => (
                <option key={link} value={link}>
                  Thread #{idx + 1} ({link.slice(-12)})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-4 pt-1">
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                checked={needsReview}
                onChange={(e) => setNeedsReview(e.target.checked)}
                className="rounded border-slate-300 text-primary-600 focus:ring-primary-500"
              />
              <span>Flag as &quot;needsReview: true&quot;</span>
            </label>
          </div>
        </div>

        {/* Right Col: Live KaTeX Preview & Generated JSON */}
        <div className="space-y-6">
          <div className="space-y-2">
            <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <Eye className="w-4 h-4 text-emerald-500" />
              <span>Live KaTeX Preview</span>
            </h2>
            <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-soft space-y-4">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-xs font-bold bg-slate-900 dark:bg-white text-white dark:text-slate-900">
                  Q. {qNum}
                </span>
                <span className="text-xs font-semibold text-primary-600">
                  {marks} Marks • Unit {unit} • CO{co}
                </span>
              </div>

              <div className="font-serif text-sm text-slate-800 dark:text-slate-200 leading-relaxed">
                {questionText ? (
                  <MathView text={questionText} />
                ) : (
                  <span className="text-slate-400 italic">Question preview will appear here...</span>
                )}
              </div>

              {stepsList.length > 0 && (
                <div className="border-t border-slate-100 dark:border-slate-800 pt-3 space-y-2 text-xs text-slate-700 dark:text-slate-300">
                  <div className="font-bold uppercase tracking-wider text-slate-900 dark:text-slate-200">
                    Solution Steps:
                  </div>
                  {stepsList.map((st, i) => (
                    <div key={i} className="flex items-start gap-1.5">
                      <span className="text-primary-500">•</span>
                      <div>
                        <MathView text={st} />
                      </div>
                    </div>
                  ))}
                  {finalAnswer && (
                    <div className="p-2.5 rounded bg-primary-50 dark:bg-primary-950/40 text-primary-900 dark:text-primary-200 font-semibold mt-2">
                      Final Answer: <MathView text={finalAnswer} />
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Generated JSON Output */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                <FileJson className="w-4 h-4 text-primary-500" />
                <span>Generated JSON Block</span>
              </h2>

              <button
                onClick={handleCopyJson}
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-primary-600 hover:bg-primary-700 text-white text-xs font-bold shadow-sm transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? "Copied JSON!" : "Copy JSON Entry"}</span>
              </button>
            </div>

            <pre className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-900 text-slate-100 text-xs font-mono overflow-x-auto max-h-72">
              {jsonString}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}


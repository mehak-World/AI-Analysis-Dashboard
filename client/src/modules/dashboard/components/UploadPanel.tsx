import { useState, useCallback } from "react";
import { UploadCloud, Loader2, AlertCircle, FileSpreadsheet, X } from "lucide-react";
import { uploadCSV } from "../api/api.dashboard";

interface UploadPanelProps {
  onUploadSuccess: (sessionId: string) => void;
}

const UploadPanel = ({ onUploadSuccess }: UploadPanelProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped?.name.endsWith(".csv")) {
      setFile(dropped);
      setError("");
    } else {
      setError("Please drop a .csv file");
    }
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    try {
      setUploading(true);
      setError("");
      const res = await uploadCSV(file);
      const sessionId = res?.data?.data?.sessionId;
      if (!sessionId) throw new Error("No session id returned");
      onUploadSuccess(sessionId);
      setFile(null);
    } catch (err: any) {
      setError(err?.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center p-8 relative overflow-hidden">
      {/* Ambient gradient glow */}
      <div className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-teal-500/10 via-cyan-500/5 to-blue-500/10 rounded-full blur-3xl" />

      <div className="relative w-full max-w-md">
        {/* Card with subtle gradient border */}
        <div className="rounded-2xl p-[1px] bg-gradient-to-br from-teal-400/30 via-zinc-800 to-blue-500/20">
          <div className="rounded-2xl bg-zinc-950 p-10">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center mb-5">
              <UploadCloud size={20} className="text-zinc-950" />
            </div>

            <h2 className="text-2xl font-bold text-white mb-1.5 tracking-tight">
              Analyze a Dataset
            </h2>
            <p className="text-sm text-zinc-400 mb-7 leading-relaxed">
              Upload a CSV file to get instant statistics, visualizations, and AI-powered insights.
            </p>

            {!file ? (
              <label
                htmlFor="csv-input"
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragOver(true);
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleDrop}
                className={`relative block rounded-xl p-10 text-center cursor-pointer transition-all mb-4 ${
                  dragOver
                    ? "bg-gradient-to-br from-teal-400/10 to-blue-500/10 ring-2 ring-teal-400"
                    : "bg-zinc-900/40 ring-1 ring-zinc-800 hover:ring-teal-400/40 hover:bg-zinc-900/60"
                }`}
              >
                <input
                  id="csv-input"
                  type="file"
                  accept=".csv"
                  className="hidden"
                  onChange={(e) => {
                    const selected = e.target.files?.[0];
                    if (selected) {
                      setFile(selected);
                      setError("");
                    }
                  }}
                />
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-teal-500/15 to-blue-500/15 ring-1 ring-white/5 flex items-center justify-center mx-auto mb-3.5">
                  <UploadCloud
                    size={20}
                    className={dragOver ? "text-teal-300" : "text-zinc-500"}
                  />
                </div>
                <div className="text-sm font-medium text-zinc-200">
                  Drop your CSV here
                </div>
                <div className="text-xs text-zinc-500 mt-1">or click to browse</div>
              </label>
            ) : (
              <div className="rounded-xl bg-zinc-900/60 ring-1 ring-zinc-800 p-4 mb-4 flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-teal-500/15 to-blue-500/15 ring-1 ring-white/5 flex items-center justify-center shrink-0">
                  <FileSpreadsheet size={17} className="text-cyan-300" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">{file.name}</p>
                  <p className="text-xs text-zinc-500 mt-0.5">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>
                <button
                  onClick={() => setFile(null)}
                  className="shrink-0 w-7 h-7 rounded-md flex items-center justify-center text-zinc-500 hover:text-white hover:bg-zinc-800 transition-colors"
                >
                  <X size={15} />
                </button>
              </div>
            )}

            {error && (
              <div className="flex items-center gap-1.5 text-xs text-red-400 mb-4">
                <AlertCircle size={13} />
                {error}
              </div>
            )}

            <button
              disabled={!file || uploading}
              onClick={handleUpload}
              className={`w-full py-3 rounded-lg text-sm font-semibold transition-all flex items-center justify-center gap-2 ${
                !file || uploading
                  ? "bg-zinc-900 text-zinc-600 cursor-not-allowed ring-1 ring-zinc-800"
                  : "bg-gradient-to-r from-teal-400 to-blue-500 text-zinc-950 hover:shadow-lg hover:shadow-teal-500/20 hover:-translate-y-0.5"
              }`}
            >
              {uploading && <Loader2 size={15} className="animate-spin" />}
              {uploading ? "Uploading…" : "Analyze Dataset"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPanel;
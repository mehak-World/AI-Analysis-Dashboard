import { useState } from "react";
import { Menu } from "lucide-react";
import AllSessions from "../components/AllSessions";
import UploadPanel from "../components/UploadPanel";
import SessionAnalysis from "../components/SessionAnalysis";
import useSessions from "../hooks/useSessions";

const isMobile = () => typeof window !== "undefined" && window.innerWidth < 768;

const DashboardPage = () => {
  const { sessions, loading, pagination, setPagination, fetchSessions } = useSessions();
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(() => !isMobile());

  const closeOnMobile = () => {
    if (isMobile()) setSidebarOpen(false);
  };

  const handleUploadSuccess = (sessionId: string) => {
    fetchSessions();
    setSelectedSessionId(sessionId);
  };

  return (
    <div className="flex h-dvh overflow-hidden bg-[#020617] text-white">
      {/* Backdrop (mobile only) */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/60 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <AllSessions
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        sessions={sessions}
        loading={loading}
        pagination={pagination}
        setPagination={setPagination}
        selectedSessionId={selectedSessionId}
        onSelectSession={(id) => {
          setSelectedSessionId(id);
          closeOnMobile();
        }}
        onNewSession={() => {
          setSelectedSessionId(null);
          closeOnMobile();
        }}
      />

      <main className="flex-1 min-w-0 overflow-y-auto flex flex-col">
        {/* Top bar with toggle */}
        <div className="sticky top-0 z-20 flex items-center gap-3 px-3 py-2.5 border-b border-zinc-800/80 bg-[#020617]/90 backdrop-blur shrink-0">
          <button
            onClick={() => setSidebarOpen((v) => !v)}
            aria-label="Toggle sidebar"
            className="w-8 h-8 rounded-md flex items-center justify-center text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
          >
            <Menu size={18} />
          </button>
          {!sidebarOpen && (
            <span className="text-sm font-semibold tracking-tight">DataLens</span>
          )}
        </div>

        {selectedSessionId ? (
          <SessionAnalysis
            sessionId={selectedSessionId}
            onSessionReady={fetchSessions}
          />
        ) : (
          <UploadPanel onUploadSuccess={handleUploadSuccess} />
        )}
      </main>
    </div>
  );
};

export default DashboardPage;
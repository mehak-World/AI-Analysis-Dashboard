import { useState } from "react";
import AllSessions from "../components/AllSessions";
import UploadPanel from "../components/UploadPanel";
import SessionAnalysis from "../components/SessionAnalysis";
import useSessions from "../hooks/useSessions";

const DashboardPage = () => {
  const { sessions, loading, pagination, setPagination, fetchSessions } = useSessions();
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);

  const handleUploadSuccess = (sessionId: string) => {
    fetchSessions();
    setSelectedSessionId(sessionId);
  };

  return (
    <div className="flex h-screen bg-[#020617] text-white">
      <AllSessions
        sessions={sessions}
        loading={loading}
        pagination={pagination}
        setPagination={setPagination}
        selectedSessionId={selectedSessionId}
        onSelectSession={setSelectedSessionId}
        onNewSession={() => setSelectedSessionId(null)}
      />

      <main className="flex-1 overflow-y-auto flex flex-col">
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
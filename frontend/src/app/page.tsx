import ChatInterface from "@/components/ChatInterface";
import ScoreViewer from "@/components/ScoreViewer";

export default function Home() {
  return (
    <div className="h-screen flex">
      {/* Left Panel: Chat Interface */}
      <div className="w-1/2 border-r border-[var(--border)]">
        <ChatInterface />
      </div>

      {/* Right Panel: Score Viewer */}
      <div className="flex-1">
        <ScoreViewer />
      </div>
    </div>
  );
}

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Music, MessageSquare, Settings, Upload } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Clef.ai",
  description: "AI-Powered Catholic Hymn Assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen w-full">
          {/* Sidebar */}
          <aside className="w-20 flex flex-col items-center py-8 border-r border-[var(--border)] bg-[var(--surface)] z-10">
            <div className="mb-12">
              <div className="w-10 h-10 rounded-full bg-[var(--primary)] flex items-center justify-center shadow-[0_0_20px_var(--primary-glow)]">
                <Music className="text-[var(--background)] w-6 h-6" />
              </div>
            </div>
            
            <nav className="flex flex-col gap-8 flex-1">
              <NavItem icon={<Upload size={24} />} active />
              <NavItem icon={<MessageSquare size={24} />} />
              <NavItem icon={<Music size={24} />} />
            </nav>

            <div className="mt-auto">
              <NavItem icon={<Settings size={24} />} />
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 relative overflow-hidden">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--primary-glow),_transparent_40%)] pointer-events-none" />
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}

function NavItem({ icon, active = false }: { icon: React.ReactNode; active?: boolean }) {
  return (
    <button
      className={`p-3 rounded-xl transition-all duration-300 ${
        active
          ? "bg-[var(--primary)] text-[var(--background)] shadow-[0_0_15px_var(--primary-glow)]"
          : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[rgba(255,255,255,0.05)]"
      }`}
    >
      {icon}
    </button>
  );
}

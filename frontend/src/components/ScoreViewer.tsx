"use client";

import { useState } from "react";
import { Music } from "lucide-react";

export default function ScoreViewer() {
    const [selectedScore, setSelectedScore] = useState<string | null>(null);

    return (
        <div className="h-full flex flex-col bg-[var(--surface)]">
            {/* Header */}
            <div className="p-4 border-b border-[var(--border)] flex items-center justify-between">
                <h2 className="text-lg font-medium text-[var(--text-primary)]">Score</h2>
                <div className="flex items-center gap-2">
                    <button className="glass-button text-xs px-3 py-1.5">
                        Adam Te Deum
                    </button>
                </div>
            </div>

            {/* Score Display Area */}
            <div className="flex-1 overflow-auto p-6">
                {selectedScore ? (
                    <div className="w-full h-full flex items-center justify-center">
                        <img
                            src={selectedScore}
                            alt="Sheet Music"
                            className="max-w-full max-h-full object-contain"
                        />
                    </div>
                ) : (
                    <div className="w-full h-full flex flex-col items-center justify-center text-center">
                        <div className="w-24 h-24 rounded-full bg-[rgba(255,255,255,0.03)] flex items-center justify-center mb-6">
                            <Music className="text-[var(--text-secondary)]" size={48} />
                        </div>
                        <h3 className="text-xl font-medium text-[var(--text-primary)] mb-2">
                            No Score Selected
                        </h3>
                        <p className="text-sm text-[var(--text-secondary)] max-w-md">
                            Upload a sheet music file or select from your library to view the score here.
                        </p>
                    </div>
                )}
            </div>

            {/* Sample Score Images (for demo) */}
            <div className="p-4 border-t border-[var(--border)]">
                <div className="flex gap-2 overflow-x-auto">
                    {[1, 2, 3].map((i) => (
                        <div
                            key={i}
                            className="flex-shrink-0 w-32 h-40 bg-[var(--surface-highlight)] rounded-lg border border-[var(--border)] cursor-pointer hover:border-[var(--primary)] transition-colors flex items-center justify-center"
                            onClick={() => setSelectedScore(null)}
                        >
                            <Music className="text-[var(--text-secondary)]" size={32} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

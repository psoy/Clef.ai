"use client";

import { useState, useRef } from "react";
import { Upload, FileMusic, CheckCircle, AlertCircle } from "lucide-react";

export default function UploadSection() {
    const [uploading, setUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<{
        type: "success" | "error" | null;
        message: string;
    }>({ type: null, message: "" });
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        await uploadFile(file);
    };

    const handleBrowseClick = () => {
        fileInputRef.current?.click();
    };

    const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        const file = event.dataTransfer.files?.[0];
        if (!file) return;

        await uploadFile(file);
    };

    const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
    };

    const uploadFile = async (file: File) => {
        // Check file type
        const validExtensions = [".xml", ".mxl", ".pdf"];
        const fileExtension = file.name.substring(file.name.lastIndexOf(".")).toLowerCase();

        if (!validExtensions.includes(fileExtension)) {
            setUploadStatus({
                type: "error",
                message: "Please upload a MusicXML (.xml, .mxl) or PDF file.",
            });
            return;
        }

        setUploading(true);
        setUploadStatus({ type: null, message: "" });

        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch("http://localhost:8000/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Upload failed");
            }

            const data = await response.json();
            setUploadStatus({
                type: "success",
                message: `Successfully uploaded ${file.name}!`,
            });

            // Clear the file input
            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }

            // Clear success message after 3 seconds
            setTimeout(() => {
                setUploadStatus({ type: null, message: "" });
            }, 3000);
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus({
                type: "error",
                message: "Failed to upload file. Please try again.",
            });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div
            className="glass-panel p-6 flex flex-col items-center justify-center text-center border-dashed border-2 border-[var(--border)] hover:border-[var(--primary)] transition-colors cursor-pointer group relative"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={handleBrowseClick}
        >
            <input
                ref={fileInputRef}
                type="file"
                accept=".xml,.mxl,.pdf"
                onChange={handleFileSelect}
                className="hidden"
            />

            <div className="w-16 h-16 rounded-full bg-[rgba(255,255,255,0.03)] flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                {uploading ? (
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[var(--primary)]"></div>
                ) : (
                    <Upload
                        className="text-[var(--text-secondary)] group-hover:text-[var(--primary)] transition-colors"
                        size={32}
                    />
                )}
            </div>

            <h3 className="text-lg font-medium text-[var(--text-primary)] mb-2">
                Upload Sheet Music
            </h3>
            <p className="text-sm text-[var(--text-secondary)] mb-4">
                Drag & drop PDF or MusicXML files here
            </p>

            <button
                className="glass-button text-sm"
                disabled={uploading}
                onClick={(e) => {
                    e.stopPropagation();
                    handleBrowseClick();
                }}
            >
                {uploading ? "Uploading..." : "Browse Files"}
            </button>

            {/* Status Message */}
            {uploadStatus.type && (
                <div
                    className={`absolute bottom-4 left-4 right-4 p-3 rounded-lg flex items-center gap-2 ${uploadStatus.type === "success"
                            ? "bg-green-500/20 border border-green-500/50"
                            : "bg-red-500/20 border border-red-500/50"
                        }`}
                >
                    {uploadStatus.type === "success" ? (
                        <CheckCircle size={18} className="text-green-400" />
                    ) : (
                        <AlertCircle size={18} className="text-red-400" />
                    )}
                    <span className="text-sm text-[var(--text-primary)]">
                        {uploadStatus.message}
                    </span>
                </div>
            )}
        </div>
    );
}

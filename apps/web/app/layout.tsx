import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Biometric Auditor",
    description: "AI COACH for your workout resolutions",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}

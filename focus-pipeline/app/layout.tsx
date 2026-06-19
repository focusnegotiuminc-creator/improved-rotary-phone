import type { Metadata, Viewport } from "next";
import { Geist_Mono, Space_Grotesk, Cormorant_Garamond } from "next/font/google";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
  weight: ["400", "500", "700"],
});

const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  subsets: ["latin"],
  weight: ["500", "600", "700"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "FOCUS MASTER AI — Pipeline Control",
  description:
    "Private AI orchestration pipeline for Focus Negotium Inc, Royal Lee Construction Solutions, and Focus Records LLC. Multi-engine task automation with live streaming output.",
  keywords: ["Focus Negotium", "AI Pipeline", "Orchestration", "Business Automation"],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#060c18",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${spaceGrotesk.variable} ${cormorant.variable} ${geistMono.variable} bg-background`}
    >
      <body className="min-h-screen font-sans text-foreground ambient-glow">
        {children}
      </body>
    </html>
  );
}

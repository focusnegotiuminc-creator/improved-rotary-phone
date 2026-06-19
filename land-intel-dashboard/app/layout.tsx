import type { Metadata, Viewport } from "next";
import { Source_Sans_3, Source_Serif_4, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const sans = Source_Sans_3({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});
const serif = Source_Serif_4({
  subsets: ["latin"],
  variable: "--font-serif",
  display: "swap",
});
const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Land Intelligence Investigation — 39.6810292° N, 91.4115990° W",
  description:
    "Geo-legal land intelligence dashboard: coordinate location report, professional map legend & key, hydrology, utilities, trusts & title, and historical research for Marion County, Missouri.",
  applicationName: "Land Intelligence OS",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#2e4a39",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`bg-background ${sans.variable} ${serif.variable} ${mono.variable}`}
    >
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}

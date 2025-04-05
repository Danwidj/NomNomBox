// added from /app/(main)/layout.tsx
// This file is used to set up the layout for the entire application
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
// end of added layout
import "./globals.css";

// added from /app/(main)/layout.tsx
const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
  });
  
  const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
  });
  
  export const metadata: Metadata = {
    title: "NomNomGo",
    description:
      "Website for NomNomBox drivers to manage their availability and deliveries",
  };
// end of added layout
  
export default function RootLayout({
    children,
  }: {
    children: React.ReactNode;
  }) {
    return (
      <html lang="en">
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>{children}</body>
      </html>
    );
  }
  
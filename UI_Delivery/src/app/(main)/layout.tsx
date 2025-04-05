// import type { Metadata } from "next";
// import { Geist, Geist_Mono } from "next/font/google";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset } from "@/components/ui/sidebar";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import { Toaster } from "sonner";
import "../globals.css";

// const geistSans = Geist({
//   variable: "--font-geist-sans",
//   subsets: ["latin"],
// });
// 
// const geistMono = Geist_Mono({
//   variable: "--font-geist-mono",
//   subsets: ["latin"],
// });
// 
// export const metadata: Metadata = {
//   title: "NomNomGo",
//   description:
//     "Website for NomNomBox drivers to manage their availability and deliveries",
// };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
//    <html lang="en">
//      <body
//        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
//      >
        <SidebarProvider>
          <AppSidebar />
          <SidebarInset>
            <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
              <SidebarTrigger className="-ml-1" />
              {/* <Separator orientation="vertical" className="mr-2 h-4" /> */}
              <Breadcrumb>Manage Deliveries</Breadcrumb>
            </header>
            {children}
            <Toaster />
          </SidebarInset>
        </SidebarProvider>
//      </body>
//    </html>
  );
}


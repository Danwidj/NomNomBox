"use client";
import Image from "next/image";
import { useEffect } from "react";
// import { GalleryVerticalEnd } from "lucide-react"
import { LoginForm } from "@/components/login-form"

export default function LoginPage() {
  useEffect(() => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("driver_id");
  }, []);

  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-center gap-2 md:justify-start">
          <a href="#" className="flex items-center gap-2 font-medium">
            <div>
              <Image
                src="/favicon.ico"
                alt="NomNomGo logo"
                width={24}
                height={24}
                className="rounded-md"
              />
            </div>
            NomNomGo
          </a>
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            <LoginForm />
          </div>
        </div>
      </div>
      <div className="relative hidden bg-muted lg:block">
        <img
          src="/images/driver.png"
          alt="This is a website for NomNomBox drivers to manage their availability and deliveries"
          className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
        />
      </div>
    </div>
  )
}
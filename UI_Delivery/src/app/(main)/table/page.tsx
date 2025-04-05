"use client";

import DataTableDemo from "./table";
import * as React from "react";

export default function Page() {
  return (
    <>
      <div className="w-[40%] m-auto">
        <h1 className="text-4xl">Deliveries</h1>
        <div>
          <DataTableDemo />
        </div>
      </div>
    </>
  );
}

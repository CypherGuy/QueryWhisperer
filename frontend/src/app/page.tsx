"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <main className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">QueryWhisperer</h1>
      <p>
        Welcome to QueryWhisperer — a simple tool that lets you ask questions in
        plain English and get SQL queries back, powered by AI.
      </p>
      <p>
        You’ll need to{" "}
        <Link href="/login" className="text-blue-600 underline">
          log in
        </Link>{" "}
        to get started. Once logged in, head to the{" "}
        <Link href="/query" className="text-blue-600 underline">
          query page
        </Link>{" "}
        to try it out.
      </p>
      <p className="text-sm text-gray-600">
        Note: You’ll need a schema (table + column names) to generate accurate
        results.
      </p>
    </main>
  );
}

"use client";

import { useState } from "react";

export default function QueryPage() {
  const [question, setQuestion] = useState("");
  const [schemaJson, setSchemaJson] = useState("");
  const [sql, setSql] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSql("");
    setLoading(true);

    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("You must log in first.");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          question,
          db_schema: JSON.parse(schemaJson || "[]"),
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to generate SQL.");
      setSql(data.generated_sql);
    } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred.");
        }
      }
      

  return (
    <main className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Query Your Database</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="w-full border p-2 rounded"
          placeholder="Natural language question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <textarea
          className="w-full border p-2 rounded"
          placeholder='Schema as JSON (e.g. [{"table":"users","columns":["id","name"]}])'
          value={schemaJson}
          onChange={(e) => setSchemaJson(e.target.value)}
          rows={5}
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Generate SQL
        </button>
      </form>

      {/* ✅ Loading indicator */}
      {loading && !error && (
        <p className="text-gray-500">Generating query...</p>
      )}

      {sql && (
        <div className="bg-gray-800 text-white border border-gray-700 p-4 rounded whitespace-pre-wrap">
          <h2 className="font-semibold mb-2">Generated SQL:</h2>
          {sql}
        </div>
      )}

      {error && (
        <div className="bg-red-100 border p-4 rounded text-red-700">
          {error}
        </div>
      )}
    </main>
  );
}

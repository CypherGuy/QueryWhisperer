"use client";

import { useState, useEffect } from "react";

export default function QueryPage() {
  const [question, setQuestion] = useState("");
  const [schemaJson, setSchemaJson] = useState("");
  const [sql, setSql] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    if (error || successMessage) {
      const timer = setTimeout(() => {
        setError("");
        setSuccessMessage("");
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, successMessage]);

  async function saveKey() {
    setError("");
    setSuccessMessage("");
    setSaving(true);

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("You must log in first.");
        return;
      }

      if (!apiKey) {
        setError("The API key cannot be blank.");
        return;
      }

      const apiKeyRegex = /^sk-[a-zA-Z0-9-_]{20,}$/;
      if (!apiKeyRegex.test(apiKey)) {
        setError("Invalid API key format.");
        return;
      }

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/users/openai-key`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ key: apiKey }),
        }
      );

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to save API key.");
      }

      setSuccessMessage("API key saved successfully!");
    } catch (err) {
      console.error(err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error occurred");
      }
    } finally {
      setSaving(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSuccessMessage("");
    setSql("");
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("You must log in first.");
        return;
      }

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
      if (!res.ok) {
        throw new Error(data.detail || "Failed to generate SQL.");
      }
      setSql(data.generated_sql);
      setSuccessMessage("Query generated successfully!");
    } catch (err) {
      console.error(err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Query Your Database</h1>

      {/* Toast notification */}
      {successMessage && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          {successMessage}
        </div>
      )}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="space-y-2">
        <label className="block font-semibold">OpenAI API Key</label>
        <input
          type="password"
          placeholder="sk-..."
          className="border p-2 w-full"
          onChange={(e) => setApiKey(e.target.value)}
        />
        <button
          type="button"
          onClick={saveKey}
          className="bg-gray-800 text-white px-4 py-2 rounded hover:bg-gray-700"
          disabled={saving}
        >
          {saving ? "Saving..." : "Save Key"}
        </button>
      </div>

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
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate SQL"}
        </button>
      </form>

      {sql && (
        <div className="bg-gray-800 text-white border border-gray-700 p-4 rounded whitespace-pre-wrap">
          <h2 className="font-semibold mb-2">Generated SQL:</h2>
          {sql}
        </div>
      )}
    </main>
  );
}

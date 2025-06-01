"use client";

import Link from "next/link";
import { useState } from "react";

export default function HomePage() {
  const [activeTab, setActiveTab] = useState(0);

  const faqs = [
    {
      question: "How accurate are the SQL queries?",
      answer:
        "Our AI generates highly accurate SQL queries based on your database schema and natural language input. The more specific your question and the more complete your schema, the more accurate the results will be.",
    },
    {
      question: "Do I need to know SQL to use this tool?",
      answer:
        "Not at all! That's the beauty of QueryWhisperer. You can ask questions in plain English, and our AI will translate them into SQL queries for you.",
    },
    {
      question: "What databases are supported?",
      answer:
        "QueryWhisperer supports all major SQL databases including PostgreSQL, MySQL, SQL Server, and SQLite.",
    },
    {
      question: "How do I provide my database schema?",
      answer:
        "After logging in, you can upload your schema in the settings section or paste it directly when creating a new query.",
    },
  ];

  return (
    <div className="min-h-screen bg-black bg-gradient-to-br from-black to-gray-900">
      {/* Navbar */}
      <nav className="border-b border-gray-800 bg-gray-950/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl font-bold text-white">
                QueryWhisperer
              </Link>
            </div>
            <div className="flex items-center space-x-6">
              <Link
                href="/query"
                className="text-gray-300 hover:text-white transition-colors duration-200"
              >
                Query
              </Link>
              <Link
                href="/login"
                className="bg-white hover:bg-gray-200 text-black px-4 py-2 rounded-md font-medium transition-colors duration-200"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content Container */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <div className="text-center space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold text-white">
              QueryWhisperer
            </h1>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Transform plain English questions into SQL queries with the power
              of AI
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
              <Link
                href="/login"
                className="bg-white hover:bg-gray-200 text-black px-6 py-3 rounded-md font-medium transition-colors duration-200 w-full sm:w-auto text-center"
              >
                Get Started
              </Link>
              <Link
                href="/query"
                className="border border-gray-600 hover:border-gray-500 text-white px-6 py-3 rounded-md font-medium transition-colors duration-200 w-full sm:w-auto text-center"
              >
                Try Demo
              </Link>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center flex-shrink-0">
                <svg
                  className="w-5 h-5 text-black"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-white">AI-Powered</h3>
            </div>
            <p className="text-gray-300">
              Advanced AI understands your natural language questions and
              converts them into precise SQL queries.
            </p>
          </div>

          <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center flex-shrink-0">
                <svg
                  className="w-5 h-5 text-black"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-white">
                Fast & Simple
              </h3>
            </div>
            <p className="text-gray-300">
              No need to remember complex SQL syntax. Just ask your question in
              plain English and get results instantly.
            </p>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-lg">1</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-3">
                Ask Your Question
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                Type your question in plain English, like &quotShow me all users
                who signed up last month&quot
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-lg">2</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-3">
                AI Processes
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                Our AI analyzes your question and your database schema to
                understand what you need
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-lg">3</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-3">
                Get SQL Query
              </h3>
              <p className="text-gray-300 text-sm leading-relaxed">
                Receive a perfectly formatted SQL query ready to run on your
                database
              </p>
            </div>
          </div>
        </div>

        {/* Example Section */}
        <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            See It In Action
          </h2>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="text-gray-400 text-sm ml-2">Query Example</span>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-gray-300 font-medium mb-2">Your question:</p>
                <div className="bg-gray-800 p-4 rounded-md">
                  <p className="text-white">
                    Show me all customers who made a purchase over $500 last
                    month
                  </p>
                </div>
              </div>

              <div>
                <p className="text-gray-300 font-medium mb-2">Generated SQL:</p>
                <div className="bg-gray-800 p-4 rounded-md overflow-x-auto">
                  <pre className="text-green-400 text-sm whitespace-pre-wrap font-mono">
                    {`SELECT c.customer_id, c.first_name, c.last_name, c.email, o.order_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_total > 500
  AND o.order_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND o.order_date < DATE_TRUNC('month', CURRENT_DATE)
ORDER BY o.order_total DESC;`}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4 max-w-3xl mx-auto">
            {faqs.map((faq, index) => (
              <div
                key={index}
                className="border border-gray-800 rounded-lg overflow-hidden"
              >
                <button
                  className="flex justify-between items-center w-full p-4 text-left bg-gray-900 hover:bg-gray-800 transition-colors"
                  onClick={() => setActiveTab(activeTab === index ? -1 : index)}
                >
                  <span className="text-white font-medium pr-4">
                    {faq.question}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-400 transform transition-transform flex-shrink-0 ${
                      activeTab === index ? "rotate-180" : ""
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>
                {activeTab === index && (
                  <div className="p-4 bg-gray-900 border-t border-gray-800">
                    <p className="text-gray-300 leading-relaxed">
                      {faq.answer}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Getting Started Section */}
        <div className="bg-gray-950 border border-gray-800 rounded-lg shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-gray-300 mb-4">
            You&apos;ll need to{" "}
            <Link
              href="/login"
              className="text-white hover:underline font-medium"
            >
              log in
            </Link>{" "}
            to get started. Once logged in, head to the{" "}
            <Link
              href="/query"
              className="text-white hover:underline font-medium"
            >
              query page
            </Link>{" "}
            to try it out.
          </p>
          <div className="bg-gray-900 border border-gray-700 rounded-md p-4">
            <p className="text-sm text-gray-400 flex items-start space-x-2">
              <svg
                className="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span>
                <strong>Note:</strong> You&apos;ll need a schema (table + column
                names) to generate accurate results.
              </span>
            </p>
          </div>
        </div>

        {/* CTA Banner */}
        <div className="bg-gradient-to-r from-gray-900 to-gray-800 border border-gray-700 rounded-lg shadow-xl p-8 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            Ready to simplify your database queries?
          </h2>
          <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
            Join thousands of users who are saving time and effort by using
            natural language to generate SQL.
          </p>
          <Link
            href="/login"
            className="bg-white hover:bg-gray-200 text-black px-8 py-3 rounded-md font-medium transition-colors duration-200 inline-block"
          >
            Get Started for Free
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-800 bg-gray-950 py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <Link href="/" className="text-xl font-bold text-white">
                QueryWhisperer
              </Link>
              <p className="text-gray-400 mt-2 max-w-md">
                Transform plain English questions into SQL queries with the
                power of AI.
              </p>
            </div>
          </div>
          <p className="text-gray-400 text-sm mt-6">
            © {new Date().getFullYear()} QueryWhisperer. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

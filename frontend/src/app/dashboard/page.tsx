"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAuthSession, signOut } from "aws-amplify/auth";
import ReactMarkdown from "react-markdown";
import {
  FiPlus,
  FiBook,
  FiArrowRight,
  FiBell,
  FiSun,
  FiMoon,
  FiMenu,
  FiX,
} from "react-icons/fi";

export default function ChatPage() {
  const router = useRouter();

  const [query, setQuery] = useState("");
  const [darkMode, setDarkMode] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [emailSent, setEmailSent] = useState(false);

  const toggleTheme = () => setDarkMode(!darkMode);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  const runAgent = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);
    setEmailSent(false);

    const session = await fetchAuthSession();
    const token = session.tokens?.idToken?.toString();
    console.log(token);
    const res = await fetch("https://urban-broccoli-69r56vr6v7w62575w-8080.app.github.dev/agent-run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ user_input: query }),
    });

    const json = await res.json();

    if (json.status === "success") {
      setResult(json.data);
      setEmailSent(true);
    }

    setLoading(false);
  };

  return (
    <div
      className={`min-h-screen ${
        darkMode ? "bg-black text-white" : "bg-white text-black"
      } flex transition-colors duration-300`}
    >
      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full z-50 transition-all duration-300 ease-in-out ${
          sidebarOpen ? "w-64" : "w-16"
        } ${
          darkMode ? "bg-gray-900 border-gray-700" : "bg-gray-100 border-gray-300"
        } border-r p-4`}
      >
        <div className="flex justify-between items-center mb-6">
          <h1 className={`font-bold transition-all duration-300 ${sidebarOpen ? "opacity-100" : "opacity-0"}`}>
            {sidebarOpen ? "Synthera" : "🧪"}
          </h1>
          <button onClick={toggleSidebar} className="hover:scale-110 transition-transform duration-200">
            {sidebarOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>

        <div className="space-y-4 text-sm">
          <div className="flex gap-2 items-center cursor-pointer hover:translate-x-1 transition-transform duration-200">
            <FiPlus /> {sidebarOpen && <span className="animate-fadeIn">New Query</span>}
          </div>
          <div className="flex gap-2 items-center cursor-pointer hover:translate-x-1 transition-transform duration-200">
            <FiBook /> {sidebarOpen && <span className="animate-fadeIn">History</span>}
          </div>
        </div>
      </aside>

      {/* Main */}
      <main
        className={`flex-1 px-6 py-8 transition-all duration-300 ${
          sidebarOpen ? "ml-64" : "ml-16"
        }`}
      >
        {/* Top bar */}
        <div className="flex justify-end gap-4 mb-6">
          <FiBell className="text-xl hover:scale-110 transition-transform duration-200 cursor-pointer animate-pulse" />
          <button onClick={toggleTheme} className="hover:rotate-180 transition-transform duration-500">
            {darkMode ? <FiSun /> : <FiMoon />}
          </button>
          <button
            onClick={handleLogout}
            className="text-xs bg-purple-600 px-3 py-1 rounded hover:bg-purple-700 hover:scale-105 transition-all duration-200"
          >
            Sign out
          </button>
        </div>

        {/* Query box */}
        <div className="max-w-3xl mx-auto mb-6">
          <div
            className={`flex items-center rounded-full px-4 py-3 transition-all duration-300 ${
              darkMode ? "bg-gray-800" : "bg-gray-200"
            } ${loading ? "animate-pulse" : ""}`}
          >
            <input
              className="flex-1 bg-transparent outline-none"
              placeholder="Ask a medical / market intelligence question"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={loading}
            />
            <button 
              onClick={runAgent}
              className="hover:scale-125 transition-transform duration-200 disabled:opacity-50"
              disabled={loading}
            >
              <FiArrowRight className={loading ? "animate-spin" : ""} />
            </button>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="max-w-3xl mx-auto mb-6">
            <div className="flex flex-col items-center space-y-4">
              {/* Animated loader */}
              <div className="relative w-24 h-24">
                <div className="absolute inset-0 border-4 border-purple-600/30 rounded-full"></div>
                <div className="absolute inset-0 border-4 border-transparent border-t-purple-600 rounded-full animate-spin"></div>
                <div className="absolute inset-2 border-4 border-transparent border-t-pink-600 rounded-full animate-spin-reverse"></div>
                <div className="absolute inset-4 border-4 border-transparent border-t-blue-600 rounded-full animate-spin"></div>
              </div>
              
              {/* Animated text */}
              <div className="text-center">
                <div className="text-lg font-semibold mb-2 animate-pulse">
                  Running agents…
                </div>
                <div className="flex items-center gap-2 text-sm opacity-70">
                  <span className="animate-bounce" style={{ animationDelay: "0ms" }}>🧠</span>
                  <span className="animate-bounce" style={{ animationDelay: "150ms" }}>Analyzing</span>
                  <span className="animate-bounce" style={{ animationDelay: "300ms" }}>data</span>
                  <span className="animate-bounce" style={{ animationDelay: "450ms" }}>📊</span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="w-64 h-1 bg-gray-700 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 animate-progress"></div>
              </div>
            </div>
          </div>
        )}

        {/* Email alert */}
        {emailSent && (
          <div className="max-w-3xl mx-auto mb-4 bg-green-600/20 border border-green-500 p-3 rounded text-sm animate-slideDown">
            📧 Report link sent to your email. Check inbox!
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="max-w-4xl mx-auto space-y-8 animate-fadeInUp">
            {/* Web Intelligence */}
            {result.web && (
              <section className="animate-fadeInUp" style={{ animationDelay: "100ms" }}>
                <h2 className="text-xl font-semibold mb-2">
                  🌐 Web Intelligence
                </h2>
                <div className="prose prose-invert max-w-none">
                  <ReactMarkdown>{result.web}</ReactMarkdown>
                </div>
              </section>
            )}

            {/* Clinical Trials */}
            {result.clinical?.active_trials && (
              <section className="animate-fadeInUp" style={{ animationDelay: "200ms" }}>
                <h2 className="text-xl font-semibold mb-2">
                  🧪 Clinical Trials
                </h2>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm border border-gray-700">
                    <thead>
                      <tr className="bg-gray-800">
                        <th className="p-2">Title</th>
                        <th>Phase</th>
                        <th>Sponsor</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.clinical.active_trials.map((t: any, idx: number) => (
                        <tr 
                          key={t.nct_id} 
                          className="border-t border-gray-700 hover:bg-gray-800/50 transition-colors duration-200 animate-fadeInUp"
                          style={{ animationDelay: `${300 + idx * 50}ms` }}
                        >
                          <td className="p-2">{t.title}</td>
                          <td>{t.phase}</td>
                          <td>{t.sponsor}</td>
                          <td>{t.status}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            )}

            {/* PDF */}
            {result.pdf_url && (
              <a
                href={result.pdf_url}
                target="_blank"
                className="inline-block bg-purple-600 px-4 py-2 rounded hover:bg-purple-700 hover:scale-105 hover:shadow-lg transition-all duration-200 animate-fadeInUp"
                style={{ animationDelay: "400ms" }}
              >
                📄 Download Full PDF Report
              </a>
            )}
          </div>
        )}
      </main>

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes progress {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }

        @keyframes spin-reverse {
          from { transform: rotate(360deg); }
          to { transform: rotate(0deg); }
        }

        .animate-fadeIn {
          animation: fadeIn 0.3s ease-in;
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.5s ease-out forwards;
          opacity: 0;
        }

        .animate-slideDown {
          animation: slideDown 0.4s ease-out;
        }

        .animate-progress {
          animation: progress 1.5s ease-in-out infinite;
        }

        .animate-spin-reverse {
          animation: spin-reverse 1s linear infinite;
        }
      `}</style>
    </div>
  );
}
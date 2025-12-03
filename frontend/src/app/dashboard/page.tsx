"use client";

import { useState } from "react";
import {useRouter} from "next/navigation";
import { fetchAuthSession, signOut } from "aws-amplify/auth";
import {
  FiPlus,
  FiBook,
  FiMic,
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
  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };
  const toggleTheme = () => setDarkMode(!darkMode);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className={`min-h-screen ${darkMode ? "bg-black text-white" : "bg-white text-black"} flex`}>
      {/* Expandable Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full z-50 transition-all duration-300 ${
          sidebarOpen ? "w-64" : "w-16"
        } ${darkMode ? "bg-gray-900 border-r border-gray-700" : "bg-gray-100 border-r border-gray-300"} p-4 flex flex-col`}
      >
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-xl font-bold">{sidebarOpen ? "Synthera" : "🧪"}</h1>
          <button onClick={toggleSidebar} className="text-xl">
            {sidebarOpen ? <FiX /> : <FiMenu />}
          </button>
        </div>

        <nav className="space-y-4 text-sm">
          <div className="flex items-center gap-2 cursor-pointer hover:underline">
            <FiPlus /> {sidebarOpen && "New chat"}
          </div>
          <div className="flex items-center gap-2 cursor-pointer hover:underline">
            <FiBook /> {sidebarOpen && "Chat history"}
          </div>
        </nav>
      </aside>

      {/* Main Chat Area */}
      <main className={`flex-1 flex flex-col items-center justify-center px-4 relative ${sidebarOpen ? "ml-64" : "ml-16"}`}>
        {/* Top-right corner icons */}
        <div className="absolute top-4 right-4 flex items-center gap-4">
          <FiBell className="text-xl cursor-pointer" />
          <button onClick={toggleTheme} className="text-xl">
            {darkMode ? <FiSun /> : <FiMoon />}
          </button>
          <button onClick={handleLogout} className="text-xs bg-purple-600 px-2 py-1 rounded hover:bg-purple-700 transition">
          Sign Out
        </button>
        </div>

        <h2 className="text-2xl font-semibold mb-6">What can I help with?</h2>

        <div
          className={`${
            darkMode ? "bg-gray-800 border border-gray-600" : "bg-gray-200 border border-gray-400"
          } flex items-center rounded-full px-4 py-2 w-full max-w-xl`}
        >
          <FiPlus className="mr-3" />
          <input
            type="text"
            placeholder="Ask anything"
            className={`bg-transparent flex-1 placeholder-gray-400 outline-none ${
              darkMode ? "text-white" : "text-black"
            }`}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <FiMic className="mx-2" />
          <FiArrowRight />
        </div>
      </main>
    </div>
  );
}
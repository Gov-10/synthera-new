"use client";
import React, { useState } from 'react';
import { Moon, Sun, Menu, X, Search, Brain, FileText, TrendingUp, Shield, Zap, Globe } from 'lucide-react';
import { useRouter } from "next/navigation";
function pushtoSignUp()
{
  window.location.href = "/signup";
}
function pushtoSignIn()
{
  window.location.href = "/login";
}
export default function LandingPage() {
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const scrollToSection = (id: any) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setMobileMenuOpen(false);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-white' : 'bg-white text-gray-900'}`}>
      {/* Navbar */}
      <nav className={`fixed w-full z-50 transition-all duration-300 ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-b backdrop-blur-sm bg-opacity-90`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className={`w-10 h-10 rounded-lg ${darkMode ? 'bg-blue-600' : 'bg-blue-500'} flex items-center justify-center`}>
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold">Synthera</span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <button onClick={() => scrollToSection('features')} className={`hover:text-blue-500 transition-colors`}>
                Features
              </button>
              <button onClick={() => scrollToSection('testimonials')} className={`hover:text-blue-500 transition-colors`}>
                Testimonials
              </button>
              <button onClick={() => scrollToSection('contact')} className={`hover:text-blue-500 transition-colors`}>
                Contact Us
              </button>
              <button onClick={toggleDarkMode} className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'} transition-colors`}>
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <button className={`px-4 py-2 rounded-lg ${darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'} transition-colors`} onClick={pushtoSignIn}>
                Sign In
              </button>
              <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors" onClick={pushtoSignUp}>
                Sign Up
              </button>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center space-x-2">
              <button onClick={toggleDarkMode} className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className={`p-2 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className={`md:hidden ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-t`}>
            <div className="px-4 py-4 space-y-3">
              <button onClick={() => scrollToSection('features')} className="block w-full text-left py-2 hover:text-blue-500">
                Features
              </button>
              <button onClick={() => scrollToSection('testimonials')} className="block w-full text-left py-2 hover:text-blue-500">
                Testimonials
              </button>
              <button onClick={() => scrollToSection('contact')} className="block w-full text-left py-2 hover:text-blue-500">
                Contact Us
              </button>
              <button className={`block w-full text-left px-4 py-2 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                Sign In
              </button>
              <button className="block w-full text-left px-4 py-2 bg-blue-500 text-white rounded-lg" onClick={pushtoSignUp}>
                Sign Up
              </button>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className={`inline-block px-4 py-2 rounded-full ${darkMode ? 'bg-blue-900 text-blue-200' : 'bg-blue-100 text-blue-700'} text-sm font-semibold mb-6`}>
                Accelerating Pharmaceutical Innovation
              </div>
              <h1 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
                Transform Drug Discovery with{' '}
                <span className="text-blue-500">Agentic AI</span>
              </h1>
              <p className={`text-xl mb-8 ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
                Reduce research time from months to hours. Our AI-powered platform identifies repurposing opportunities, analyzes patents, and delivers actionable insights for value-added pharmaceutical products.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button className="px-8 py-4 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold text-lg transition-colors">
                  Get Started Free
                </button>
                <button className={`px-8 py-4 ${darkMode ? 'bg-gray-800 hover:bg-gray-700 border-gray-700' : 'bg-white hover:bg-gray-50 border-gray-300'} border-2 rounded-lg font-semibold text-lg transition-colors`}>
                  Watch Demo
                </button>
              </div>
            </div>
            <div className={`relative ${darkMode ? 'bg-gray-800' : 'bg-gradient-to-br from-blue-50 to-indigo-100'} rounded-2xl p-8 shadow-2xl`}>
              <div className="space-y-4">
                <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} rounded-lg p-4 shadow-lg transform hover:scale-105 transition-transform`}>
                  <div className="flex items-center space-x-3 mb-2">
                    <Search className="w-6 h-6 text-blue-500" />
                    <span className="font-semibold">Query: Find molecules for diabetes</span>
                  </div>
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Master Agent delegating to worker agents...</div>
                </div>
                <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} rounded-lg p-4 shadow-lg transform hover:scale-105 transition-transform`}>
                  <div className="flex items-center space-x-3 mb-2">
                    <TrendingUp className="w-6 h-6 text-green-500" />
                    <span className="font-semibold">Market Analysis Complete</span>
                  </div>
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>IQVIA: $45B market, 8.2% CAGR</div>
                </div>
                <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} rounded-lg p-4 shadow-lg transform hover:scale-105 transition-transform`}>
                  <div className="flex items-center space-x-3 mb-2">
                    <FileText className="w-6 h-6 text-purple-500" />
                    <span className="font-semibold">Report Generated</span>
                  </div>
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>15 viable opportunities identified</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className={`py-20 px-4 sm:px-6 lg:px-8 ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Intelligent Agent Ecosystem</h2>
            <p className={`text-xl ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
              Specialized AI agents working together to accelerate your research
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <TrendingUp className="w-8 h-8" />,
                title: 'IQVIA Insights Agent',
                description: 'Real-time market analysis with sales trends, CAGR calculations, and competitive landscape mapping'
              },
              {
                icon: <Shield className="w-8 h-8" />,
                title: 'Patent Landscape Agent',
                description: 'Comprehensive IP analysis from USPTO and global databases with FTO assessments and expiry timelines'
              },
              {
                icon: <Search className="w-8 h-8" />,
                title: 'Clinical Trials Agent',
                description: 'Pipeline intelligence from ClinicalTrials.gov with phase distribution and sponsor insights'
              },
              {
                icon: <Globe className="w-8 h-8" />,
                title: 'Web Intelligence Agent',
                description: 'Automated scanning of guidelines, publications, and patient forums with credible source verification'
              },
              {
                icon: <Zap className="w-8 h-8" />,
                title: 'EXIM Trends Agent',
                description: 'Import-export analytics for APIs and formulations across global markets'
              },
              {
                icon: <FileText className="w-8 h-8" />,
                title: 'Report Generator Agent',
                description: 'Professional PDF reports with charts, tables, and actionable recommendations'
              }
            ].map((feature, idx) => (
              <div key={idx} className={`${darkMode ? 'bg-gray-700 hover:bg-gray-650' : 'bg-white hover:shadow-xl'} rounded-xl p-6 shadow-lg transition-all duration-300 hover:-translate-y-1`}>
                <div className="text-blue-500 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Trusted by Industry Leaders</h2>
            <p className={`text-xl ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
              See how pharmaceutical companies are transforming their R&D pipelines
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                quote: "Reduced our preliminary research time by 85%. What used to take 3 months now takes just 2 weeks.",
                author: "Dr. Sarah Chen",
                role: "VP of R&D, Global Pharma Inc."
              },
              {
                quote: "The patent landscape analysis alone has saved us from costly FTO issues. Invaluable tool for strategic planning.",
                author: "Michael Rodriguez",
                role: "Chief Scientific Officer, BioTech Solutions"
              },
              {
                quote: "We've identified 12 viable repurposing opportunities in our first quarter. ROI exceeded all expectations.",
                author: "Dr. Priya Sharma",
                role: "Head of Innovation, MedGen Pharmaceuticals"
              }
            ].map((testimonial, idx) => (
              <div key={idx} className={`${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border-2 rounded-xl p-6 shadow-lg`}>
                <div className="text-yellow-500 text-2xl mb-4">★★★★★</div>
                <p className={`mb-6 italic ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>"{testimonial.quote}"</p>
                <div>
                  <div className="font-semibold">{testimonial.author}</div>
                  <div className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className={`py-20 px-4 sm:px-6 lg:px-8 ${darkMode ? 'bg-gray-800' : 'bg-gray-50'}`}>
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Get in Touch</h2>
            <p className={`text-xl ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
              Ready to accelerate your pharmaceutical innovation?
            </p>
          </div>
          <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} rounded-xl p-8 shadow-lg space-y-6`}>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold mb-2">First Name</label>
                <input type="text" className={`w-full px-4 py-3 rounded-lg ${darkMode ? 'bg-gray-600 border-gray-500' : 'bg-gray-50 border-gray-300'} border focus:ring-2 focus:ring-blue-500 outline-none transition-all`} />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-2">Last Name</label>
                <input type="text" className={`w-full px-4 py-3 rounded-lg ${darkMode ? 'bg-gray-600 border-gray-500' : 'bg-gray-50 border-gray-300'} border focus:ring-2 focus:ring-blue-500 outline-none transition-all`} />
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Email</label>
              <input type="email" className={`w-full px-4 py-3 rounded-lg ${darkMode ? 'bg-gray-600 border-gray-500' : 'bg-gray-50 border-gray-300'} border focus:ring-2 focus:ring-blue-500 outline-none transition-all`} />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Company</label>
              <input type="text" className={`w-full px-4 py-3 rounded-lg ${darkMode ? 'bg-gray-600 border-gray-500' : 'bg-gray-50 border-gray-300'} border focus:ring-2 focus:ring-blue-500 outline-none transition-all`} />
            </div>
            <div>
              <label className="block text-sm font-semibold mb-2">Message</label>
              <textarea rows={4} className={`w-full px-4 py-3 rounded-lg ${darkMode ? 'bg-gray-600 border-gray-500' : 'bg-gray-50 border-gray-300'} border focus:ring-2 focus:ring-blue-500 outline-none transition-all`}></textarea>
            </div>
            <button type="button" className="w-full px-8 py-4 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold text-lg transition-colors">
              Send Message
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className={`${darkMode ? 'bg-gray-900 border-gray-800' : 'bg-gray-900 text-white'} border-t py-12 px-4 sm:px-6 lg:px-8`}>
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Synthera</span>
          </div>
          <p className="text-gray-400 mb-4">Accelerating pharmaceutical innovation through intelligent AI agents</p>
          <p className="text-gray-500 text-sm">©️ 2025 Synthera. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  GraduationCap, 
  Smartphone, 
  MessageCircle, 
  CheckCircle, 
  Users, 
  Globe, 
  Zap,
  Github,
  ArrowRight,
  Menu,
  X
} from 'lucide-react';

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
    setIsMenuOpen(false);
  };

  const openWhatsApp = () => {
    window.open('https://wa.me/14155238886?text=start', '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <header className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrollY > 50 ? 'bg-gray-900/95 backdrop-blur-sm shadow-lg border-b border-gray-800' : 'bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-600 rounded-lg flex items-center justify-center">
                <GraduationCap className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Examinator</span>
            </div>
            
            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              <button onClick={() => scrollToSection('features')} className="text-gray-300 hover:text-green-400 transition-colors">
                Features
              </button>
              <button onClick={() => scrollToSection('how-it-works')} className="text-gray-300 hover:text-green-400 transition-colors">
                How it Works
              </button>
            </nav>

            {/* Mobile Menu Button */}
            <button 
              className="md:hidden p-2 text-white"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden bg-gray-800 border-t border-gray-700 py-4">
              <nav className="flex flex-col space-y-4">
                <button onClick={() => scrollToSection('features')} className="text-left text-gray-300 hover:text-green-400 transition-colors">
                  Features
                </button>
                <button onClick={() => scrollToSection('how-it-works')} className="text-left text-gray-300 hover:text-green-400 transition-colors">
                  How it Works
                </button>
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section with Dot Matrix Background */}
      <section className="relative pt-20 pb-16 px-4 sm:px-6 lg:px-8 bg-gray-900 overflow-hidden">
        {/* Dot Matrix Background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute inset-0" style={{
            backgroundImage: `radial-gradient(circle, #10b981 1px, transparent 1px)`,
            backgroundSize: '30px 30px',
            backgroundPosition: '0 0, 15px 15px'
          }}></div>
        </div>
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900/90 via-gray-900/95 to-gray-900/90"></div>
        
        <div className="relative max-w-7xl mx-auto">
          <div className="text-center">
            <div className="mb-6">
              <div className="inline-flex items-center px-4 py-2 rounded-full bg-gray-800/80 border border-gray-700 backdrop-blur-sm">
                <div className="flex items-center space-x-3">
                  {/* Bolt Badge */}
                  <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center border-2 border-white">
                    <span className="text-white font-bold text-sm">b</span>
                  </div>
                  <Zap className="h-4 w-4 text-green-400" />
                  <span className="text-gray-200 font-medium">Built for World's Largest Hackathon</span>
                </div>
              </div>
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
              Examinator: AI-Powered 
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-teal-400">
                Exam Prep in Your Pocket
              </span>
            </h1>
            
            <p className="text-xl sm:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Practice JAMB, SAT & NEET with real past questions - all through WhatsApp
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <button 
                onClick={openWhatsApp}
                className="group flex items-center px-8 py-4 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                <MessageCircle className="h-6 w-6 mr-2" />
                Start Practicing Now
                <ArrowRight className="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <div className="flex items-center text-gray-400">
                <span className="text-sm">No downloads • Works on any phone</span>
              </div>
            </div>

            {/* Hero Visual */}
            <div className="relative max-w-4xl mx-auto">
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl shadow-2xl p-8 sm:p-12 border border-gray-700">
                <div className="grid md:grid-cols-2 gap-8 items-center">
                  <div className="space-y-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center border border-green-500/30">
                        <Smartphone className="h-6 w-6 text-green-400" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">WhatsApp Integration</h3>
                        <p className="text-gray-400 text-sm">Works on every smartphone</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-teal-500/20 rounded-full flex items-center justify-center border border-teal-500/30">
                        <BookOpen className="h-6 w-6 text-teal-400" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">Real Past Papers</h3>
                        <p className="text-gray-400 text-sm">2015-2024 official questions</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center border border-blue-500/30">
                        <Zap className="h-6 w-6 text-blue-400" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">AI-Powered</h3>
                        <p className="text-gray-400 text-sm">RAG technology for accuracy</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="relative">
                    <div className="w-64 h-96 mx-auto bg-gray-900 rounded-[2.5rem] p-2 shadow-2xl border border-gray-700">
                      <div className="w-full h-full bg-white rounded-[2rem] overflow-hidden">
                        <div className="bg-green-500 p-4 text-white">
                          <div className="flex items-center space-x-2">
                            <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                              <GraduationCap className="h-5 w-5 text-green-500" />
                            </div>
                            <span className="font-semibold">Examinator</span>
                          </div>
                        </div>
                        <div className="p-4 space-y-3">
                          <div className="bg-gray-100 rounded-lg p-3">
                            <p className="text-sm">Hi! I'm your AI exam tutor. Which exam are you preparing for?</p>
                          </div>
                          <div className="bg-green-100 rounded-lg p-3 ml-8">
                            <p className="text-sm">JAMB Mathematics</p>
                          </div>
                          <div className="bg-gray-100 rounded-lg p-3">
                            <p className="text-sm">Great! Let's start with a 2023 past question...</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
              The Global Education Challenge
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Millions of students worldwide lack access to quality exam preparation due to cost barriers and internet limitations
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 bg-gray-900/50 rounded-xl border border-gray-700">
              <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-red-500/30">
                <Globe className="h-8 w-8 text-red-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Limited Access</h3>
              <p className="text-gray-400">
                Students in developing countries often lack reliable internet or expensive prep materials
              </p>
            </div>

            <div className="text-center p-6 bg-gray-900/50 rounded-xl border border-gray-700">
              <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-yellow-500/30">
                <Users className="h-8 w-8 text-yellow-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">High Costs</h3>
              <p className="text-gray-400">
                Quality tutoring and prep courses are expensive, excluding millions of talented students
              </p>
            </div>

            <div className="text-center p-6 bg-gray-900/50 rounded-xl border border-gray-700">
              <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-blue-500/30">
                <Smartphone className="h-8 w-8 text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Device Barriers</h3>
              <p className="text-gray-400">
                Many students only have basic phones, limiting access to modern learning apps
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-900">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
              Why Choose Examinator?
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Revolutionary AI tutoring that works on every phone, accessible to students everywhere
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 hover:border-green-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-green-500/10">
              <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-4 border border-green-500/30">
                <MessageCircle className="h-6 w-6 text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">WhatsApp Native</h3>
              <p className="text-gray-400">
                No app downloads required. Works on every smartphone with WhatsApp - from iPhone to basic Android
              </p>
            </div>

            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 hover:border-teal-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-teal-500/10">
              <div className="w-12 h-12 bg-teal-500/20 rounded-lg flex items-center justify-center mb-4 border border-teal-500/30">
                <BookOpen className="h-6 w-6 text-teal-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Real Past Papers</h3>
              <p className="text-gray-400">
                Practice with official 2015-2024 past questions from JAMB, SAT, and NEET examinations
              </p>
            </div>

            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 hover:border-blue-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10">
              <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4 border border-blue-500/30">
                <Zap className="h-6 w-6 text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">RAG-Powered AI</h3>
              <p className="text-gray-400">
                Advanced AI with Retrieval-Augmented Generation ensures accurate, contextual answers
              </p>
            </div>

            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/10">
              <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4 border border-purple-500/30">
                <GraduationCap className="h-6 w-6 text-purple-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Personalized Tutoring</h3>
              <p className="text-gray-400">
                AI adapts to your learning style and focuses on areas where you need improvement
              </p>
            </div>

            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 hover:border-orange-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-orange-500/10">
              <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center mb-4 border border-orange-500/30">
                <Globe className="h-6 w-6 text-orange-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Global Accessibility</h3>
              <p className="text-gray-400">
                Works with minimal internet connection, making quality education accessible worldwide
              </p>
            </div>

            <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700 hover:border-pink-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-pink-500/10">
              <div className="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4 border border-pink-500/30">
                <CheckCircle className="h-6 w-6 text-pink-400" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">Zero Barriers</h3>
              <p className="text-gray-400">
                No registration, no subscriptions, no hidden costs. Just start chatting and learning
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-800">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
              How It Works
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Getting started is as simple as sending a WhatsApp message
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white font-bold text-2xl shadow-lg">
                1
              </div>
              <h3 className="text-xl font-semibold text-white mb-4">Send a Message</h3>
              <p className="text-gray-400">
                Click our WhatsApp button and send "start" to begin your exam prep journey
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-teal-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white font-bold text-2xl shadow-lg">
                2
              </div>
              <h3 className="text-xl font-semibold text-white mb-4">Choose Your Exam</h3>
              <p className="text-gray-400">
                Select from JAMB, SAT, or NEET and specify your subject preferences
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-6 text-white font-bold text-2xl shadow-lg">
                3
              </div>
              <h3 className="text-xl font-semibold text-white mb-4">Start Learning</h3>
              <p className="text-gray-400">
                Receive personalized questions, explanations, and track your progress
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-green-600 to-teal-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to Ace Your Exams?
          </h2>
          <p className="text-xl text-green-100 mb-8 max-w-2xl mx-auto">
            Join thousands of students worldwide who are already improving their scores with AI-powered exam prep
          </p>
          
          <button 
            onClick={openWhatsApp}
            className="group inline-flex items-center px-8 py-4 bg-white hover:bg-gray-100 text-green-600 font-semibold rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl text-lg"
          >
            <MessageCircle className="h-6 w-6 mr-2" />
            Start Practicing Now - It's Free!
            <ArrowRight className="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" />
          </button>
          
          <p className="text-green-100 mt-4 text-sm">
            No registration required • Works on any phone • Start immediately
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4 sm:px-6 lg:px-8 border-t border-gray-800">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-600 rounded-lg flex items-center justify-center">
                  <GraduationCap className="h-6 w-6 text-white" />
                </div>
                <span className="text-xl font-bold">Examinator</span>
              </div>
              <p className="text-gray-400 mb-4 max-w-md">
                Democratizing education through AI-powered exam preparation accessible via WhatsApp. 
                Built for students worldwide, especially those in developing countries.
              </p>
              <div className="flex space-x-4">
                <a 
                  href="https://github.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Github className="h-6 w-6" />
                </a>
                <button 
                  onClick={openWhatsApp}
                  className="text-gray-400 hover:text-green-400 transition-colors"
                >
                  <MessageCircle className="h-6 w-6" />
                </button>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Exams Supported</h3>
              <ul className="space-y-2 text-gray-400">
                <li>JAMB (Joint Admissions)</li>
                <li>SAT (Scholastic Assessment)</li>
                <li>NEET (Medical Entrance)</li>
                <li>More coming soon...</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Quick Start</h3>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <button onClick={openWhatsApp} className="hover:text-white transition-colors">
                    Start on WhatsApp
                  </button>
                </li>
                <li>No downloads needed</li>
                <li>Works on any phone</li>
                <li>Available 24/7</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Examinator. Built with ❤️ for the World's Largest Hackathon.</p>
            <p className="mt-2">Empowering students worldwide through accessible AI education.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import HomePage from './pages/HomePage'
import TestingPage from './pages/TestingPage'
import DocumentationPage from './pages/DocumentationPage'
import StatusPage from './pages/StatusPage'

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-secondary-50 via-white to-primary-50">
      <Navbar />
      
      <motion.main 
        className="flex-1"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/testing" element={<TestingPage />} />
          <Route path="/docs" element={<DocumentationPage />} />
          <Route path="/status" element={<StatusPage />} />
        </Routes>
      </motion.main>
      
      <Footer />
    </div>
  )
}

export default App
import React from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Bot, ArrowRight, Sparkles, Twitter } from 'lucide-react'

const HeroSection: React.FC = () => {
  return (
    <section className="relative py-20 lg:py-32 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-secondary-50" />
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" />
        <div className="absolute top-40 right-10 w-72 h-72 bg-secondary-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-primary-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center px-4 py-2 rounded-full bg-primary-100 text-primary-700 text-sm font-medium mb-8"
          >
            <Sparkles className="h-4 w-4 mr-2" />
            Built for the Bolt Hackathon
          </motion.div>

          {/* Main Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl md:text-6xl lg:text-7xl font-bold text-secondary-900 mb-6"
          >
            Convert Betting Codes
            <span className="block text-gradient">Instantly on X</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl md:text-2xl text-secondary-600 mb-12 max-w-4xl mx-auto leading-relaxed"
          >
            FlexCode Bot converts betting codes between platforms like Stake, SportyBet, 
            Bet9ja, and more via X mentions and DMs using advanced NLP and AI.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
          >
            <a
              href="https://twitter.com/FlexCodeBot"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary px-8 py-4 text-lg font-semibold shadow-glow"
            >
              <Twitter className="h-5 w-5 mr-2" />
              Try @FlexCodeBot Now
            </a>
            <Link
              to="/testing"
              className="btn-secondary px-8 py-4 text-lg font-semibold"
            >
              Test the API
              <ArrowRight className="h-5 w-5 ml-2" />
            </Link>
          </motion.div>

          {/* Demo Preview */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="relative max-w-4xl mx-auto"
          >
            <div className="bg-white rounded-2xl shadow-2xl border border-secondary-200 overflow-hidden">
              <div className="bg-secondary-900 px-6 py-4 flex items-center space-x-3">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-error-500 rounded-full" />
                  <div className="w-3 h-3 bg-warning-500 rounded-full" />
                  <div className="w-3 h-3 bg-success-500 rounded-full" />
                </div>
                <span className="text-secondary-400 text-sm font-mono">X (Twitter)</span>
              </div>
              <div className="p-8">
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                      <span className="text-primary-600 font-semibold text-sm">U</span>
                    </div>
                    <div className="flex-1">
                      <div className="bg-secondary-100 rounded-2xl px-4 py-3">
                        <p className="text-secondary-800">
                          @FlexCodeBot Convert Stake code ABC123 to SportyBet and Bet9ja code XYZ789 to 1xBet
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-gradient-primary rounded-full flex items-center justify-center">
                      <Bot className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="bg-primary-100 rounded-2xl px-4 py-3">
                        <p className="text-primary-800">
                          @User Converted codes: Stake ABC123 to SportyBet: DEF456; Bet9ja XYZ789 to 1xBet: GHI789
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

export default HeroSection
import React from 'react'
import { Bot, Heart, Code } from 'lucide-react'

const Footer: React.FC = () => {
  return (
    <footer className="bg-secondary-900 text-secondary-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="p-2 bg-gradient-primary rounded-lg">
                <Bot className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">FlexCode Bot</span>
            </div>
            <p className="text-secondary-400 mb-4 max-w-md">
              Convert betting codes between platforms like Stake, SportyBet, Bet9ja, and more 
              via X (Twitter) mentions and DMs. Built for the Bolt hackathon.
            </p>
            <div className="flex items-center space-x-1 text-sm">
              <span>Made with</span>
              <Heart className="h-4 w-4 text-error-500" />
              <span>for the</span>
              <Code className="h-4 w-4 text-primary-400" />
              <span>Bolt Hackathon</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a href="/testing" className="hover:text-primary-400 transition-colors duration-200">
                  Test Bot
                </a>
              </li>
              <li>
                <a href="/docs" className="hover:text-primary-400 transition-colors duration-200">
                  Documentation
                </a>
              </li>
              <li>
                <a href="/status" className="hover:text-primary-400 transition-colors duration-200">
                  Bot Status
                </a>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a 
                  href="https://github.com/yourusername/flexcode" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="hover:text-primary-400 transition-colors duration-200"
                >
                  GitHub Repository
                </a>
              </li>
              <li>
                <a 
                  href="https://twitter.com/FlexCodeBot" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="hover:text-primary-400 transition-colors duration-200"
                >
                  @FlexCodeBot
                </a>
              </li>
              <li>
                <a 
                  href="https://convertbetcodes.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="hover:text-primary-400 transition-colors duration-200"
                >
                  ConvertBetCodes API
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-secondary-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-secondary-400 text-sm">
            © 2025 FlexCode Bot. Built with FastAPI, React, and Hugging Face.
          </p>
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <span className="text-secondary-500 text-sm">Powered by</span>
            <div className="flex items-center space-x-3">
              <span className="text-xs bg-secondary-800 px-2 py-1 rounded">FastAPI</span>
              <span className="text-xs bg-secondary-800 px-2 py-1 rounded">React</span>
              <span className="text-xs bg-secondary-800 px-2 py-1 rounded">Hugging Face</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
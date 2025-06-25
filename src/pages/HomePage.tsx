import React from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  Bot, 
  MessageCircle, 
  Zap, 
  Shield, 
  ArrowRight, 
  Twitter,
  Code,
  Cpu,
  Globe
} from 'lucide-react'
import HeroSection from '../components/home/HeroSection'
import FeaturesSection from '../components/home/FeaturesSection'
import HowItWorksSection from '../components/home/HowItWorksSection'
import PlatformsSection from '../components/home/PlatformsSection'

const HomePage: React.FC = () => {
  return (
    <div className="space-y-0">
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
      <PlatformsSection />
      
      {/* CTA Section */}
      <section className="py-20 bg-gradient-primary">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Convert Your Betting Codes?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Start using FlexCode Bot today. Mention @FlexCodeBot on X or send a DM 
              to convert your betting codes instantly.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://twitter.com/FlexCodeBot"
                target="_blank"
                rel="noopener noreferrer"
                className="btn bg-white text-primary-600 hover:bg-primary-50 font-semibold px-8 py-3 text-lg"
              >
                <Twitter className="h-5 w-5 mr-2" />
                Follow @FlexCodeBot
              </a>
              <Link
                to="/testing"
                className="btn bg-primary-800 text-white hover:bg-primary-900 font-semibold px-8 py-3 text-lg border border-primary-700"
              >
                Test the Bot
                <ArrowRight className="h-5 w-5 ml-2" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
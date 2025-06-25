import React from 'react'
import { motion } from 'framer-motion'
import { 
  Zap, 
  MessageCircle, 
  Shield, 
  Bot, 
  Globe, 
  Code,
  Cpu,
  Twitter
} from 'lucide-react'

const features = [
  {
    icon: Zap,
    title: 'Instant Conversion',
    description: 'Convert betting codes between platforms in seconds using advanced AI and NLP processing.',
    color: 'text-warning-600',
    bgColor: 'bg-warning-100',
  },
  {
    icon: MessageCircle,
    title: 'X Integration',
    description: 'Works seamlessly with X (Twitter) mentions and direct messages for easy access.',
    color: 'text-primary-600',
    bgColor: 'bg-primary-100',
  },
  {
    icon: Bot,
    title: 'Smart NLP',
    description: 'Uses Hugging Face BERT models to extract multiple codes and platforms from natural language.',
    color: 'text-success-600',
    bgColor: 'bg-success-100',
  },
  {
    icon: Shield,
    title: 'Reliable & Secure',
    description: 'Built with enterprise-grade security and error handling for consistent performance.',
    color: 'text-error-600',
    bgColor: 'bg-error-100',
  },
  {
    icon: Globe,
    title: 'Multi-Platform',
    description: 'Supports 10+ betting platforms including Stake, SportyBet, Bet9ja, 1xBet, and more.',
    color: 'text-secondary-600',
    bgColor: 'bg-secondary-100',
  },
  {
    icon: Code,
    title: 'Developer Friendly',
    description: 'Clean FastAPI backend with comprehensive documentation and testing endpoints.',
    color: 'text-primary-600',
    bgColor: 'bg-primary-100',
  },
]

const FeaturesSection: React.FC = () => {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-3xl md:text-4xl font-bold text-secondary-900 mb-4"
          >
            Powerful Features for Seamless Conversion
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="text-xl text-secondary-600 max-w-3xl mx-auto"
          >
            FlexCode Bot combines cutting-edge AI, robust APIs, and seamless social media integration 
            to deliver the best betting code conversion experience.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="card group hover:shadow-lg transition-all duration-300"
            >
              <div className={`inline-flex p-3 rounded-lg ${feature.bgColor} mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className={`h-6 w-6 ${feature.color}`} />
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-secondary-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default FeaturesSection
import React from 'react'
import { motion } from 'framer-motion'
import { 
  MessageSquare, 
  Brain, 
  RefreshCw, 
  CheckCircle,
  ArrowRight
} from 'lucide-react'

const steps = [
  {
    icon: MessageSquare,
    title: 'Mention or DM',
    description: 'Send a message to @FlexCodeBot on X with your betting codes and target platforms.',
    example: '@FlexCodeBot Convert Stake ABC123 to SportyBet',
    color: 'text-primary-600',
    bgColor: 'bg-primary-100',
  },
  {
    icon: Brain,
    title: 'AI Processing',
    description: 'Our NLP model extracts codes, platforms, and conversion instructions from your message.',
    example: 'Code: ABC123, From: Stake, To: SportyBet',
    color: 'text-success-600',
    bgColor: 'bg-success-100',
  },
  {
    icon: RefreshCw,
    title: 'Code Conversion',
    description: 'The bot converts your codes using the ConvertBetCodes API with real-time processing.',
    example: 'ABC123 → DEF456 (SportyBet format)',
    color: 'text-warning-600',
    bgColor: 'bg-warning-100',
  },
  {
    icon: CheckCircle,
    title: 'Instant Reply',
    description: 'Receive converted codes instantly via reply or DM with detailed conversion information.',
    example: 'Converted: Stake ABC123 to SportyBet: DEF456',
    color: 'text-error-600',
    bgColor: 'bg-error-100',
  },
]

const HowItWorksSection: React.FC = () => {
  return (
    <section className="py-20 bg-secondary-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-3xl md:text-4xl font-bold text-secondary-900 mb-4"
          >
            How FlexCode Bot Works
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="text-xl text-secondary-600 max-w-3xl mx-auto"
          >
            Converting betting codes is as simple as sending a message. 
            Our AI-powered bot handles the rest automatically.
          </motion.p>
        </div>

        <div className="relative">
          {/* Connection Lines */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-primary-200 via-success-200 via-warning-200 to-error-200 transform -translate-y-1/2" />
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="relative"
              >
                <div className="card text-center group hover:shadow-lg transition-all duration-300">
                  {/* Step Number */}
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 w-8 h-8 bg-white border-2 border-secondary-200 rounded-full flex items-center justify-center text-sm font-semibold text-secondary-600 group-hover:border-primary-300 transition-colors duration-300">
                    {index + 1}
                  </div>
                  
                  <div className={`inline-flex p-4 rounded-xl ${step.bgColor} mb-4 mt-4 group-hover:scale-110 transition-transform duration-300`}>
                    <step.icon className={`h-8 w-8 ${step.color}`} />
                  </div>
                  
                  <h3 className="text-xl font-semibold text-secondary-900 mb-3">
                    {step.title}
                  </h3>
                  
                  <p className="text-secondary-600 mb-4 leading-relaxed">
                    {step.description}
                  </p>
                  
                  <div className="bg-secondary-100 rounded-lg p-3">
                    <code className="text-sm text-secondary-700 font-mono">
                      {step.example}
                    </code>
                  </div>
                </div>
                
                {/* Arrow for desktop */}
                {index < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                    <ArrowRight className="h-6 w-6 text-secondary-400" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default HowItWorksSection
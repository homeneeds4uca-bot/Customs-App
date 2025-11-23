import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="border-b border-navy-100">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-navy-900 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">CC</span>
            </div>
            <span className="font-display text-xl text-navy-900">CustomsCompass</span>
          </div>
          <div className="flex items-center space-x-6">
            <Link href="#features" className="text-navy-700 hover:text-navy-900 transition">
              Features
            </Link>
            <Link href="#pricing" className="text-navy-700 hover:text-navy-900 transition">
              Pricing
            </Link>
            <Link href="#faq" className="text-navy-700 hover:text-navy-900 transition">
              FAQ
            </Link>
            <Link href="/auth/login" className="text-navy-700 hover:text-navy-900 transition">
              Log In
            </Link>
            <Link
              href="/auth/signup"
              className="bg-navy-900 text-white px-4 py-2 rounded-lg hover:bg-navy-800 transition"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="font-display text-5xl md:text-6xl text-navy-900 mb-6">
          Customs compliance in 3 clicks.<br />Not 3 weeks.
        </h1>
        <p className="text-xl text-navy-600 mb-8 max-w-2xl mx-auto">
          AI-powered HS code classification, duty calculator, and document generation
          for Canadian SMB importers. CARM-compliant and ready for 2024.
        </p>
        <div className="flex justify-center space-x-4 mb-12">
          <Link
            href="/auth/signup"
            className="bg-gold-500 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gold-600 transition"
          >
            Start Free Trial
          </Link>
          <Link
            href="#demo"
            className="border-2 border-navy-900 text-navy-900 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-navy-50 transition"
          >
            Watch Demo
          </Link>
        </div>

        {/* Trust Badges */}
        <div className="flex justify-center items-center space-x-8 text-sm text-navy-600">
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>Canadian Data Residency</span>
          </div>
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span>PIPEDA Compliant</span>
          </div>
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
            </svg>
            <span>Bank-Grade Encryption</span>
          </div>
        </div>
      </section>

      {/* Problem/Solution Comparison */}
      <section className="bg-navy-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-4xl text-navy-900 text-center mb-12">
            Stop losing time and money on customs
          </h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-8 rounded-lg border-2 border-red-200">
              <h3 className="font-display text-2xl text-navy-900 mb-4">Before CustomsCompass</h3>
              <ul className="space-y-3 text-navy-700">
                <li className="flex items-start">
                  <span className="text-red-500 mr-2">✗</span>
                  <span>3-4 hours per product classification</span>
                </li>
                <li className="flex items-start">
                  <span className="text-red-500 mr-2">✗</span>
                  <span>$150-250 per broker entry</span>
                </li>
                <li className="flex items-start">
                  <span className="text-red-500 mr-2">✗</span>
                  <span>2-3 day document turnaround</span>
                </li>
                <li className="flex items-start">
                  <span className="text-red-500 mr-2">✗</span>
                  <span>No visibility into costs until shipment arrives</span>
                </li>
                <li className="flex items-start">
                  <span className="text-red-500 mr-2">✗</span>
                  <span>15-25% error rate causing delays</span>
                </li>
              </ul>
            </div>

            <div className="bg-gold-50 p-8 rounded-lg border-2 border-gold-400">
              <h3 className="font-display text-2xl text-navy-900 mb-4">After CustomsCompass</h3>
              <ul className="space-y-3 text-navy-700">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>30 seconds AI classification</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>$199/month unlimited classifications</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>5 minutes document generation</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Real-time landed cost calculation</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>92%+ AI accuracy with validation</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Critical Liability Notice */}
      <section className="bg-yellow-50 border-y-2 border-yellow-400 py-12">
        <div className="container mx-auto px-4 max-w-4xl">
          <div className="flex items-start space-x-4">
            <svg className="w-8 h-8 text-yellow-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <h3 className="font-display text-2xl text-navy-900 mb-3">
                IMPORTANT - IMPORTER LIABILITY NOTICE
              </h3>
              <div className="text-navy-700 space-y-3">
                <p>
                  Per CBSA D-Memorandum D17-2-5 and Section 32 of the Customs Act:
                </p>
                <blockquote className="border-l-4 border-yellow-500 pl-4 italic">
                  "The importer is ultimately responsible for the accounting documentation, payment of duties
                  and taxes, and subsequent corrections such as re-determination of classification, origin and
                  valuation - <strong>even if using the services of a customs broker or software platform.</strong>"
                </blockquote>
                <p>
                  <strong>This platform provides classification guidance and calculation tools - NOT official
                  customs rulings.</strong> You accept full liability for all customs declarations. For binding
                  rulings, contact CBSA directly.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-4xl text-navy-900 text-center mb-12">
            Everything you need for customs compliance
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white p-6 rounded-lg border border-navy-200">
              <div className="w-12 h-12 bg-gold-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-navy-900 mb-2">AI Classification</h3>
              <p className="text-navy-600">
                92%+ accuracy on 6-digit HS codes using fine-tuned models trained on CBSA rulings
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-navy-200">
              <div className="w-12 h-12 bg-gold-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-navy-900 mb-2">Duty Calculator</h3>
              <p className="text-navy-600">
                Real-time landed cost calculation with USMCA/CPTPP/CETA rates and provincial taxes
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg border border-navy-200">
              <div className="w-12 h-12 bg-gold-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-gold-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="font-display text-xl text-navy-900 mb-2">Document Generation</h3>
              <p className="text-navy-600">
                CBSA-compliant commercial invoices, packing lists, and certificates of origin
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="bg-navy-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-4xl text-navy-900 text-center mb-12">
            Simple, transparent pricing
          </h2>
          <div className="grid md:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {/* Free Tier */}
            <div className="bg-white p-6 rounded-lg border-2 border-navy-200">
              <h3 className="font-display text-2xl text-navy-900 mb-2">Free</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-navy-900">$0</span>
                <span className="text-navy-600">/month</span>
              </div>
              <ul className="space-y-2 text-sm text-navy-700 mb-6">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>25 classifications/month</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Basic calculator</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>View-only documents</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full text-center bg-navy-100 text-navy-900 px-4 py-2 rounded-lg hover:bg-navy-200 transition"
              >
                Get Started
              </Link>
            </div>

            {/* Starter Tier */}
            <div className="bg-white p-6 rounded-lg border-2 border-gold-400 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-gold-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
                POPULAR
              </div>
              <h3 className="font-display text-2xl text-navy-900 mb-2">Starter</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-navy-900">$199</span>
                <span className="text-navy-600">/month</span>
              </div>
              <ul className="space-y-2 text-sm text-navy-700 mb-6">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>500 classifications/month</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Full document generation</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Bulk import (100 products)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Email support</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full text-center bg-gold-500 text-white px-4 py-2 rounded-lg hover:bg-gold-600 transition"
              >
                Start Free Trial
              </Link>
            </div>

            {/* Growth Tier */}
            <div className="bg-white p-6 rounded-lg border-2 border-navy-200">
              <h3 className="font-display text-2xl text-navy-900 mb-2">Growth</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-navy-900">$499</span>
                <span className="text-navy-600">/month</span>
              </div>
              <ul className="space-y-2 text-sm text-navy-700 mb-6">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Unlimited classifications</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>API access (1K calls/mo)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Priority support</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Audit trail export</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full text-center bg-navy-900 text-white px-4 py-2 rounded-lg hover:bg-navy-800 transition"
              >
                Start Free Trial
              </Link>
            </div>

            {/* Professional Tier */}
            <div className="bg-white p-6 rounded-lg border-2 border-navy-200">
              <h3 className="font-display text-2xl text-navy-900 mb-2">Professional</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-navy-900">$999</span>
                <span className="text-navy-600">/month</span>
              </div>
              <ul className="space-y-2 text-sm text-navy-700 mb-6">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Everything in Growth</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>API (10K calls/mo)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>White-label option</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span>Dedicated CSM</span>
                </li>
              </ul>
              <Link
                href="/auth/signup"
                className="block w-full text-center bg-navy-900 text-white px-4 py-2 rounded-lg hover:bg-navy-800 transition"
              >
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="font-display text-4xl text-navy-900 mb-6">
            Ready to simplify your customs process?
          </h2>
          <p className="text-xl text-navy-600 mb-8 max-w-2xl mx-auto">
            Join Canadian importers who are saving time and money with CustomsCompass
          </p>
          <Link
            href="/auth/signup"
            className="inline-block bg-gold-500 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gold-600 transition"
          >
            Start Your Free Trial
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-navy-100 py-12 bg-navy-50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-navy-900 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">CC</span>
                </div>
                <span className="font-display text-xl text-navy-900">CustomsCompass</span>
              </div>
              <p className="text-sm text-navy-600">
                Making customs compliance invisible for SMB importers
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-navy-900 mb-3">Product</h4>
              <ul className="space-y-2 text-sm text-navy-600">
                <li><Link href="#features">Features</Link></li>
                <li><Link href="#pricing">Pricing</Link></li>
                <li><Link href="/docs">Documentation</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-navy-900 mb-3">Company</h4>
              <ul className="space-y-2 text-sm text-navy-600">
                <li><Link href="/about">About</Link></li>
                <li><Link href="/contact">Contact</Link></li>
                <li><Link href="/privacy">Privacy Policy</Link></li>
                <li><Link href="/terms">Terms of Service</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-navy-900 mb-3">Legal</h4>
              <ul className="space-y-2 text-sm text-navy-600">
                <li><Link href="/liability">Liability Notice</Link></li>
                <li><Link href="/compliance">Compliance Guide</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-navy-200 mt-8 pt-8 text-center text-sm text-navy-600">
            <p>&copy; 2024 CustomsCompass. All rights reserved. Made in Canada 🇨🇦</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

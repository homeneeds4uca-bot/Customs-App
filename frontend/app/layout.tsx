import type { Metadata } from 'next'
import { DM_Serif_Display, Source_Sans_3, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const dmSerif = DM_Serif_Display({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
})

const sourceSans = Source_Sans_3({
  subsets: ['latin'],
  variable: '--font-body',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'CustomsCompass - Canadian Customs Compliance Made Simple',
  description: 'AI-powered HS code classification, duty calculator, and document generation for Canadian importers. CARM-compliant customs automation.',
  keywords: 'customs, CARM, HS code, duty calculator, Canadian imports, customs compliance',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${dmSerif.variable} ${sourceSans.variable} ${jetbrainsMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}

import type { Metadata, Viewport } from 'next';
import { Plus_Jakarta_Sans, JetBrains_Mono } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import LogoIntro from '@/components/LogoIntro';

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  weight: ['400', '500', '600', '700', '800'],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
  weight: ['400', '500', '600'],
});

export const viewport: Viewport = {
  themeColor: '#0d9488',
  width: 'device-width',
  initialScale: 1,
};

export const metadata: Metadata = {
  title: 'MEDSURE — Know the Fair Price. Verify Every Bill.',
  description: 'AI-Powered Healthcare Cost Transparency, Medical Bill Auditing & Fair-Price Estimation Platform for patients and caregivers.',
  keywords: ['medical bill audit', 'healthcare transparency', 'hospital charges', 'CGHS tariff', 'NABH rates', 'medical dispute'],
  authors: [{ name: 'MEDSURE Healthcare Intelligence' }],
};


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${plusJakarta.variable} ${jetbrainsMono.variable} scroll-smooth`}>
      <body className="min-h-screen flex flex-col bg-slate-50/70 text-slate-900 font-sans antialiased selection:bg-teal-500 selection:text-white">
        <LogoIntro />
        <Navbar />
        <main className="flex-1 relative z-10 w-full">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}


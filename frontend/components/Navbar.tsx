'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Shield, 
  Stethoscope, 
  FileText, 
  Database, 
  Sparkles, 
  LayoutDashboard, 
  Menu, 
  X,
  ArrowRight,
  Activity,
  CheckCircle2
} from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: '/', label: 'Overview', icon: Activity },
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/triage', label: 'Fair Price Estimator', icon: Stethoscope },
    { href: '/bills/upload', label: 'Audit Medical Bill', icon: FileText },
    { href: '/reference-rates', label: 'Tariff Benchmarks', icon: Database },
  ];

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/85 border-b border-slate-200/80 shadow-xs transition-all w-full">
      <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 2xl:px-20">
        <div className="flex items-center justify-between h-18">
          {/* Brand Logo & Live Engine Status */}
          <Link href="/" className="flex items-center gap-3.5 group shrink-0">
            <div className="relative">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-teal-500 via-teal-600 to-emerald-700 flex items-center justify-center text-white shadow-md shadow-teal-700/25 group-hover:scale-105 group-hover:shadow-teal-700/40 transition-all duration-300">
                <Shield className="w-6 h-6 stroke-[2.3]" />
              </div>
              <span className="absolute -top-0.5 -right-0.5 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500 border-2 border-white"></span>
              </span>
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="text-xl font-extrabold tracking-tight text-slate-950 font-sans group-hover:text-teal-700 transition-colors">
                  MEDSURE
                </span>
                <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-teal-50 text-teal-700 border border-teal-200/80">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-500"></span>
                  Rules A–E
                </span>
              </div>
              <p className="text-[11px] font-medium text-slate-500 tracking-tight leading-none">
                Know the Fair Price • Verify Every Bill
              </p>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center gap-1.5">
            {navLinks.map((link) => {
              const isActive = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
              const Icon = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                    isActive
                      ? 'bg-teal-50/80 text-teal-800 font-bold border border-teal-200/80 shadow-xs'
                      : 'text-slate-600 hover:text-slate-950 hover:bg-slate-100/70'
                  }`}
                >
                  {Icon && <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-teal-600' : 'text-slate-400'}`} />}
                  {link.label}
                </Link>
              );
            })}
          </nav>

          {/* Desktop Right Action Area */}
          <div className="hidden sm:flex items-center gap-3">
            <Link
              href="/demo"
              className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold text-amber-900 bg-amber-50 hover:bg-amber-100/90 border border-amber-200/80 shadow-xs hover:border-amber-300 transition-all"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-600" />
              <span>Interactive Demo</span>
            </Link>

            <Link
              href="/bills/upload"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 shadow-md shadow-teal-600/20 hover:shadow-teal-600/35 hover:-translate-y-0.5 transition-all"
            >
              <span>Audit Bill</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex lg:hidden items-center gap-2">
            <Link
              href="/demo"
              className="sm:hidden inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-bold text-amber-900 bg-amber-50 border border-amber-200"
            >
              <Sparkles className="w-3 h-3 text-amber-600" />
              <span>Demo</span>
            </Link>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-slate-700 hover:text-slate-950 hover:bg-slate-100 border border-slate-200 transition"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-slate-200/80 bg-white/95 backdrop-blur-xl px-4 pt-3 pb-6 space-y-2 shadow-lg animate-in slide-in-from-top duration-200">
          <div className="space-y-1">
            {navLinks.map((link) => {
              const isActive = pathname === link.href || (link.href !== '/' && pathname.startsWith(link.href));
              const Icon = link.icon;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-semibold transition ${
                    isActive
                      ? 'bg-teal-50 text-teal-800 font-bold border border-teal-200'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    {Icon && <Icon className={`w-4 h-4 ${isActive ? 'text-teal-600' : 'text-slate-400'}`} />}
                    <span>{link.label}</span>
                  </div>
                  {isActive && <CheckCircle2 className="w-4 h-4 text-teal-600" />}
                </Link>
              );
            })}
          </div>

          <div className="pt-3 border-t border-slate-100 flex flex-col gap-2">
            <Link
              href="/bills/upload"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-teal-600 to-emerald-600 shadow-sm"
            >
              <FileText className="w-4 h-4" />
              <span>Audit Medical Bill</span>
            </Link>

            <Link
              href="/demo"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl text-sm font-bold text-amber-900 bg-amber-50 border border-amber-200"
            >
              <Sparkles className="w-4 h-4 text-amber-600" />
              <span>2-Minute Demo Walkthrough</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}

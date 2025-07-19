import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const navLinks = [
  { label: 'Documentation', href: '#' },
  { label: 'Resources', href: '#' },
  { label: 'Request Preview', href: '#' },
  { label: 'Pricing', href: '#' },
];

export const Header: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="w-full bg-white border-b border-gray-100 sticky top-0 z-30">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-4 py-3 md:py-4">
        {/* Logo */}
        <a href="#" className="font-bold text-2xl text-primary-600 font-sans tracking-tight">Finda</a>
        {/* Desktop Navigation */}
        <nav className="hidden md:flex gap-6 ml-8">
          {navLinks.map(link => (
            <a
              key={link.label}
              href={link.href}
              className="text-gray-900 hover:text-primary-600 font-medium transition-colors"
            >
              {link.label}
            </a>
          ))}
        </nav>
        {/* CTA Buttons */}
        <div className="hidden md:flex gap-3 ml-auto">
          <a
            href="#"
            className="px-5 py-2 rounded-full border border-primary-500 text-primary-600 font-semibold hover:bg-primary-50 transition-colors"
          >
            Contact Sales
          </a>
          <a
            href="#"
            className="px-5 py-2 rounded-full bg-primary-500 text-white font-semibold hover:bg-primary-600 transition-colors"
          >
            Dashboard
          </a>
        </div>
        {/* Mobile Menu Toggle */}
        <button
          className="md:hidden flex items-center justify-center p-2 rounded-full hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
          aria-label="Open menu"
          onClick={() => setMobileOpen(v => !v)}
        >
          <Menu size={28} />
        </button>
      </div>
      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="md:hidden absolute left-0 right-0 bg-white shadow-lg border-b border-gray-100 z-20"
          >
            <nav className="flex flex-col gap-2 px-4 py-4">
              {navLinks.map(link => (
                <a
                  key={link.label}
                  href={link.href}
                  className="text-gray-900 hover:text-primary-600 font-medium py-2 px-2 rounded transition-colors"
                  onClick={() => setMobileOpen(false)}
                >
                  {link.label}
                </a>
              ))}
              <a
                href="#"
                className="mt-2 px-5 py-2 rounded-full border border-primary-500 text-primary-600 font-semibold hover:bg-primary-50 transition-colors"
                onClick={() => setMobileOpen(false)}
              >
                Contact Sales
              </a>
              <a
                href="#"
                className="mt-2 px-5 py-2 rounded-full bg-primary-500 text-white font-semibold hover:bg-primary-600 transition-colors"
                onClick={() => setMobileOpen(false)}
              >
                Dashboard
              </a>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}; 
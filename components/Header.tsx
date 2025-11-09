import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { NAV_LINKS } from '../constants';
import { Rocket, Menu, X } from 'lucide-react';

const Header: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleFeaturesClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    setIsOpen(false);
    if (location.pathname !== '/') {
      navigate('/');
      setTimeout(() => {
        document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const renderNavLink = (link: { name: string; path: string }, isMobile: boolean = false) => {
    const className = isMobile
      ? "text-gray-700 hover:bg-teal-50 hover:text-teal-700 block px-3 py-2 rounded-md text-base font-medium transition-colors"
      : "text-gray-700 hover:text-teal-700 px-3 py-2 rounded-md text-sm font-medium transition-colors";

    if (link.path.includes('#')) {
      return (
        <a key={link.name} href="#features" onClick={handleFeaturesClick} className={className}>
          {link.name}
        </a>
      );
    }
    return (
      <Link key={link.name} to={link.path} onClick={() => setIsOpen(false)} className={className}>
        {link.name}
      </Link>
    );
  };

  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-teal-100 via-teal-50 to-white backdrop-blur-md shadow-sm border-b border-teal-100">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <a
              href="#/"
              onClick={(e) => {
                e.preventDefault();
                navigate('/');
              }}
              className="flex items-center space-x-2 text-2xl font-bold text-teal-700"
            >
              <Rocket className="w-8 h-8 text-teal-500" />
              <span>BizPilot</span>
            </a>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {NAV_LINKS.map((link) => renderNavLink(link))}
            </div>
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => navigate('/auth')}
                className="text-gray-700 hover:bg-teal-100 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Log In
              </button>
              <button
                onClick={() => navigate('/auth')}
                className="bg-teal-500 hover:bg-teal-600 text-white px-4 py-2 rounded-md text-sm font-semibold transition-all duration-300 shadow-sm"
              >
                Sign Up
              </button>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              type="button"
              className="bg-teal-100 inline-flex items-center justify-center p-2 rounded-md text-teal-700 hover:bg-teal-200 focus:outline-none transition-all duration-300"
            >
              {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && (
        <div className="md:hidden bg-gradient-to-b from-teal-50 to-white border-t border-teal-100 shadow-lg">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {NAV_LINKS.map((link) => renderNavLink(link, true))}
          </div>
          <div className="pt-4 pb-3 border-t border-teal-100">
            <div className="flex flex-col px-5 space-y-2">
              <button
                onClick={() => {
                  navigate('/auth');
                  setIsOpen(false);
                }}
                className="w-full text-left text-gray-700 hover:bg-teal-100 block px-3 py-2 rounded-md text-base font-medium"
              >
                Log In
              </button>
              <button
                onClick={() => {
                  navigate('/auth');
                  setIsOpen(false);
                }}
                className="w-full text-left bg-teal-500 text-white hover:bg-teal-600 block px-3 py-2 rounded-md text-base font-semibold shadow-sm transition"
              >
                Sign Up
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;

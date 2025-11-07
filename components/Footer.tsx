import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Rocket, Twitter, Linkedin, Github } from "lucide-react";
import { NAV_LINKS } from "../constants";

const Footer: React.FC = () => {
  const [subscribed, setSubscribed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleFeaturesClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    if (location.pathname !== "/") {
      navigate("/");
      setTimeout(() => {
        document.getElementById("features")?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } else {
      document.getElementById("features")?.scrollIntoView({ behavior: "smooth" });
    }
  };

  const handleSubscribe = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const emailInput = e.currentTarget.elements.namedItem("email-address") as HTMLInputElement;
    if (emailInput && emailInput.value) {
      setSubscribed(true);
    }
  };

  const renderNavLink = (link: { name: string; path: string }) => {
    if (link.path.includes("#")) {
      return (
        <a
          href="#features"
          onClick={handleFeaturesClick}
          className="text-sm text-gray-600 hover:text-teal-600 transition-colors duration-200"
        >
          {link.name}
        </a>
      );
    }
    return (
      <Link
        to={link.path}
        className="text-sm text-gray-600 hover:text-teal-600 transition-colors duration-200"
      >
        {link.name}
      </Link>
    );
  };

  return (
    <footer className="relative bg-gradient-to-br from-white via-teal-200 to-white border-t border-cyan-100">
      <div className="container mx-auto py-12 px-6 md:px-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {/* Logo + About */}
          <div className="space-y-4">
            <a
              href="#/"
              onClick={(e) => {
                e.preventDefault();
                navigate("/");
              }}
              className="flex items-center space-x-2 text-2xl font-bold"
            >
              <Rocket className="w-8 h-8 text-teal-600" />
              <span className="bg-gradient-to-r from-teal-500 to-teal-700 text-transparent bg-clip-text">
                BizPilot
              </span>
            </a>
            <p className="text-gray-500 text-sm leading-relaxed max-w-xs">
              Your AI co-pilot for smarter, faster business decisions.
            </p>
            <div className="flex space-x-4 pt-2">
              <a href="#" className="text-gray-400 hover:text-teal-600 transition">
                <Twitter size={18} />
              </a>
              <a href="#" className="text-gray-400 hover:text-teal-600 transition">
                <Linkedin size={18} />
              </a>
              <a href="#" className="text-gray-400 hover:text-teal-600 transition">
                <Github size={18} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Quick Links
            </h3>
            <ul className="mt-4 space-y-2">
              {NAV_LINKS.map((link) => (
                <li key={link.name}>{renderNavLink(link)}</li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Legal
            </h3>
            <ul className="mt-4 space-y-2">
              <li>
                <a
                  href="#"
                  className="text-sm text-gray-600 hover:text-teal-600 transition-colors duration-200"
                >
                  Privacy Policy
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm text-gray-600 hover:text-teal-600 transition-colors duration-200"
                >
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          {/* Subscribe */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider">
              Subscribe
            </h3>
            <p className="mt-4 text-sm text-gray-600 leading-relaxed">
              Join our newsletter to stay in the loop with product updates.
            </p>

            {subscribed ? (
              <p className="mt-4 text-teal-600 font-medium bg-teal-50 border border-teal-100 rounded-md px-4 py-2">
                🎉 Thank you for subscribing!
              </p>
            ) : (
              <form
                onSubmit={handleSubscribe}
                className="mt-4 flex flex-col sm:flex-row sm:items-center gap-3"
              >
                <input
                  type="email"
                  name="email-address"
                  id="email-address"
                  autoComplete="email"
                  required
                  className="flex-1 border border-teal-200 rounded-md py-2 px-3 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent shadow-sm"
                  placeholder="Enter your email"
                />
                <button
                  type="submit"
                  className="bg-gradient-to-r from-teal-500 to-teal-700 text-white rounded-md py-2 px-4 text-sm font-medium hover:from-teal-600 hover:to-teal-800 transition-all duration-300 shadow-md"
                >
                  Subscribe
                </button>
              </form>
            )}
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 border-t border-teal-100 pt-6 text-center">
          <p className="text-sm text-gray-500">
            © {new Date().getFullYear()} BizPilot. All rights reserved.
          </p>
        </div>
      </div>

      {/* Soft gradient accent */}
      <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-teal-400 via-teal-500 to-teal-700 opacity-60"></div>
    </footer>
  );
};

export default Footer;

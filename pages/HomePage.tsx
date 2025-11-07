import React from 'react';
import { Link } from 'react-router-dom';
import FeatureCard from '../components/FeatureCard';
import { FEATURES } from '../constants';
import { Rocket } from 'lucide-react';

const HomePage: React.FC = () => {
  const handleExploreClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    const featuresElement = document.getElementById('features');
    if (featuresElement) {
      featuresElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="bg-gradient-to-br from-white via-teal-100 to-white border-t border-cyan-100 space-y-16 sm:space-y-24">
      {/* Hero Section */}
      <section className="text-center pt-16 pb-12">
        <div className="inline-flex items-center justify-center bg-gradient-to-br from-white via-teal-100 to-white border-t border-teal-100 text-primary px-4 py-1 rounded-full text-sm font-semibold mb-4">
          <Rocket className="w-4 h-4 mr-2" /> Launch Your Dream Business
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold text-secondary tracking-tight">
          Your AI Co-Pilot for <span className="bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text">Business Success</span>
        </h1>
        <p className="mt-4 max-w-2xl mx-auto text-lg text-gray-600">
          From idea validation to investor matching, BizPilot provides the AI-powered tools and insights you need to build and grow a successful venture.
        </p>
        <div className="mt-8 flex justify-center space-x-4">
          <Link
            to="/ai-powered-idea-validation"
            className="inline-block bg-gradient-to-br from-primary to-primary-700 text-white font-semibold px-8 py-3 rounded-md hover:from-primary-600 hover:to-primary-800 transition-all duration-300 shadow-lg"
          >
            Validate Your Idea
          </Link>
          <a
            href="#features"
            onClick={handleExploreClick}
            className="inline-block bg-gray-200 text-gray-800 font-semibold px-8 py-3 rounded-md hover:bg-gray-300 transition-colors"
          >
            Explore Features
          </a>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-12 bg-white rounded-lg shadow-inner">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-base font-bold tracking-wide uppercase bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text">Our Features</h1>
            <p className="mt-2 text-3xl font-extrabold text-gray-900 tracking-tight sm:text-4xl">
              Everything <span className="bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text"> You Need to Succeed</span>
            </p>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-500">
              BizPilot is packed with powerful features to guide you at every stage of your entrepreneurial journey.
            </p>
          </div>
          <div className="mt-12 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {FEATURES.map((feature) => (
              <FeatureCard key={feature.slug} feature={feature} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
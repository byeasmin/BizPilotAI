import React from 'react';
import { Link } from 'react-router-dom';
import type { Feature } from '../types';
import { ArrowRight } from 'lucide-react';

interface FeatureCardProps {
  feature: Feature;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ feature }) => {
  const Icon = feature.icon;
  const path =
    feature.slug === 'ai-powered-idea-validation'
      ? `/${feature.slug}`
      : `/features/${feature.slug}`;

  return (
    <div className="bg-gradient-to-br from-white to-teal-50 p-6 rounded-2xl shadow-sm hover:shadow-md border border-teal-100 transition-all duration-300 flex flex-col">
      {/* Icon */}
      <div className="flex-shrink-0">
        <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-teal-100 text-teal-600 shadow-sm">
          <Icon className="h-6 w-6" aria-hidden="true" />
        </div>
      </div>

      {/* Title + Description */}
      <div className="mt-4 flex-grow">
        <h3 className="text-lg font-semibold text-gray-900">{feature.title}</h3>
        <p className="mt-2 text-sm text-gray-600 leading-relaxed">
          {feature.description}
        </p>
      </div>

      {/* Learn More Button */}
      <div className="mt-4">
        <Link
          to={path}
          className="inline-flex items-center text-teal-600 hover:text-teal-700 font-medium text-sm group"
        >
          Learn more
          <ArrowRight className="ml-2 h-4 w-4 text-teal-500 transform group-hover:translate-x-1 transition-transform" />
        </Link>
      </div>
    </div>
  );
};

export default FeatureCard;

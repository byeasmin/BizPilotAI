import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { FEATURES } from '../constants';
import { Wrench } from 'lucide-react';

const FeaturePlaceholderPage: React.FC = () => {
  const { slug } = useParams();
  const feature = FEATURES.find(f => f.slug === slug);

  if (!feature) {
    return (
      <div className="text-center py-20">
        <h1 className="text-4xl font-bold">Feature Not Found</h1>
        <p className="mt-4 text-lg text-gray-600">Sorry, we couldn't find the feature you're looking for.</p>
        <Link to="/" className="mt-6 inline-block bg-gradient-to-br from-primary to-primary-700 text-white font-semibold px-6 py-2 rounded-md hover:from-primary-600 hover:to-primary-800 transition-all duration-300">
          Back to Home
        </Link>
      </div>
    );
  }

  const Icon = feature.icon;

  return (
    <div className="max-w-4xl mx-auto text-center py-16">
      <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 text-primary mb-6">
        <Icon className="h-8 w-8" />
      </div>
      <h1 className="text-4xl font-extrabold text-secondary tracking-tight">{feature.title}</h1>
      <p className="mt-4 text-xl text-gray-600">{feature.description}</p>
      
      <div className="mt-12 bg-yellow-50 border-l-4 border-yellow-400 p-6 text-left rounded-r-lg">
          <div className="flex">
            <div className="flex-shrink-0">
                <Wrench className="h-6 w-6 text-yellow-500" />
            </div>
            <div className="ml-3">
              <h3 className="text-lg font-medium text-yellow-800">Coming Soon!</h3>
              <div className="mt-2 text-md text-yellow-700">
                <p>We're hard at work building this feature. Check back soon for exciting updates!</p>
              </div>
            </div>
          </div>
      </div>

       <Link to="/" className="mt-12 inline-block bg-gradient-to-br from-primary to-primary-700 text-white font-semibold px-8 py-3 rounded-md hover:from-primary-600 hover:to-primary-800 transition-all duration-300">
          Return to Dashboard
        </Link>
    </div>
  );
};

export default FeaturePlaceholderPage;
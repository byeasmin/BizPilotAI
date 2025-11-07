import React, { useState } from 'react';
import { Mail, Phone, MapPin, CheckCircle } from 'lucide-react';

const ContactPage: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="bg-gradient-to-br from-white via-teal-100 to-white border-t border-teal-100 rounded-lg shadow-lg overflow-hidden">
      <div className="p-8 md:p-12">
        <div className="text-center">
            <h1 className="text-4xl font-extrabold text-teal-800 text-secondary tracking-tight">Get in Touch</h1>
            <p className="mt-3 max-w-2xl mx-auto text-lg text-gray-600">We’d love to hear from you! Whether you have a question about features, trials, or anything else, our team is ready to answer all your questions.</p>
        </div>
        
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-12">
            {/* Contact Form */}
            {submitted ? (
              <div className="flex flex-col items-center justify-center text-center h-full bg-gray-50 rounded-lg p-8">
                <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
                <h3 className="text-2xl font-bold text-secondary">Thank You!</h3>
                <p className="text-gray-600 mt-2">Your message has been received. We'll get back to you shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700">Full Name</label>
                      <input required type="text" name="name" id="name" autoComplete="name" className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary" />
                  </div>
                  <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                      <input required type="email" name="email" id="email" autoComplete="email" className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary" />
                  </div>
                  <div>
                      <label htmlFor="message" className="block text-sm font-medium text-gray-700">Message</label>
                      <textarea required id="message" name="message" rows={4} className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary"></textarea>
                  </div>
                  <div>
                      <button type="submit" className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-br from-primary to-primary-700 hover:from-primary-600 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-300">
                          Send Message
                      </button>
                  </div>
              </form>
            )}

            {/* Contact Info */}
            <div className="space-y-8">
                <div className="flex items-start">
                    <div className="flex-shrink-0">
                        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-50 text-primary">
                            <Mail className="h-6 w-6" />
                        </div>
                    </div>
                    <div className="ml-4">
                        <h3 className="text-lg font-medium text-gray-900">Email</h3>
                        <p className="mt-1 text-gray-600">support@bizpilot.com</p>
                    </div>
                </div>
                 <div className="flex items-start">
                    <div className="flex-shrink-0">
                        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-50 text-primary">
                            <Phone className="h-6 w-6" />
                        </div>
                    </div>
                    <div className="ml-4">
                        <h3 className="text-lg font-medium text-gray-900">Phone</h3>
                        <p className="mt-1 text-gray-600">+1 (555) 123-4567</p>
                    </div>
                </div>
                 <div className="flex items-start">
                    <div className="flex-shrink-0">
                        <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-50 text-primary">
                            <MapPin className="h-6 w-6" />
                        </div>
                    </div>
                    <div className="ml-4">
                        <h3 className="text-lg font-medium text-gray-900">Address</h3>
                        <p className="mt-1 text-gray-600">123 Innovation Drive, Startup City, 12345</p>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
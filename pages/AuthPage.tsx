import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Rocket, Mail, Lock } from 'lucide-react';

const AuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-xl shadow-lg">
        <div className="text-center mb-8">
            <Link to="/" className="flex justify-center items-center space-x-2 text-3xl font-bold mb-2">
              <Rocket className="w-9 h-9 text-primary" />
              <span className="bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text">BizPilot</span>
            </Link>
            <h2 className="text-2xl font-bold text-secondary">
              {isLogin ? 'Welcome Back!' : 'Create an Account'}
            </h2>
            <p className="text-gray-600">
                {isLogin ? 'Log in to continue your journey.' : 'Join us to start building your dream business.'}
            </p>
        </div>

        <form className="space-y-6">
            <div className="relative">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                    <Mail className="h-5 w-5 text-gray-400" />
                </span>
                <input
                    type="email"
                    name="email"
                    placeholder="Email Address"
                    required
                    className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                />
            </div>

            <div className="relative">
                 <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                    <Lock className="h-5 w-5 text-gray-400" />
                </span>
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    required
                    className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                />
            </div>
            {!isLogin && (
                <div className="relative">
                    <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                        <Lock className="h-5 w-5 text-gray-400" />
                    </span>
                    <input
                        type="password"
                        name="confirmPassword"
                        placeholder="Confirm Password"
                        required
                        className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary focus:border-primary"
                    />
                </div>
            )}
            {isLogin && (
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" className="h-4 w-4 text-primary focus:ring-primary-dark border-gray-300 rounded" />
                        <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">Remember me</label>
                    </div>
                    <div className="text-sm">
                        <a href="#" className="font-medium bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text hover:brightness-110">Forgot your password?</a>
                    </div>
                </div>
            )}
            
            <div>
                <button
                    type="submit"
                    className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-br from-primary to-primary-700 hover:from-primary-600 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-300"
                >
                    {isLogin ? 'Log In' : 'Sign Up'}
                </button>
            </div>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
            {isLogin ? "Don't have an account?" : 'Already have an account?'}
            <button onClick={() => setIsLogin(!isLogin)} className="font-medium bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text hover:brightness-110 ml-1">
                 {isLogin ? 'Sign up' : 'Log in'}
            </button>
        </p>
      </div>
    </div>
  );
};

export default AuthPage;
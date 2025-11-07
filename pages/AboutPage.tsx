import React from 'react';
import { Rocket, Users, Target } from 'lucide-react';

const teamMembers = [
  { name: 'Mohammad Hossain', role: 'Software Developer', imageUrl: 'https://picsum.photos/id/1005/200/200' },
  { name: 'Mohammad Minul Islam', role: 'Software Developer', imageUrl: 'https://picsum.photos/id/1011/200/200' },
  { name: 'Umme Benin Yeasmin Meem', role: 'Backend Developer', imageUrl: 'https://picsum.photos/id/1027/200/200' },
  { name: 'Kazi Namira Meyheg Sanam', role: 'UX/UI Designer', imageUrl: 'https://picsum.photos/id/10/200/200' },
];

const AboutPage: React.FC = () => {
  return (
    <div className="bg-gradient-to-br from-white via-teal-100 to-white border-t border-teal-100 rounded-lg shadow-lg overflow-hidden">
      <div className="relative h-64 w-full">
        <img className="h-full w-full object-cover" src="" alt="Team working" />
        <div className="absolute inset-0 bg-gradient-to-t from-primary/70 to-primary-100/80 flex items-center justify-center">
            <h1 className="text-5xl font-extrabold text-teal-800 tracking-tight">About BizPilot</h1>
        </div>
      </div>

      <div className="p-8 md:p-12 space-y-16">
        {/* Our Mission */}
        <section className="grid md:grid-cols-2 gap-8 items-center">
            <div>
                <h2 className="text-3xl font-bold text-secondary flex items-center"><Target className="w-8 h-8 mr-3 text-primary"/>Our Mission</h2>
                <p className="mt-4 text-lg text-gray-600">
                    To empower entrepreneurs everywhere by providing accessible, AI-driven tools that simplify the complexities of starting and growing a business. We believe that a great idea, combined with the right guidance, can change the world. BizPilot is here to be that guide.
                </p>
            </div>
            <div className="text-center">
                <Rocket className="w-48 h-48 text-primary-200 mx-auto"/>
            </div>
        </section>

        {/* Our Story */}
        <section>
          <h2 className="text-3xl font-bold text-center text-secondary">Our Story</h2>
          <p className="mt-4 max-w-3xl mx-auto text-center text-lg text-gray-600">
            Founded by a team of entrepreneurs and AI experts, BizPilot was born from a shared frustration with the barriers new founders face. From navigating dense legal jargon to securing that first round of funding, we've been there. We built BizPilot to be the co-pilot we wish we had, leveraging cutting-edge AI to provide clear, actionable, and personalized business advice.
          </p>
        </section>
        
        {/* Meet the Team */}
        <section>
          <div className="text-center">
             <h2 className="text-3xl font-bold text-secondary flex items-center justify-center"><Users className="w-8 h-8 mr-3 text-primary"/>Meet the Team</h2>
            <p className="mt-4 max-w-2xl mx-auto text-lg text-gray-600">
              The passionate minds behind the mission.
            </p>
          </div>
          <div className="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
            {teamMembers.map((person) => (
              <div key={person.name} className="text-center">
                <img className="mx-auto h-32 w-32 rounded-full" src={person.imageUrl} alt={person.name} />
                <div className="mt-4">
                  <h3 className="text-lg font-medium text-gray-900">{person.name}</h3>
                  <p className="font-semibold bg-gradient-to-r from-primary to-primary-700 text-transparent bg-clip-text">{person.role}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default AboutPage;
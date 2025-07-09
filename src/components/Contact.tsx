
import { Mail, Phone, MapPin, Send, Clock, Users, Target, Award } from 'lucide-react';
import { useState } from 'react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    experience: '',
    currentRole: '',
    company: '',
    motivation: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Application submitted:', formData);
  };

  const applicationProcess = [
    {
      step: "1",
      title: "Submit Application",
      description: "Fill out our comprehensive application form with your background and growth goals",
      icon: Send
    },
    {
      step: "2", 
      title: "Growth Assessment",
      description: "Take our proprietary growth mindset and analytical thinking assessment",
      icon: Target
    },
    {
      step: "3",
      title: "Interview Round",
      description: "One-on-one interview with our growth experts to understand your potential",
      icon: Users
    },
    {
      step: "4",
      title: "Welcome to GrowthX",
      description: "Join your exclusive cohort and begin your growth transformation journey",
      icon: Award
    }
  ];

  return (
    <section id="contact" className="py-20 bg-[#0a0a12] relative">
      <div className="absolute inset-0 bg-gradient-to-b from-purple-900/10 via-transparent to-purple-900/10"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-300 text-sm font-medium mb-6">
            🚀 Ready to Transform Your Career?
          </div>
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-white">
            Start Your
            <span className="gradient-text"> Growth Journey</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Apply now for our next cohort. Limited seats available with our selective admission process 
            ensuring you learn alongside the best growth professionals in India.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-16">
          {/* Contact Information & Process */}
          <div className="space-y-8">
            {/* Contact Details */}
            <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl p-8 border border-gray-800/50 card-glow">
              <h3 className="text-2xl font-bold text-white mb-6">Get in Touch</h3>
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-full flex items-center justify-center">
                    <Mail className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">Email Us</h4>
                    <p className="text-gray-400">hello@growthx.club</p>
                    <p className="text-gray-400">admissions@growthx.club</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-full flex items-center justify-center">
                    <Phone className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">Call Us</h4>
                    <p className="text-gray-400">+91 98765 43210</p>
                    <p className="text-gray-400">Mon-Fri, 10AM-6PM IST</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-full flex items-center justify-center">
                    <MapPin className="w-6 h-6 text-purple-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">Visit Us</h4>
                    <p className="text-gray-400">Koramangala, Bengaluru</p>
                    <p className="text-gray-400">Karnataka, India 560034</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Application Process */}
            <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl p-8 border border-gray-800/50 card-glow">
              <h3 className="text-2xl font-bold text-white mb-6">Application Process</h3>
              <div className="space-y-6">
                {applicationProcess.map((process, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
                      {process.step}
                    </div>
                    <div>
                      <h4 className="text-white font-semibold mb-1">{process.title}</h4>
                      <p className="text-gray-400 text-sm leading-relaxed">{process.description}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg">
                <div className="flex items-center text-purple-300 text-sm">
                  <Clock className="w-4 h-4 mr-2" />
                  <span>Application deadline: March 15, 2024 | Next cohort starts: April 1, 2024</span>
                </div>
              </div>
            </div>
          </div>

          {/* Application Form */}
          <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl p-8 border border-gray-800/50 card-glow">
            <h3 className="text-2xl font-bold text-white mb-6">Apply Now</h3>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-gray-400"
                    placeholder="Your full name"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-gray-400"
                    placeholder="your@email.com"
                    required
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-gray-300 mb-2">
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-gray-400"
                    placeholder="+91 98765 43210"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="experience" className="block text-sm font-medium text-gray-300 mb-2">
                    Years of Experience *
                  </label>
                  <select
                    id="experience"
                    name="experience"
                    value={formData.experience}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white"
                    required
                  >
                    <option value="">Select experience</option>
                    <option value="0-2">0-2 years</option>
                    <option value="2-5">2-5 years</option>
                    <option value="5-10">5-10 years</option>
                    <option value="10+">10+ years</option>
                  </select>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="currentRole" className="block text-sm font-medium text-gray-300 mb-2">
                    Current Role *
                  </label>
                  <input
                    type="text"
                    id="currentRole"
                    name="currentRole"
                    value={formData.currentRole}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-gray-400"
                    placeholder="e.g. Marketing Manager"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-300 mb-2">
                    Current Company *
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-gray-400"
                    placeholder="Company name"
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="motivation" className="block text-sm font-medium text-gray-300 mb-2">
                  Why do you want to join GrowthX? *
                </label>
                <textarea
                  id="motivation"
                  name="motivation"
                  rows={4}
                  value={formData.motivation}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none text-white placeholder-gray-400"
                  placeholder="Tell us about your growth goals, what you hope to achieve, and why you want to be part of our exclusive community..."
                  required
                ></textarea>
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white px-8 py-4 rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-300 font-semibold flex items-center justify-center"
              >
                Submit Application
                <Send className="ml-2 w-5 h-5" />
              </button>

              <p className="text-xs text-gray-400 text-center">
                By submitting this form, you agree to our Terms of Service and Privacy Policy. 
                We'll contact you within 48 hours.
              </p>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;

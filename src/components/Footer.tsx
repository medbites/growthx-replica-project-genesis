
import { Twitter, Linkedin, Instagram, Mail, ArrowUp } from 'lucide-react';

const Footer = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-[#0a0a12] border-t border-gray-800/50 relative">
      <div className="absolute inset-0 bg-gradient-to-t from-purple-900/5 to-transparent"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand & Description */}
          <div className="space-y-6">
            <div className="text-2xl font-bold gradient-text">
              GrowthX
            </div>
            <p className="text-gray-400 max-w-xs leading-relaxed">
              Building India's most exclusive community of growth professionals. 
              Transform your career with us.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="w-10 h-10 bg-gray-800/50 rounded-full flex items-center justify-center text-gray-400 hover:text-purple-400 hover:bg-purple-500/20 transition-all duration-300">
                <Twitter size={18} />
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800/50 rounded-full flex items-center justify-center text-gray-400 hover:text-purple-400 hover:bg-purple-500/20 transition-all duration-300">
                <Linkedin size={18} />
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800/50 rounded-full flex items-center justify-center text-gray-400 hover:text-purple-400 hover:bg-purple-500/20 transition-all duration-300">
                <Instagram size={18} />
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800/50 rounded-full flex items-center justify-center text-gray-400 hover:text-purple-400 hover:bg-purple-500/20 transition-all duration-300">
                <Mail size={18} />
              </a>
            </div>
          </div>

          {/* Programs */}
          <div>
            <h3 className="text-lg font-semibold mb-6 text-white">Programs</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Growth Leadership</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Product Growth</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Marketing Bootcamp</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Growth Foundations</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Executive Program</a></li>
            </ul>
          </div>

          {/* Community */}
          <div>
            <h3 className="text-lg font-semibold mb-6 text-white">Community</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Alumni Network</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Success Stories</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Events & Workshops</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Mentorship Program</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Job Board</a></li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-lg font-semibold mb-6 text-white">Company</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">About GrowthX</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Our Team</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Careers</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Blog & Resources</a></li>
              <li><a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">Contact Us</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800/50 mt-12 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-8">
              <p className="text-gray-400 text-sm">
                © 2024 GrowthX. All rights reserved.
              </p>
              <div className="flex space-x-6">
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors text-sm">
                  Privacy Policy
                </a>
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors text-sm">
                  Terms of Service
                </a>
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors text-sm">
                  Cookie Policy
                </a>
              </div>
            </div>
            
            <button 
              onClick={scrollToTop}
              className="w-10 h-10 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-full flex items-center justify-center text-purple-400 hover:from-purple-500/30 hover:to-purple-600/30 transition-all duration-300 mt-4 md:mt-0"
            >
              <ArrowUp size={18} />
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

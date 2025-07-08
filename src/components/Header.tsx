
import { useState } from 'react';
import { Menu, X } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="fixed top-0 w-full bg-[#0a0a12]/95 backdrop-blur-md border-b border-gray-800/50 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="text-2xl font-bold text-white">
              GrowthX
            </div>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <a href="#home" className="text-gray-300 hover:text-white transition-colors font-medium">
              Home
            </a>
            <a href="#about" className="text-gray-300 hover:text-white transition-colors font-medium">
              About
            </a>
            <a href="#programs" className="text-gray-300 hover:text-white transition-colors font-medium">
              Programs
            </a>
            <a href="#community" className="text-gray-300 hover:text-white transition-colors font-medium">
              Community
            </a>
            <a href="#contact" className="text-gray-300 hover:text-white transition-colors font-medium">
              Contact
            </a>
          </nav>

          <div className="hidden md:flex items-center space-x-4">
            <button className="text-gray-300 hover:text-white transition-colors font-medium">
              Sign In
            </button>
            <button className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-6 py-2 rounded-full hover:from-purple-600 hover:to-purple-700 transition-all duration-300 font-medium">
              Apply Now
            </button>
          </div>

          <div className="md:hidden">
            <button onClick={toggleMenu} className="text-gray-300 hover:text-white">
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-800">
            <div className="flex flex-col space-y-4">
              <a href="#home" className="text-gray-300 hover:text-white transition-colors font-medium">
                Home
              </a>
              <a href="#about" className="text-gray-300 hover:text-white transition-colors font-medium">
                About
              </a>
              <a href="#programs" className="text-gray-300 hover:text-white transition-colors font-medium">
                Programs
              </a>
              <a href="#community" className="text-gray-300 hover:text-white transition-colors font-medium">
                Community
              </a>
              <a href="#contact" className="text-gray-300 hover:text-white transition-colors font-medium">
                Contact
              </a>
              <div className="flex flex-col space-y-2 pt-4 border-t border-gray-800">
                <button className="text-gray-300 hover:text-white transition-colors font-medium text-left">
                  Sign In
                </button>
                <button className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-6 py-2 rounded-full hover:from-purple-600 hover:to-purple-700 transition-all duration-300 font-medium">
                  Apply Now
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;


import { ArrowRight, Play } from 'lucide-react';

const Hero = () => {
  return (
    <section id="home" className="pt-16 min-h-screen flex items-center bg-[#0a0a12] relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-blue-900/20"></div>
      <div className="absolute top-20 right-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-6">
              <div className="inline-flex items-center px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-300 text-sm font-medium">
                🚀 India's most exclusive growth community
              </div>
              
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight text-white">
                Build your
                <span className="block gradient-text">Growth Career</span>
              </h1>
              
              <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                Join India's most exclusive growth community. Learn from the best growth leaders, 
                work on real challenges, and accelerate your career in growth.
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="group bg-gradient-to-r from-purple-500 to-purple-600 text-white px-8 py-4 rounded-full hover:from-purple-600 hover:to-purple-700 transition-all duration-300 font-semibold flex items-center justify-center">
                Apply for next cohort
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
              </button>
              
              <button className="group border border-gray-600 text-white px-8 py-4 rounded-full hover:border-purple-500 hover:bg-purple-500/10 transition-all duration-300 font-semibold flex items-center justify-center">
                <Play className="mr-2" size={20} />
                Watch Demo
              </button>
            </div>

            <div className="flex items-center space-x-12 pt-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">5000+</div>
                <div className="text-gray-400 text-sm">Growth Professionals</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white">50+</div>
                <div className="text-gray-400 text-sm">Partner Companies</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white">15+</div>
                <div className="text-gray-400 text-sm">Successful Cohorts</div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="relative z-10">
              <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl p-8 border border-gray-800/50 card-glow">
                <div className="space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
                      <span className="text-white font-bold text-lg">GX</span>
                    </div>
                    <div>
                      <div className="font-semibold text-white">Growth Dashboard</div>
                      <div className="text-gray-400 text-sm">Live Metrics</div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                      <span className="text-green-400 font-medium">User Acquisition</span>
                      <span className="text-green-400 font-bold text-xl">↗ 342%</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                      <span className="text-blue-400 font-medium">Revenue Growth</span>
                      <span className="text-blue-400 font-bold text-xl">↗ 185%</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-purple-500/10 rounded-lg border border-purple-500/20">
                      <span className="text-purple-400 font-medium">Retention Rate</span>
                      <span className="text-purple-400 font-bold text-xl">↗ 96%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

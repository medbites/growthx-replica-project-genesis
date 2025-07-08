
import { ArrowRight } from 'lucide-react';

const Hero = () => {
  return (
    <section id="home" className="pt-16 min-h-screen flex items-center bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-6">
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                Build your
                <span className="block text-orange-500">Growth Career</span>
              </h1>
              <p className="text-xl text-gray-400 leading-relaxed max-w-2xl">
                Join India's most exclusive growth community. Learn from the best growth leaders, 
                work on real challenges, and accelerate your career in growth.
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="group bg-orange-500 text-white px-8 py-4 rounded-md hover:bg-orange-600 transition-all duration-300 font-semibold flex items-center justify-center">
                Apply for Cohort
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
              </button>
              <button className="border border-gray-600 text-white px-8 py-4 rounded-md hover:border-orange-500 hover:text-orange-500 transition-all duration-300 font-semibold">
                Learn More
              </button>
            </div>

            <div className="flex items-center space-x-12 pt-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">5000+</div>
                <div className="text-gray-400">Growth Professionals</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white">50+</div>
                <div className="text-gray-400">Partner Companies</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white">15+</div>
                <div className="text-gray-400">Cohorts</div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="relative z-10">
              <div className="bg-gray-900 rounded-2xl p-8 border border-gray-800">
                <div className="space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center">
                      <span className="text-white font-bold text-lg">GX</span>
                    </div>
                    <div>
                      <div className="font-semibold text-white">Growth Metrics</div>
                      <div className="text-gray-400 text-sm">Live Dashboard</div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-green-900/20 rounded-lg border border-green-800/30">
                      <span className="text-green-400 font-medium">User Growth</span>
                      <span className="text-green-400 font-bold">↗ 340%</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-blue-900/20 rounded-lg border border-blue-800/30">
                      <span className="text-blue-400 font-medium">Revenue</span>
                      <span className="text-blue-400 font-bold">↗ 180%</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-purple-900/20 rounded-lg border border-purple-800/30">
                      <span className="text-purple-400 font-medium">Retention</span>
                      <span className="text-purple-400 font-bold">↗ 95%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="absolute inset-0 bg-orange-500/10 rounded-2xl transform rotate-3 -z-10"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

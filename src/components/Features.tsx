
import { Users, Target, TrendingUp, BookOpen, Award, Network } from 'lucide-react';

const Features = () => {
  const programs = [
    {
      icon: Award,
      title: "Growth Leadership Program",
      description: "A 16-week intensive program designed for senior growth professionals looking to level up their leadership skills.",
      duration: "16 weeks",
      level: "Senior Level",
      price: "₹1,50,000"
    },
    {
      icon: Target,
      title: "Growth Product Manager",
      description: "Specialized 12-week program for Product Managers who want to master product-led growth strategies.",
      duration: "12 weeks", 
      level: "Mid-Senior",
      price: "₹1,20,000"
    },
    {
      icon: TrendingUp,
      title: "Growth Marketing Bootcamp",
      description: "Master performance marketing, growth loops, and data-driven marketing in this comprehensive bootcamp.",
      duration: "10 weeks",
      level: "All Levels",
      price: "₹80,000"
    },
    {
      icon: BookOpen,
      title: "Growth Foundations",
      description: "Perfect entry point for professionals new to growth. Learn the fundamentals from industry experts.",
      duration: "8 weeks",
      level: "Beginner",
      price: "₹50,000"
    },
    {
      icon: Users,
      title: "Executive Growth Program",
      description: "Exclusive program for C-suite executives and founders scaling their businesses to new heights.",
      duration: "6 weeks",
      level: "Executive",
      price: "₹2,00,000"
    },
    {
      icon: Network,
      title: "Community Access",
      description: "Get lifetime access to our exclusive community of 5000+ growth professionals and industry leaders.",
      duration: "Lifetime",
      level: "All Programs",
      price: "Included"
    }
  ];

  return (
    <section id="programs" className="py-20 bg-[#0a0a12] relative">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-purple-900/5 to-transparent"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-300 text-sm font-medium mb-6">
            📚 Our Programs
          </div>
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-white">
            Choose Your
            <span className="gradient-text"> Growth Path</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
            From beginners to executives, we have carefully designed programs that cater to 
            different experience levels and career goals in growth.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {programs.map((program, index) => (
            <div
              key={index}
              className="group p-8 bg-gray-900/50 backdrop-blur-lg rounded-2xl border border-gray-800/50 hover:border-purple-500/50 transition-all duration-500 card-hover card-glow"
            >
              <div className="w-14 h-14 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-xl flex items-center justify-center mb-6 group-hover:from-purple-500/30 group-hover:to-purple-600/30 transition-all duration-300">
                <program.icon className="w-7 h-7 text-purple-400" />
              </div>
              
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-white group-hover:text-purple-300 transition-colors">
                  {program.title}
                </h3>
                <div className="text-right">
                  <div className="text-sm text-purple-400 font-medium">{program.duration}</div>
                  <div className="text-xs text-gray-500">{program.level}</div>
                </div>
              </div>
              
              <p className="text-gray-400 leading-relaxed mb-6">
                {program.description}
              </p>
              
              <div className="flex items-center justify-between mb-6">
                <span className="text-2xl font-bold text-white">{program.price}</span>
                <span className="text-sm text-gray-500">Per person</span>
              </div>
              
              <button className="w-full py-3 bg-gradient-to-r from-purple-500/20 to-purple-600/20 border border-purple-500/30 rounded-lg text-purple-300 hover:from-purple-500/30 hover:to-purple-600/30 hover:border-purple-400 transition-all duration-300 font-medium">
                Learn More
              </button>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <button className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-8 py-4 rounded-full hover:from-purple-600 hover:to-purple-700 transition-all duration-300 font-semibold">
            View All Programs & Apply
          </button>
        </div>
      </div>
    </section>
  );
};

export default Features;

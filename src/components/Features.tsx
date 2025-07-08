
import { Users, Target, TrendingUp, BookOpen, Award, Network } from 'lucide-react';

const Features = () => {
  const programs = [
    {
      icon: Users,
      title: "Growth Leadership Program",
      description: "16-week intensive program for senior growth professionals and leaders.",
      duration: "16 weeks",
      level: "Senior"
    },
    {
      icon: Target,
      title: "Growth Product Manager",
      description: "Specialized program for PMs focusing on growth and product-led growth.",
      duration: "12 weeks", 
      level: "Mid-Senior"
    },
    {
      icon: TrendingUp,
      title: "Growth Marketing Bootcamp",
      description: "Master growth marketing frameworks, channels, and optimization techniques.",
      duration: "10 weeks",
      level: "All Levels"
    },
    {
      icon: BookOpen,
      title: "Growth Foundations",
      description: "Perfect for beginners looking to start their career in growth.",
      duration: "8 weeks",
      level: "Beginner"
    },
    {
      icon: Award,
      title: "Executive Growth Program",
      description: "For C-suite executives and founders scaling their businesses.",
      duration: "6 weeks",
      level: "Executive"
    },
    {
      icon: Network,
      title: "Community Access",
      description: "Lifetime access to our exclusive community of growth professionals.",
      duration: "Lifetime",
      level: "All Programs"
    }
  ];

  return (
    <section id="programs" className="py-20 bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Our
            <span className="text-orange-500"> Programs</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Choose from our carefully designed programs that cater to different experience levels 
            and career goals in growth.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {programs.map((program, index) => (
            <div
              key={index}
              className="group p-8 bg-black rounded-2xl border border-gray-800 hover:border-orange-500/50 transition-all duration-300 hover:-translate-y-2"
            >
              <div className="w-14 h-14 bg-orange-500/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-orange-500/20 transition-colors duration-300">
                <program.icon className="w-7 h-7 text-orange-500" />
              </div>
              
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-white group-hover:text-orange-500 transition-colors">
                  {program.title}
                </h3>
                <div className="text-right">
                  <div className="text-sm text-orange-500 font-medium">{program.duration}</div>
                  <div className="text-xs text-gray-500">{program.level}</div>
                </div>
              </div>
              
              <p className="text-gray-400 leading-relaxed mb-6">
                {program.description}
              </p>
              
              <button className="w-full py-3 border border-gray-700 rounded-lg text-gray-300 hover:border-orange-500 hover:text-orange-500 transition-colors font-medium">
                Learn More
              </button>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <button className="bg-orange-500 text-white px-8 py-4 rounded-md hover:bg-orange-600 transition-colors font-semibold">
            View All Programs
          </button>
        </div>
      </div>
    </section>
  );
};

export default Features;

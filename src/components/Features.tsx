
import { TrendingUp, Users, Target, BarChart3, Zap, Shield } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: TrendingUp,
      title: "Growth Analytics",
      description: "Advanced metrics and insights to track your business growth with real-time data visualization and reporting."
    },
    {
      icon: Users,
      title: "Expert Network",
      description: "Connect with industry leaders, mentors, and growth experts who can guide your business journey."
    },
    {
      icon: Target,
      title: "Strategic Planning",
      description: "Develop comprehensive growth strategies tailored to your business goals and market opportunities."
    },
    {
      icon: BarChart3,
      title: "Performance Tracking",
      description: "Monitor key performance indicators and optimize your growth initiatives with data-driven decisions."
    },
    {
      icon: Zap,
      title: "Rapid Implementation",
      description: "Execute growth strategies quickly with our streamlined processes and proven methodologies."
    },
    {
      icon: Shield,
      title: "Risk Management",
      description: "Identify and mitigate potential risks while maximizing growth opportunities for sustainable success."
    }
  ];

  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Powerful Features for
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Exponential Growth</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Everything you need to scale your business efficiently and effectively, backed by data and proven by results.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-8 bg-gradient-to-br from-gray-50 to-white rounded-2xl border border-gray-100 hover:shadow-xl hover:border-blue-200 transition-all duration-300 hover:-translate-y-2"
            >
              <div className="w-14 h-14 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <feature.icon className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-full hover:shadow-xl transition-all duration-300 font-semibold">
            Explore All Features
          </button>
        </div>
      </div>
    </section>
  );
};

export default Features;

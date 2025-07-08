
import { CheckCircle, Award, Globe, Lightbulb } from 'lucide-react';

const About = () => {
  const values = [
    {
      icon: CheckCircle,
      title: "Proven Results",
      description: "Track record of helping businesses achieve 3x growth within 12 months"
    },
    {
      icon: Award,
      title: "Industry Recognition",
      description: "Awarded as the leading growth platform by major industry publications"
    },
    {
      icon: Globe,
      title: "Global Reach",
      description: "Supporting businesses across 50+ countries with localized expertise"
    },
    {
      icon: Lightbulb,
      title: "Innovation First",
      description: "Cutting-edge strategies and tools that stay ahead of market trends"
    }
  ];

  return (
    <section id="about" className="py-20 bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="text-4xl font-bold text-gray-900">
                Empowering Businesses to
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block">
                  Reach New Heights
                </span>
              </h2>
              <p className="text-xl text-gray-600 leading-relaxed">
                We believe every business has the potential for extraordinary growth. Our mission is to provide the tools, insights, and expertise needed to unlock that potential and create lasting success.
              </p>
            </div>

            <div className="space-y-6">
              {values.map((value, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <value.icon className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {value.title}
                    </h3>
                    <p className="text-gray-600">
                      {value.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex items-center space-x-8 pt-8">
              <div className="text-center">
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  500+
                </div>
                <div className="text-gray-600 font-medium">Success Stories</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  98%
                </div>
                <div className="text-gray-600 font-medium">Client Satisfaction</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  50+
                </div>
                <div className="text-gray-600 font-medium">Countries</div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="relative z-10">
              <img
                src="https://images.unsplash.com/photo-1581092795360-fd1ca04f0952?auto=format&fit=crop&w=800&q=80"
                alt="Team collaboration"
                className="rounded-2xl shadow-2xl"
              />
            </div>
            <div className="absolute -top-6 -right-6 w-full h-full bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl opacity-20"></div>
            <div className="absolute -bottom-6 -left-6 w-full h-full bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl opacity-10"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;

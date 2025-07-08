
import { CheckCircle, Users, Target, Award } from 'lucide-react';

const About = () => {
  const stats = [
    { number: "5000+", label: "Alumni Network" },
    { number: "50+", label: "Partner Companies" },
    { number: "15+", label: "Successful Cohorts" },
    { number: "95%", label: "Job Placement Rate" }
  ];

  const features = [
    {
      icon: CheckCircle,
      title: "Industry-Relevant Curriculum",
      description: "Our curriculum is designed by top growth leaders from companies like Flipkart, Swiggy, and Razorpay"
    },
    {
      icon: Users,
      title: "Peer Learning",
      description: "Learn alongside ambitious growth professionals from diverse backgrounds and industries"
    },
    {
      icon: Target,
      title: "Real Projects",
      description: "Work on live projects with partner companies and build a portfolio that showcases your skills"
    },
    {
      icon: Award,
      title: "Career Support",
      description: "Get personalized career guidance, interview prep, and access to exclusive job opportunities"
    }
  ];

  return (
    <section id="about" className="py-20 bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h2 className="text-4xl font-bold">
                Why Choose
                <span className="text-orange-500 block">GrowthX?</span>
              </h2>
              <p className="text-xl text-gray-400 leading-relaxed">
                We're building India's most exclusive community of growth professionals. 
                Our alumni work at top companies and lead growth teams that drive millions in revenue.
              </p>
            </div>

            <div className="space-y-6">
              {features.map((feature, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-orange-500/10 rounded-full flex items-center justify-center flex-shrink-0">
                    <feature.icon className="w-5 h-5 text-orange-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-1">
                      {feature.title}
                    </h3>
                    <p className="text-gray-400">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-8">
            <div className="grid grid-cols-2 gap-6">
              {stats.map((stat, index) => (
                <div key={index} className="text-center p-6 bg-gray-900 rounded-2xl border border-gray-800">
                  <div className="text-3xl font-bold text-orange-500 mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-400 font-medium">{stat.label}</div>
                </div>
              ))}
            </div>

            <div className="bg-gray-900 rounded-2xl p-8 border border-gray-800">
              <h3 className="text-xl font-semibold text-white mb-4">Success Stories</h3>
              <div className="space-y-4">
                <div className="border-l-4 border-orange-500 pl-4">
                  <p className="text-gray-400 italic">
                    "GrowthX transformed my career. I went from a marketing executive to leading 
                    growth at a unicorn startup within 18 months."
                  </p>
                  <p className="text-white font-medium mt-2">- Priya Sharma, Growth Lead at Razorpay</p>
                </div>
                <div className="border-l-4 border-orange-500 pl-4">
                  <p className="text-gray-400 italic">
                    "The network and knowledge I gained at GrowthX has been invaluable. 
                    It's not just a program, it's a community for life."
                  </p>
                  <p className="text-white font-medium mt-2">- Arjun Patel, VP Growth at Swiggy</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;

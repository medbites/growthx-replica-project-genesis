
import { CheckCircle, Users, Target, Award, Star, TrendingUp } from 'lucide-react';

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
      description: "Our curriculum is designed by top growth leaders from companies like Flipkart, Swiggy, Razorpay, and CRED"
    },
    {
      icon: Users,
      title: "Peer Learning Network",
      description: "Learn alongside ambitious growth professionals from diverse backgrounds and top-tier companies"
    },
    {
      icon: Target,
      title: "Real-World Projects",
      description: "Work on live growth challenges with our partner companies and build a portfolio that stands out"
    },
    {
      icon: Award,
      title: "Career Transformation",
      description: "Get personalized career guidance, interview prep, and access to exclusive job opportunities at top companies"
    }
  ];

  const testimonials = [
    {
      quote: "GrowthX transformed my career completely. I went from a marketing executive to leading growth at a unicorn startup within 18 months of completing the program.",
      author: "Priya Sharma",
      position: "Growth Lead at Razorpay",
      image: "PS"
    },
    {
      quote: "The network and knowledge I gained at GrowthX has been invaluable. It's not just a program, it's a community for life that opens doors you never knew existed.",
      author: "Arjun Patel",
      position: "VP Growth at Swiggy",
      image: "AP"
    }
  ];

  return (
    <section id="about" className="py-20 bg-[#0a0a12] relative">
      <div className="absolute inset-0 bg-gradient-to-r from-purple-900/10 via-transparent to-blue-900/10"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center mb-20">
          <div className="space-y-8">
            <div className="space-y-6">
              <div className="inline-flex items-center px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-300 text-sm font-medium">
                🏆 Why Choose GrowthX
              </div>
              
              <h2 className="text-4xl lg:text-5xl font-bold text-white">
                India's Most
                <span className="gradient-text block">Exclusive Growth Community</span>
              </h2>
              
              <p className="text-xl text-gray-400 leading-relaxed">
                We're building India's most exclusive community of growth professionals. 
                Our alumni work at top companies and lead growth teams that drive millions in revenue.
              </p>
            </div>

            <div className="space-y-6">
              {features.map((feature, index) => (
                <div key={index} className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-purple-500/20 to-purple-600/20 rounded-full flex items-center justify-center flex-shrink-0">
                    <feature.icon className="w-5 h-5 text-purple-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-400 leading-relaxed">
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
                <div key={index} className="text-center p-6 bg-gray-900/50 backdrop-blur-lg rounded-2xl border border-gray-800/50 card-glow">
                  <div className="text-3xl lg:text-4xl font-bold gradient-text mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-400 font-medium">{stat.label}</div>
                </div>
              ))}
            </div>

            <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl p-8 border border-gray-800/50 card-glow">
              <div className="flex items-center mb-6">
                <Star className="w-6 h-6 text-yellow-400 mr-2" />
                <h3 className="text-xl font-semibold text-white">Success Stories</h3>
              </div>
              
              <div className="space-y-6">
                {testimonials.map((testimonial, index) => (
                  <div key={index} className="border-l-4 border-purple-500 pl-6">
                    <p className="text-gray-400 italic mb-4 leading-relaxed">
                      "{testimonial.quote}"
                    </p>
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                        {testimonial.image}
                      </div>
                      <div>
                        <p className="text-white font-semibold">{testimonial.author}</p>
                        <p className="text-gray-400 text-sm">{testimonial.position}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Partner Companies Section */}
        <div className="text-center">
          <h3 className="text-2xl font-bold text-white mb-8">Our Alumni Work At</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8 opacity-60">
            {['Flipkart', 'Swiggy', 'Razorpay', 'CRED', 'Zomato', 'PhonePe'].map((company) => (
              <div key={company} className="text-gray-400 font-semibold text-lg">
                {company}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;

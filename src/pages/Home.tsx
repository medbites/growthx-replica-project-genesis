
import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ExternalLink, Star, Users, Award, Briefcase, Code, Palette, Brain, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Navigation from '@/components/Navigation';

const Home = () => {
  useEffect(() => {
    const observeElements = () => {
      const elements = document.querySelectorAll('.scroll-reveal');
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('revealed');
            }
          });
        },
        { threshold: 0.1 }
      );

      elements.forEach((element) => observer.observe(element));
      return () => observer.disconnect();
    };

    const cleanup = observeElements();
    return cleanup;
  }, []);

  const featuredProjects = [
    {
      id: 'global-calcium',
      title: 'Visual Impact: Global Calcium',
      description: 'Complete brand transformation with AI-powered visual identity system and packaging redesign.',
      tags: ['Branding', 'Visual Identity', 'Packaging'],
      image: 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop',
      client: 'Global Calcium Ltd.',
      year: '2024',
      impact: '340% increase in brand recognition'
    },
    {
      id: 'velbiom',
      title: 'Velbiom – Character Design & 2D Animation',
      description: 'Character-driven brand system with animated mascots and comprehensive style guide.',
      tags: ['Character Design', 'Animation', 'Brand Systems'],
      image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600&h=400&fit=crop',
      client: 'Velbiom Studios',
      year: '2024',
      impact: '8M+ social media impressions'
    },
    {
      id: 'med-bites',
      title: 'MED-bites Branding',
      description: 'Health-focused food brand with sustainable packaging and digital-first approach.',
      tags: ['Branding', 'Packaging', 'Digital Strategy'],
      image: 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=600&h=400&fit=crop',
      client: 'MED-bites',
      year: '2023',
      impact: '250% sales growth in Q1'
    },
  ];

  const services = [
    {
      icon: Palette,
      title: 'Brand Identity Systems',
      description: 'Complete visual identity packages that tell your brand story across all touchpoints',
      features: ['Logo Design', 'Color Systems', 'Typography', 'Brand Guidelines']
    },
    {
      icon: Brain,
      title: 'AI-Powered Design',
      description: 'Cutting-edge AI tools integrated with human creativity for innovative solutions',
      features: ['Figma Automation', 'AI Prompt Engineering', 'Smart Templates', 'Data-Driven Design']
    },
    {
      icon: Code,
      title: 'Digital Experiences',
      description: 'Seamless digital interfaces that bridge brand and user experience',
      features: ['Web Design', 'Mobile UI', 'Interactive Prototypes', 'Design Systems']
    },
    {
      icon: Briefcase,
      title: 'Packaging Solutions',
      description: 'Physical brand extensions that create memorable shelf presence',
      features: ['Product Packaging', 'Label Design', 'Sustainable Materials', 'Print Production']
    }
  ];

  const stats = [
    { label: 'Projects Completed', value: '150+', icon: Award },
    { label: 'Happy Clients', value: '80+', icon: Users },
    { label: 'Years Experience', value: '8+', icon: Star },
    { label: 'Brand Systems', value: '45+', icon: Zap }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Enhanced Hero Section */}
      <section className="pt-32 pb-32 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-20 right-10 w-72 h-72 bg-brand-turquoise/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-10 w-96 h-96 bg-brand-coral/10 rounded-full blur-3xl"></div>
        </div>
        
        <div className="max-w-6xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8 scroll-reveal">
              <div className="space-y-6">
                <Badge variant="outline" className="border-brand-turquoise text-brand-turquoise px-6 py-2 text-sm font-medium">
                  ✨ Available for new projects
                </Badge>
                
                <h1 className="text-6xl md:text-8xl font-bold leading-tight">
                  <span className="brand-turquoise">Hem</span>{' '}
                  <span className="brand-coral">Prashanth</span>
                </h1>
                
                <h2 className="text-3xl md:text-4xl font-semibold brand-yellow">
                  AI Creative Identity & Brand Systems
                </h2>
                
                <p className="text-xl md:text-2xl text-muted-foreground leading-relaxed max-w-2xl">
                  Designing at the intersection of <span className="brand-turquoise font-semibold">culture</span>, 
                  <span className="brand-coral font-semibold"> clarity</span>, 
                  and <span className="brand-yellow font-semibold">code</span>.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-6">
                <Button asChild size="lg" className="bg-brand-turquoise hover:bg-brand-turquoise/90 text-background px-8 py-4 text-lg">
                  <Link to="/work">
                    View My Work
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button asChild variant="outline" size="lg" className="border-brand-coral text-brand-coral hover:bg-brand-coral hover:text-background px-8 py-4 text-lg">
                  <Link to="/contact">
                    Let's Collaborate
                  </Link>
                </Button>
              </div>

              {/* Stats Row */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-12">
                {stats.map((stat, index) => (
                  <div key={stat.label} className="text-center space-y-2" style={{ animationDelay: `${index * 0.1}s` }}>
                    <div className="flex items-center justify-center mb-2">
                      <stat.icon className="h-6 w-6 brand-turquoise" />
                    </div>
                    <div className="text-2xl md:text-3xl font-bold text-foreground">{stat.value}</div>
                    <div className="text-sm text-muted-foreground">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Visual Element */}
            <div className="relative scroll-reveal">
              <div className="relative z-10">
                <div className="bg-card/50 backdrop-blur-lg rounded-3xl p-8 border border-border shadow-2xl">
                  <div className="space-y-6">
                    <div className="flex items-center space-x-4">
                      <div className="w-16 h-16 bg-gradient-to-br from-brand-turquoise to-brand-coral rounded-2xl flex items-center justify-center">
                        <Palette className="h-8 w-8 text-background" />
                      </div>
                      <div>
                        <div className="font-semibold text-xl text-foreground">Brand Systems</div>
                        <div className="text-muted-foreground">AI-Powered Design</div>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-4 bg-brand-turquoise/10 rounded-xl border border-brand-turquoise/20">
                        <span className="brand-turquoise font-medium">Visual Identity</span>
                        <span className="brand-turquoise font-bold text-xl">98%</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-brand-coral/10 rounded-xl border border-brand-coral/20">
                        <span className="brand-coral font-medium">Brand Recognition</span>
                        <span className="brand-coral font-bold text-xl">95%</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-brand-yellow/10 rounded-xl border border-brand-yellow/20">
                        <span className="brand-yellow font-medium">Client Satisfaction</span>
                        <span className="brand-yellow font-bold text-xl">100%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20 scroll-reveal">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">What I Do</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Comprehensive design solutions that blend cutting-edge AI technology with 
              timeless design principles to create memorable brand experiences.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {services.map((service, index) => (
              <Card key={service.title} className={`group card-hover cursor-pointer scroll-reveal bg-card border-border`} style={{ animationDelay: `${index * 0.2}s` }}>
                <CardContent className="p-8">
                  <div className="flex items-start space-x-4 mb-6">
                    <div className="w-14 h-14 bg-brand-turquoise/20 rounded-xl flex items-center justify-center group-hover:bg-brand-turquoise/30 transition-colors">
                      <service.icon className="h-7 w-7 brand-turquoise" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-semibold mb-3 group-hover:brand-turquoise transition-colors">
                        {service.title}
                      </h3>
                      <p className="text-muted-foreground text-lg leading-relaxed mb-6">
                        {service.description}
                      </p>
                      <div className="space-y-2">
                        {service.features.map((feature) => (
                          <div key={feature} className="flex items-center space-x-2">
                            <div className="w-1.5 h-1.5 bg-brand-turquoise rounded-full"></div>
                            <span className="text-sm text-muted-foreground">{feature}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Featured Work Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20 scroll-reveal">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Featured Work</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              A selection of recent projects showcasing comprehensive brand systems, 
              AI-powered design solutions, and measurable business impact.
            </p>
          </div>
          
          <div className="space-y-16">
            {featuredProjects.map((project, index) => (
              <Card key={project.id} className={`group card-hover cursor-pointer scroll-reveal bg-card border-border overflow-hidden`} style={{ animationDelay: `${index * 0.2}s` }}>
                <div className={`grid lg:grid-cols-2 gap-0 ${index % 2 === 1 ? 'lg:grid-flow-col-dense' : ''}`}>
                  <div className={`relative overflow-hidden ${index % 2 === 1 ? 'lg:col-start-2' : ''}`}>
                    <img 
                      src={project.image} 
                      alt={project.title}
                      className="w-full h-80 lg:h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                      <Button variant="secondary" className="opacity-90">
                        View Case Study <ExternalLink className="ml-2 h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <div className={`p-8 lg:p-12 flex flex-col justify-center ${index % 2 === 1 ? 'lg:col-start-1' : ''}`}>
                    <div className="space-y-6">
                      <div className="flex flex-wrap gap-2 mb-4">
                        {project.tags.map((tag) => (
                          <Badge key={tag} variant="secondary" className="px-3 py-1">
                            {tag}
                          </Badge>
                        ))}
                      </div>
                      
                      <h3 className="text-3xl font-bold group-hover:brand-turquoise transition-colors">
                        {project.title}
                      </h3>
                      
                      <p className="text-lg text-muted-foreground leading-relaxed">
                        {project.description}
                      </p>
                      
                      <div className="flex items-center justify-between pt-4 border-t border-border">
                        <div className="space-y-1">
                          <div className="text-sm text-muted-foreground">Client</div>
                          <div className="font-medium">{project.client}</div>
                        </div>
                        <div className="space-y-1 text-right">
                          <div className="text-sm text-muted-foreground">Impact</div>
                          <div className="font-medium brand-turquoise">{project.impact}</div>
                        </div>
                      </div>
                      
                      <Link to={`/work/${project.id}`} className="inline-flex items-center text-brand-turquoise hover:text-brand-turquoise/80 font-medium transition-colors">
                        View Full Case Study
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Link>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
          
          <div className="text-center mt-16 scroll-reveal">
            <Button asChild variant="outline" size="lg" className="border-brand-turquoise text-brand-turquoise hover:bg-brand-turquoise hover:text-background">
              <Link to="/work">
                View All Projects
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Enhanced About Me Preview */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-muted/50">
        <div className="max-w-4xl mx-auto scroll-reveal">
          <div className="grid lg:grid-cols-3 gap-12 items-center">
            <div className="lg:col-span-2">
              <h2 className="text-4xl md:text-5xl font-bold mb-8">About Me</h2>
              <div className="space-y-6 text-lg text-muted-foreground leading-relaxed">
                <p>
                  I specialize in creating <span className="brand-turquoise font-semibold">AI-powered brand systems</span> that 
                  blend cutting-edge technology with timeless design principles. My work focuses on building 
                  cohesive visual identities that resonate across cultures while maintaining clarity and 
                  purpose in every touchpoint.
                </p>
                <p>
                  With expertise in <span className="brand-coral font-semibold">Figma, Gemini, and advanced AI tools</span>, 
                  I help brands navigate the intersection of human creativity and artificial intelligence, 
                  creating solutions that are both innovative and deeply human.
                </p>
                <p>
                  My approach centers on understanding the unique story of each brand and translating that 
                  into <span className="brand-yellow font-semibold">systematic, scalable design solutions</span> that 
                  drive measurable business impact.
                </p>
              </div>
              <Button asChild variant="outline" size="lg" className="mt-8 border-brand-yellow text-brand-yellow hover:bg-brand-yellow hover:text-background">
                <Link to="/about">
                  Read Full Story
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
            <div className="relative">
              <div className="aspect-square bg-gradient-to-br from-brand-turquoise/20 via-brand-coral/20 to-brand-yellow/20 rounded-3xl flex items-center justify-center">
                <img 
                  src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face" 
                  alt="Hem Prashanth"
                  className="w-64 h-64 object-cover rounded-2xl"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center scroll-reveal">
          <h2 className="text-4xl md:text-5xl font-bold mb-8">
            <span className="gradient-brand bg-clip-text text-transparent">
              Have a project in mind?
            </span>
          </h2>
          <p className="text-xl text-muted-foreground mb-12 max-w-2xl mx-auto">
            Let's connect and create something amazing together. From brand identity 
            to AI-powered design systems, I'm here to help bring your vision to life.
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Button asChild size="lg" className="bg-brand-coral hover:bg-brand-coral/90 text-background px-8 py-4 text-lg">
              <Link to="/contact">
                Start a Conversation
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="border-brand-turquoise text-brand-turquoise hover:bg-brand-turquoise hover:text-background px-8 py-4 text-lg">
              <Link to="/work">
                Browse Portfolio
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;

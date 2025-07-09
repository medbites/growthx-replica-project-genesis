
import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Play, Check, Sparkles, Palette, Brain, Grid, Package, Star, ExternalLink } from 'lucide-react';
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
      title: 'Global Calcium',
      description: 'Complete brand transformation with AI-powered visual identity system and packaging redesign.',
      tags: ['Brand Identity', 'AI', 'Packaging'],
      image: 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop',
      impact: '340% brand recognition increase'
    },
    {
      id: 'velbiom',
      title: 'Velbiom Studios',
      description: 'Character-driven brand system with animated mascots and comprehensive style guide.',
      tags: ['Character Design', 'Animation', 'Brand Systems'],
      image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600&h=400&fit=crop',
      impact: '8M+ social media impressions'
    },
    {
      id: 'med-bites',
      title: 'MED-bites',
      description: 'Health-focused food brand with sustainable packaging and digital-first approach.',
      tags: ['Branding', 'Packaging', 'Digital Strategy'],
      image: 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=600&h=400&fit=crop',
      impact: '250% sales growth in Q1'
    },
  ];

  const designProcess = [
    {
      icon: Sparkles,
      title: 'Discovery',
      description: 'Deep dive into brand essence, target audience, and competitive landscape to uncover unique positioning opportunities.'
    },
    {
      icon: Palette,
      title: 'Visual Exploration',
      description: 'Create multiple design directions exploring typography, color, and visual language that resonates with your audience.'
    },
    {
      icon: Brain,
      title: 'AI Enhancement',
      description: 'Leverage cutting-edge AI tools to iterate rapidly, generate variations, and push creative boundaries beyond traditional limits.'
    },
    {
      icon: Grid,
      title: 'System Delivery',
      description: 'Deliver comprehensive brand guidelines, asset libraries, and implementation roadmaps for consistent execution.'
    }
  ];

  const blogPosts = [
    {
      title: 'Designing Soul Mango with AI',
      excerpt: 'How I used Gemini and Figma to create a complete brand identity in half the time.',
      image: 'https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=400&h=300&fit=crop',
      tag: 'Case Study'
    },
    {
      title: 'Prompt Engineering for Designers',
      excerpt: 'Essential techniques for getting better results from AI design tools.',
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop',
      tag: 'Tutorial'
    },
    {
      title: 'The Future of Brand Systems',
      excerpt: 'Why AI-powered design systems are revolutionizing how brands maintain consistency.',
      image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
      tag: 'Insights'
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Hero Section */}
      <section className="pt-20 pb-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 right-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
        </div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8 scroll-reveal">
              <div className="space-y-6">
                <Badge variant="outline" className="border-purple-400/50 text-purple-300 px-4 py-2 text-sm font-medium">
                  ✨ Branding with AI-powered imagination
                </Badge>
                
                <h1 className="text-5xl md:text-7xl font-bold leading-tight text-white">
                  Build your{' '}
                  <span className="gradient-text">Visual Identity</span>
                </h1>
                
                <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl">
                  From digital-first brands to cultural storytelling—designs that resonate 
                  across touchpoints and create lasting connections with your audience.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Button asChild className="btn-gradient text-white px-8 py-4 text-lg rounded-full">
                  <Link to="/work">
                    View Work
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button asChild variant="outline" className="btn-outline px-8 py-4 text-lg rounded-full">
                  <Link to="#reel">
                    <Play className="mr-2 h-5 w-5" />
                    Watch Reel
                  </Link>
                </Button>
              </div>
            </div>

            {/* Dashboard Metrics */}
            <div className="relative scroll-reveal">
              <div className="relative z-10">
                <div className="bg-card/50 backdrop-blur-lg rounded-3xl p-8 border border-border/50 card-glow">
                  <div className="space-y-6">
                    <div className="flex items-center space-x-4">
                      <div className="w-16 h-16 gradient-purple rounded-2xl flex items-center justify-center">
                        <Palette className="h-8 w-8 text-white" />
                      </div>
                      <div>
                        <div className="font-semibold text-xl text-white">Design Dashboard</div>
                        <div className="text-muted-foreground">Live Metrics</div>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-4 bg-green-500/10 rounded-xl border border-green-500/20">
                        <span className="text-green-400 font-medium">Projects Completed</span>
                        <span className="text-green-400 font-bold text-xl">150+</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
                        <span className="text-blue-400 font-medium">Brands Designed</span>
                        <span className="text-blue-400 font-bold text-xl">80+</span>
                      </div>
                      <div className="flex justify-between items-center p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
                        <span className="text-purple-400 font-medium">AI Tools Mastered</span>
                        <span className="text-purple-400 font-bold text-xl">12+</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Work Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 scroll-reveal">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">Selected Work</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              A showcase of recent brand systems and AI-powered design solutions that drive measurable business impact.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {featuredProjects.map((project, index) => (
              <Card key={project.id} className={`group card-hover cursor-pointer scroll-reveal bg-card border-border card-glow`} style={{ animationDelay: `${index * 0.2}s` }}>
                <Link to={`/work/${project.id}`}>
                  <div className="relative overflow-hidden rounded-t-lg">
                    <img 
                      src={project.image} 
                      alt={project.title}
                      className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                      <Button variant="secondary" className="opacity-90">
                        Learn More <ExternalLink className="ml-2 h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <CardContent className="p-6">
                    <h3 className="text-2xl font-semibold mb-3 text-white group-hover:text-purple-300 transition-colors">
                      {project.title}
                    </h3>
                    <p className="text-muted-foreground mb-4 leading-relaxed">
                      {project.description}
                    </p>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {project.tags.map((tag) => (
                        <Badge key={tag} variant="secondary" className="px-3 py-1 bg-purple-500/10 text-purple-300 border-purple-500/20">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-sm text-green-400 font-medium">
                      {project.impact}
                    </div>
                  </CardContent>
                </Link>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Design Process Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 scroll-reveal">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">My Design Framework</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              A systematic approach that blends traditional design thinking with cutting-edge AI capabilities.
            </p>
          </div>
          
          <div className="space-y-8">
            {designProcess.map((step, index) => (
              <div key={step.title} className={`flex items-start space-x-6 scroll-reveal`} style={{ animationDelay: `${index * 0.2}s` }}>
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 gradient-purple rounded-xl flex items-center justify-center">
                    <step.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="flex items-center space-x-4 flex-1">
                  <Check className="h-5 w-5 text-green-400 flex-shrink-0" />
                  <div>
                    <h3 className="text-xl font-semibold text-white mb-2">{step.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">{step.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Me Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="scroll-reveal">
              <div className="relative">
                <img 
                  src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&crop=face" 
                  alt="Hem Prashanth"
                  className="w-full aspect-square object-cover rounded-3xl"
                />
                <div className="absolute -bottom-4 -right-4 bg-card border border-border rounded-2xl p-4">
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-white">7+</div>
                      <div className="text-xs text-muted-foreground">Years</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">15+</div>
                      <div className="text-xs text-muted-foreground">Brands</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-white">200+</div>
                      <div className="text-xs text-muted-foreground">Assets</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="space-y-8 scroll-reveal">
              <div>
                <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">About Me</h2>
                <p className="text-xl text-muted-foreground leading-relaxed mb-6">
                  I'm a brand system designer focused on meaning, clarity, and craft. 
                  My work bridges the gap between human creativity and artificial intelligence, 
                  creating visual identities that resonate across cultures and platforms.
                </p>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  With expertise in AI-powered design tools and systematic thinking, 
                  I help brands tell their stories through cohesive, scalable visual systems.
                </p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-card/50 p-4 rounded-xl border border-border/50">
                  <Package className="h-6 w-6 text-purple-400 mb-2" />
                  <div className="font-semibold text-white">Identity</div>
                </div>
                <div className="bg-card/50 p-4 rounded-xl border border-border/50">
                  <Brain className="h-6 w-6 text-purple-400 mb-2" />
                  <div className="font-semibold text-white">AI Tools</div>
                </div>
                <div className="bg-card/50 p-4 rounded-xl border border-border/50">
                  <Grid className="h-6 w-6 text-purple-400 mb-2" />
                  <div className="font-semibold text-white">Systems</div>
                </div>
                <div className="bg-card/50 p-4 rounded-xl border border-border/50">
                  <Palette className="h-6 w-6 text-purple-400 mb-2" />
                  <div className="font-semibold text-white">Webflow</div>
                </div>
              </div>
              
              <Button asChild variant="outline" className="btn-outline px-8 py-3 text-lg rounded-full">
                <Link to="/contact">
                  Let's Connect
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Blog Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 scroll-reveal">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">Studio Notes</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Insights, tutorials, and behind-the-scenes looks at AI-powered design processes.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {blogPosts.map((post, index) => (
              <Card key={post.title} className={`group card-hover cursor-pointer scroll-reveal bg-card border-border card-glow`} style={{ animationDelay: `${index * 0.2}s` }}>
                <div className="relative overflow-hidden rounded-t-lg">
                  <img 
                    src={post.image} 
                    alt={post.title}
                    className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <div className="absolute top-4 left-4">
                    <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30">
                      {post.tag}
                    </Badge>
                  </div>
                </div>
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold mb-3 text-white group-hover:text-purple-300 transition-colors">
                    {post.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {post.excerpt}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/30">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16">
            <div className="scroll-reveal">
              <h2 className="text-4xl md:text-5xl font-bold mb-8 text-white">
                Have a project in mind?
              </h2>
              <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
                Let's connect and create something amazing together. From brand identity 
                to AI-powered design systems, I'm here to help bring your vision to life.
              </p>
              
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center">
                    <Star className="h-6 w-6 text-purple-400" />
                  </div>
                  <div>
                    <div className="font-semibold text-white">Quick Response</div>
                    <div className="text-muted-foreground">Usually within 24 hours</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center">
                    <Brain className="h-6 w-6 text-purple-400" />
                  </div>
                  <div>
                    <div className="font-semibold text-white">AI-Enhanced Process</div>
                    <div className="text-muted-foreground">Faster iterations, better results</div>
                  </div>
                </div>
              </div>
            </div>
            
            <Card className="bg-card/50 border-border/50 card-glow scroll-reveal">
              <CardContent className="p-8">
                <form className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <input
                        type="text"
                        placeholder="Your Name"
                        className="w-full px-4 py-3 bg-background border border-border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-muted-foreground"
                      />
                    </div>
                    <div>
                      <input
                        type="email"
                        placeholder="Email Address"
                        className="w-full px-4 py-3 bg-background border border-border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-white placeholder-muted-foreground"
                      />
                    </div>
                  </div>
                  <div>
                    <textarea
                      rows={4}
                      placeholder="Tell me about your project..."
                      className="w-full px-4 py-3 bg-background border border-border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none text-white placeholder-muted-foreground"
                    />
                  </div>
                  <Button className="w-full btn-gradient text-white py-3 rounded-lg font-medium">
                    Send Message
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;

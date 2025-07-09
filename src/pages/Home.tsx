
import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
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
      tags: ['Branding', 'Visual Identity'],
      image: 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop'
    },
    {
      id: 'velbiom',
      title: 'Velbiom – Character Design & 2D Animation',
      tags: ['Character Design', 'Animation'],
      image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600&h=400&fit=crop'
    },
    {
      id: 'med-bites',
      title: 'MED-bites Branding',
      tags: ['Branding', 'Packaging'],
      image: 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=600&h=400&fit=crop'
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center scroll-reveal">
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="brand-turquoise">Hem</span>{' '}
            <span className="brand-coral">Prashanth</span>
          </h1>
          <h2 className="text-2xl md:text-3xl font-semibold mb-6 brand-yellow">
            AI Creative Identity & Brand Systems
          </h2>
          <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            Designing at the intersection of culture, clarity, and code.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="bg-brand-turquoise hover:bg-brand-turquoise/90 text-background">
              <Link to="/work">
                View My Work
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="border-brand-coral text-brand-coral hover:bg-brand-coral hover:text-background">
              <Link to="/contact">
                Let's Collaborate
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Featured Work Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 scroll-reveal">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Featured Work</h2>
            <p className="text-lg text-muted-foreground">
              A selection of recent projects showcasing brand systems and visual identity
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredProjects.map((project, index) => (
              <Card key={project.id} className={`group card-hover cursor-pointer scroll-reveal bg-card border-border`} style={{ animationDelay: `${index * 0.2}s` }}>
                <div className="relative overflow-hidden rounded-t-lg">
                  <img 
                    src={project.image} 
                    alt={project.title}
                    className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <Button variant="secondary" className="opacity-90">
                      View Case <ExternalLink className="ml-2 h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold mb-3">{project.title}</h3>
                  <div className="flex flex-wrap gap-2">
                    {project.tags.map((tag) => (
                      <span key={tag} className="px-3 py-1 bg-muted text-sm rounded-full">
                        {tag}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* About Me Preview */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-muted/50">
        <div className="max-w-4xl mx-auto text-center scroll-reveal">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">About Me</h2>
          <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
            I specialize in creating AI-powered brand systems that blend cutting-edge technology with 
            timeless design principles. My work focuses on building cohesive visual identities that 
            resonate across cultures while maintaining clarity and purpose in every touchpoint.
          </p>
          <Button asChild variant="outline" size="lg" className="border-brand-yellow text-brand-yellow hover:bg-brand-yellow hover:text-background">
            <Link to="/about">
              Read More
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center scroll-reveal">
          <h2 className="text-3xl md:text-4xl font-bold mb-6 gradient-brand bg-clip-text text-transparent">
            Have a project in mind?
          </h2>
          <p className="text-lg text-muted-foreground mb-8">
            Let's connect and create something amazing together.
          </p>
          <Button asChild size="lg" className="bg-brand-coral hover:bg-brand-coral/90 text-background">
            <Link to="/contact">
              Start a Conversation
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;


import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ExternalLink, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const Work = () => {
  const [activeFilter, setActiveFilter] = useState('All');

  const filters = ['All', 'Branding', 'Packaging', 'AI Design', 'Identity Systems'];

  const projects = [
    {
      id: 'global-calcium',
      title: 'Visual Impact: Global Calcium',
      category: 'Branding',
      tags: ['Branding', 'Visual Identity'],
      image: 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=600&h=400&fit=crop',
      year: '2024'
    },
    {
      id: 'velbiom',
      title: 'Velbiom Character Design',
      category: 'Identity Systems',
      tags: ['Character Design', 'Animation'],
      image: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600&h=400&fit=crop',
      year: '2024'
    },
    {
      id: 'med-bites',
      title: 'MED-bites Branding',
      category: 'Packaging',
      tags: ['Branding', 'Packaging'],
      image: 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=600&h=400&fit=crop',
      year: '2023'
    },
    {
      id: 'soul-mango',
      title: 'Soul Mango AI Branding',
      category: 'AI Design',
      tags: ['AI Design', 'Branding'],
      image: 'https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=600&h=400&fit=crop',
      year: '2024'
    },
    {
      id: 'tech-startup',
      title: 'Tech Startup Identity',
      category: 'Identity Systems',
      tags: ['Identity Systems', 'Digital'],
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop',
      year: '2023'
    },
    {
      id: 'eco-packaging',
      title: 'Eco-Friendly Packaging',
      category: 'Packaging',
      tags: ['Packaging', 'Sustainability'],
      image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop',
      year: '2024'
    }
  ];

  const filteredProjects = activeFilter === 'All' 
    ? projects 
    : projects.filter(project => project.category === activeFilter);

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Header */}
      <section className="pt-32 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">My Work</h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              A collection of brand systems, visual identities, and AI-powered design solutions
            </p>
          </div>

          {/* Filter Buttons */}
          <div className="flex flex-wrap justify-center gap-3 mb-12">
            {filters.map((filter) => (
              <Button
                key={filter}
                variant={activeFilter === filter ? "default" : "outline"}
                onClick={() => setActiveFilter(filter)}
                className={activeFilter === filter 
                  ? "bg-brand-turquoise hover:bg-brand-turquoise/90 text-background" 
                  : "border-border hover:border-brand-turquoise hover:text-brand-turquoise"
                }
              >
                <Filter className="mr-2 h-4 w-4" />
                {filter}
              </Button>
            ))}
          </div>
        </div>
      </section>

      {/* Projects Grid */}
      <section className="pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {filteredProjects.map((project, index) => (
              <Card key={project.id} className="group card-hover cursor-pointer bg-card border-border">
                <Link to={`/work/${project.id}`}>
                  <div className="relative overflow-hidden rounded-t-lg">
                    <img 
                      src={project.image} 
                      alt={project.title}
                      className="w-full h-80 object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                      <Button variant="secondary" className="opacity-90">
                        View Case Study <ExternalLink className="ml-2 h-4 w-4" />
                      </Button>
                    </div>
                    <div className="absolute top-4 right-4 bg-background/90 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium">
                      {project.year}
                    </div>
                  </div>
                  <CardContent className="p-6">
                    <h3 className="text-2xl font-semibold mb-3 group-hover:brand-turquoise transition-colors">
                      {project.title}
                    </h3>
                    <div className="flex flex-wrap gap-2 mb-4">
                      {project.tags.map((tag) => (
                        <span key={tag} className="px-3 py-1 bg-muted text-sm rounded-full">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <p className="text-muted-foreground text-sm">
                      {project.category} • {project.year}
                    </p>
                  </CardContent>
                </Link>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Work;

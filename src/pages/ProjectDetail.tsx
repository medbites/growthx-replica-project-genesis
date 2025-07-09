
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const ProjectDetail = () => {
  const { id } = useParams();

  // Mock project data - in a real app, this would come from an API or CMS
  const projectData = {
    'global-calcium': {
      title: 'Visual Impact: Global Calcium',
      client: 'Global Calcium Ltd.',
      year: '2024',
      role: 'Brand Designer & Visual Strategist',
      coverImage: 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=1200&h=600&fit=crop',
      overview: 'Global Calcium needed a complete brand overhaul to position themselves as industry leaders in sustainable calcium production. The challenge was creating a visual identity that communicated both scientific credibility and environmental responsibility.',
      tools: ['Figma', 'Gemini AI', 'Adobe Creative Suite', 'Principle'],
      sections: [
        {
          title: 'Brand Strategy',
          content: 'We began with extensive research into the calcium industry and competitor analysis. The strategy focused on highlighting innovation while maintaining trust and reliability.',
          images: ['https://images.unsplash.com/photo-1553484771-371a605b060b?w=800&h=500&fit=crop']
        },
        {
          title: 'Visual Identity',
          content: 'The logo combines molecular structures with clean typography, representing the scientific foundation of the brand while remaining approachable and modern.',
          images: ['https://images.unsplash.com/photo-1572044162444-ad60f128bdea?w=800&h=500&fit=crop']
        },
        {
          title: 'Brand Applications',
          content: 'The system was applied across packaging, digital platforms, and corporate materials, ensuring consistency at every touchpoint.',
          images: ['https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=800&h=500&fit=crop']
        }
      ],
      outcome: '40% increase in brand recognition and 25% improvement in customer trust metrics within 6 months of launch.',
      takeaways: [
        'Scientific credibility and approachability can coexist in visual design',
        'AI tools accelerate concept exploration while maintaining design quality',
        'Systematic approach to brand applications ensures long-term consistency'
      ]
    }
  };

  const project = projectData[id as keyof typeof projectData];

  if (!project) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Project Not Found</h1>
          <Button asChild>
            <Link to="/work">Back to Work</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Hero Section */}
      <section className="pt-32 pb-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <Button asChild variant="ghost" className="mb-6 hover:brand-turquoise">
            <Link to="/work">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Work
            </Link>
          </Button>
          
          <div className="relative mb-8">
            <img 
              src={project.coverImage} 
              alt={project.title}
              className="w-full h-96 md:h-[500px] object-cover rounded-2xl"
            />
          </div>

          <div className="grid lg:grid-cols-3 gap-12">
            <div className="lg:col-span-2">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">{project.title}</h1>
              <p className="text-lg text-muted-foreground leading-relaxed">
                {project.overview}
              </p>
            </div>
            
            <div className="space-y-6">
              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <h3 className="font-semibold mb-4">Project Details</h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <span className="text-muted-foreground">Client:</span>
                      <p className="font-medium">{project.client}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Year:</span>
                      <p className="font-medium">{project.year}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Role:</span>
                      <p className="font-medium">{project.role}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Tools:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {project.tools.map((tool) => (
                          <span key={tool} className="px-2 py-1 bg-muted rounded text-xs">
                            {tool}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Process Sections */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto space-y-16">
          {project.sections.map((section, index) => (
            <div key={index}>
              <h2 className="text-3xl font-bold mb-6">{section.title}</h2>
              <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
                {section.content}
              </p>
              <div className="grid gap-6">
                {section.images.map((image, imageIndex) => (
                  <img 
                    key={imageIndex}
                    src={image} 
                    alt={`${section.title} ${imageIndex + 1}`}
                    className="w-full rounded-xl"
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Outcome */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 bg-muted/50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-6">Outcome</h2>
          <p className="text-lg leading-relaxed mb-8">
            {project.outcome}
          </p>
        </div>
      </section>

      {/* Takeaways */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-6">Key Takeaways</h2>
          <div className="space-y-4">
            {project.takeaways.map((takeaway, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="w-6 h-6 bg-brand-turquoise/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <div className="w-2 h-2 bg-brand-turquoise rounded-full"></div>
                </div>
                <p className="text-lg">{takeaway}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Navigation */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 border-t border-border">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <Button asChild variant="outline">
            <Link to="/work">
              <ArrowLeft className="mr-2 h-4 w-4" />
              All Projects
            </Link>
          </Button>
          <Button asChild className="bg-brand-coral hover:bg-brand-coral/90 text-background">
            <Link to="/contact">
              Start Your Project
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default ProjectDetail;

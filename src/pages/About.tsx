
import { Link } from 'react-router-dom';
import { ArrowRight, Palette, Brain, Grid, Package } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const About = () => {
  const skills = [
    {
      icon: Palette,
      title: 'Branding',
      description: 'Creating cohesive visual identities that tell compelling brand stories',
      color: 'brand-turquoise'
    },
    {
      icon: Brain,
      title: 'AI Tools',
      description: 'Leveraging Figma, Gemini, and cutting-edge AI for design innovation',
      color: 'brand-coral'
    },
    {
      icon: Grid,
      title: 'Visual Systems',
      description: 'Developing scalable design systems that maintain consistency across touchpoints',
      color: 'brand-yellow'
    },
    {
      icon: Package,
      title: 'Packaging Design',
      description: 'Crafting packaging solutions that connect with consumers at shelf level',
      color: 'brand-turquoise'
    }
  ];

  const testimonials = [
    {
      quote: "Hem's approach to AI-powered branding is revolutionary. He delivered a complete brand system that exceeded our expectations.",
      author: "Sarah Chen",
      role: "Marketing Director, Global Calcium",
      company: "Global Calcium Ltd."
    },
    {
      quote: "The character design work for Velbiom was exceptional. Hem brought our vision to life with incredible attention to detail.",
      author: "Michael Rodriguez",
      role: "Creative Director",
      company: "Velbiom Studios"
    },
    {
      quote: "Working with Hem on our packaging redesign was seamless. His systematic approach and creative solutions were exactly what we needed.",
      author: "Anna Thompson",
      role: "Brand Manager",
      company: "MED-bites"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Header */}
      <section className="pt-32 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold mb-6">
                About <span className="brand-turquoise">Me</span>
              </h1>
              <div className="prose prose-lg text-muted-foreground space-y-6">
                <p>
                  I'm Hem Prashanth, a visual designer specializing in AI-powered brand systems 
                  and creative identity solutions. With a passion for blending technology with 
                  timeless design principles, I help brands create meaningful connections with 
                  their audiences.
                </p>
                <p>
                  My approach centers on the intersection of culture, clarity, and code. I believe 
                  that great design should not only look beautiful but also function seamlessly 
                  across all touchpoints, telling a cohesive story that resonates with people 
                  from diverse backgrounds.
                </p>
                <p>
                  Working with cutting-edge AI tools like Figma and Gemini, I push the boundaries 
                  of what's possible in visual design while maintaining the human touch that makes 
                  brands truly memorable.
                </p>
              </div>
              <Button asChild className="mt-8 bg-brand-coral hover:bg-brand-coral/90 text-background">
                <Link to="/contact">
                  Let's Work Together
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
            <div className="relative">
              <div className="aspect-square bg-gradient-to-br from-brand-turquoise/20 to-brand-coral/20 rounded-2xl flex items-center justify-center">
                <img 
                  src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&crop=face" 
                  alt="Hem Prashanth"
                  className="w-80 h-80 object-cover rounded-xl"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Skills Grid */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Skills & Expertise</h2>
            <p className="text-lg text-muted-foreground">
              Core competencies that drive my design practice
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {skills.map((skill, index) => (
              <Card key={skill.title} className="bg-card border-border card-hover">
                <CardContent className="p-6 text-center">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-xl bg-${skill.color}/20 flex items-center justify-center`}>
                    <skill.icon className={`h-8 w-8 ${skill.color}`} />
                  </div>
                  <h3 className="text-xl font-semibold mb-3">{skill.title}</h3>
                  <p className="text-muted-foreground">{skill.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">What Clients Say</h2>
            <p className="text-lg text-muted-foreground">
              Feedback from collaborative partnerships
            </p>
          </div>
          
          <div className="grid lg:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="bg-card border-border">
                <CardContent className="p-6">
                  <p className="text-muted-foreground mb-6 italic">
                    "{testimonial.quote}"
                  </p>
                  <div>
                    <p className="font-semibold">{testimonial.author}</p>
                    <p className="text-sm text-muted-foreground">{testimonial.role}</p>
                    <p className="text-sm brand-turquoise">{testimonial.company}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;

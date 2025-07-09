
import { useState } from 'react';
import { Mail, Linkedin, ExternalLink, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import Navigation from '@/components/Navigation';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    projectType: '',
    message: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    // Handle form submission here
  };

  const projectTypes = [
    'Branding & Identity',
    'Packaging Design',
    'AI Design Systems',
    'Character Design',
    'Visual Strategy',
    'Other'
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Header */}
      <section className="pt-32 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Let's <span className="brand-turquoise">Talk</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Freelance, collaborations, brand systems — open to ideas. 
            Ready to create something amazing together?
          </p>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-12">
            {/* Contact Form */}
            <div className="lg:col-span-2">
              <Card className="bg-card border-border">
                <CardContent className="p-8">
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <Label htmlFor="name" className="text-sm font-medium mb-2 block">
                          Name *
                        </Label>
                        <Input
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleInputChange}
                          placeholder="Your full name"
                          required
                          className="bg-background border-border"
                        />
                      </div>
                      <div>
                        <Label htmlFor="email" className="text-sm font-medium mb-2 block">
                          Email *
                        </Label>
                        <Input
                          type="email"
                          id="email"
                          name="email"
                          value={formData.email}
                          onChange={handleInputChange}
                          placeholder="your@email.com"
                          required
                          className="bg-background border-border"
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="projectType" className="text-sm font-medium mb-2 block">
                        Project Type
                      </Label>
                      <select
                        id="projectType"
                        name="projectType"
                        value={formData.projectType}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 bg-background border border-border rounded-md focus:ring-2 focus:ring-brand-turquoise focus:border-transparent"
                      >
                        <option value="">Select project type</option>
                        {projectTypes.map((type) => (
                          <option key={type} value={type}>{type}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <Label htmlFor="message" className="text-sm font-medium mb-2 block">
                        Message *
                      </Label>
                      <textarea
                        id="message"
                        name="message"
                        rows={6}
                        value={formData.message}
                        onChange={handleInputChange}
                        placeholder="Tell me about your project, goals, timeline, and any specific requirements..."
                        required
                        className="w-full px-3 py-2 bg-background border border-border rounded-md focus:ring-2 focus:ring-brand-turquoise focus:border-transparent resize-none"
                      />
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-brand-turquoise hover:bg-brand-turquoise/90 text-background"
                    >
                      Send Message
                      <Send className="ml-2 h-4 w-4" />
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Contact Info */}
            <div className="space-y-6">
              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold mb-4">Get in Touch</h3>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-brand-turquoise/20 rounded-lg flex items-center justify-center">
                        <Mail className="h-5 w-5 brand-turquoise" />
                      </div>
                      <div>
                        <p className="font-medium">Email</p>
                        <p className="text-muted-foreground text-sm">hem@example.com</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-brand-coral/20 rounded-lg flex items-center justify-center">
                        <Linkedin className="h-5 w-5 brand-coral" />
                      </div>
                      <div>
                        <p className="font-medium">LinkedIn</p>
                        <p className="text-muted-foreground text-sm">@hemprashanth</p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-brand-yellow/20 rounded-lg flex items-center justify-center">
                        <ExternalLink className="h-5 w-5 brand-yellow" />
                      </div>
                      <div>
                        <p className="font-medium">Behance</p>
                        <p className="text-muted-foreground text-sm">@hemprashanth</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-card border-border">
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold mb-4">Response Time</h3>
                  <p className="text-muted-foreground">
                    I typically respond to inquiries within 24-48 hours. 
                    For urgent projects, feel free to mention it in your message.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;

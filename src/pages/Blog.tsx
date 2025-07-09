
import { Link } from 'react-router-dom';
import { Calendar, ArrowRight, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Navigation from '@/components/Navigation';

const Blog = () => {
  const blogPosts = [
    {
      id: 'designing-soul-mango-ai',
      title: 'Designing Soul Mango with AI',
      excerpt: 'How I leveraged Gemini AI and modern design tools to create a complete brand identity for a tropical beverage startup.',
      image: 'https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=600&h=400&fit=crop',
      date: '2024-01-15',
      readTime: '8 min read',
      tags: ['AI Design', 'Branding', 'Case Study']
    },
    {
      id: 'prompt-engineering-designers',
      title: 'Prompt Engineering for Designers',
      excerpt: 'A comprehensive guide to crafting effective prompts for AI design tools, with practical examples and best practices.',
      image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&h=400&fit=crop',
      date: '2024-01-08',
      readTime: '12 min read',
      tags: ['AI Tools', 'Tutorial', 'Workflow']
    },
    {
      id: 'future-brand-systems',
      title: 'The Future of Brand Systems',
      excerpt: 'Exploring how AI and automation are reshaping the way we think about scalable design systems and brand consistency.',
      image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=400&fit=crop',
      date: '2023-12-22',
      readTime: '6 min read',
      tags: ['Brand Systems', 'Future Tech', 'Opinion']
    }
  ];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      {/* Header */}
      <section className="pt-32 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Studio <span className="brand-turquoise">Log</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Insights, tutorials, and thoughts on AI-powered design, brand systems, 
            and the future of visual identity.
          </p>
        </div>
      </section>

      {/* Blog Posts */}
      <section className="pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="space-y-12">
            {blogPosts.map((post, index) => (
              <Card key={post.id} className="group card-hover cursor-pointer bg-card border-border overflow-hidden">
                <Link to={`/blog/${post.id}`}>
                  <div className="grid md:grid-cols-5 gap-0">
                    <div className="md:col-span-2">
                      <img 
                        src={post.image} 
                        alt={post.title}
                        className="w-full h-64 md:h-full object-cover transition-transform duration-300 group-hover:scale-105"
                      />
                    </div>
                    <div className="md:col-span-3">
                      <CardContent className="p-8 h-full flex flex-col justify-between">
                        <div>
                          <div className="flex items-center space-x-4 text-sm text-muted-foreground mb-4">
                            <div className="flex items-center space-x-1">
                              <Calendar className="h-4 w-4" />
                              <span>{formatDate(post.date)}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Clock className="h-4 w-4" />
                              <span>{post.readTime}</span>
                            </div>
                          </div>
                          
                          <h2 className="text-2xl md:text-3xl font-bold mb-4 group-hover:brand-turquoise transition-colors">
                            {post.title}
                          </h2>
                          
                          <p className="text-muted-foreground mb-6 leading-relaxed">
                            {post.excerpt}
                          </p>
                          
                          <div className="flex flex-wrap gap-2 mb-6">
                            {post.tags.map((tag) => (
                              <span key={tag} className="px-3 py-1 bg-muted text-sm rounded-full">
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                        
                        <div className="flex items-center text-brand-turquoise font-medium group-hover:underline">
                          Read Article
                          <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                        </div>
                      </CardContent>
                    </div>
                  </div>
                </Link>
              </Card>
            ))}
          </div>

          {/* Load More */}
          <div className="text-center mt-16">
            <Button variant="outline" className="border-brand-turquoise text-brand-turquoise hover:bg-brand-turquoise hover:text-background">
              Load More Articles
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Blog;


import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Calendar, Clock, Share2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Navigation from '@/components/Navigation';

const BlogDetail = () => {
  const { id } = useParams();

  // Mock blog post data
  const blogPost = {
    title: 'Designing Soul Mango with AI',
    date: '2024-01-15',
    readTime: '8 min read',
    image: 'https://images.unsplash.com/photo-1611348586804-61bf6c080437?w=1200&h=600&fit=crop',
    tags: ['AI Design', 'Branding', 'Case Study'],
    content: `
      <p>When Soul Mango approached me to create their brand identity, I knew this would be the perfect opportunity to showcase how AI can enhance the creative process without replacing human intuition and creativity.</p>
      
      <h2>The Challenge</h2>
      <p>Soul Mango is a tropical beverage startup focused on authentic mango flavors sourced directly from small farms. They needed a brand that would communicate freshness, authenticity, and premium quality while standing out in a crowded market.</p>
      
      <h2>AI-Powered Ideation</h2>
      <p>I started the process by using Gemini AI to explore various conceptual directions. Instead of replacing my creative thinking, the AI served as a brainstorming partner, helping me rapidly explore different visual metaphors and brand positioning strategies.</p>
      
      <h2>The Design Process</h2>
      <p>The final brand system combines organic shapes inspired by mango forms with a vibrant color palette that evokes tropical sunsets. Every element was carefully crafted to tell the story of authenticity and premium quality.</p>
      
      <h2>Results and Impact</h2>
      <p>The brand launched to positive reception, with early customer feedback highlighting the premium feel and memorable visual identity. The systematic approach to brand development ensured consistency across all touchpoints.</p>
      
      <h2>Key Learnings</h2>
      <p>This project reinforced my belief that AI is most powerful when used as a creative amplifier rather than a replacement for human creativity. The combination of AI-powered exploration and human curation leads to stronger, more resonant design solutions.</p>
    `
  };

  const relatedPosts = [
    {
      id: 'prompt-engineering-designers',
      title: 'Prompt Engineering for Designers',
      image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=300&h=200&fit=crop'
    },
    {
      id: 'future-brand-systems',
      title: 'The Future of Brand Systems',
      image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=300&h=200&fit=crop'
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
      <section className="pt-32 pb-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <Button asChild variant="ghost" className="mb-6 hover:brand-turquoise">
            <Link to="/blog">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Blog
            </Link>
          </Button>
          
          <div className="mb-8">
            <img 
              src={blogPost.image} 
              alt={blogPost.title}
              className="w-full h-96 object-cover rounded-2xl"
            />
          </div>

          <div className="flex items-center space-x-4 text-sm text-muted-foreground mb-6">
            <div className="flex items-center space-x-1">
              <Calendar className="h-4 w-4" />
              <span>{formatDate(blogPost.date)}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4" />
              <span>{blogPost.readTime}</span>
            </div>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold mb-6">{blogPost.title}</h1>
          
          <div className="flex flex-wrap gap-2 mb-8">
            {blogPost.tags.map((tag) => (
              <span key={tag} className="px-3 py-1 bg-muted text-sm rounded-full">
                {tag}
              </span>
            ))}
          </div>

          <div className="flex items-center justify-between border-b border-border pb-8 mb-12">
            <div className="text-sm text-muted-foreground">
              By Hem Prashanth
            </div>
            <Button variant="outline" size="sm">
              <Share2 className="mr-2 h-4 w-4" />
              Share
            </Button>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div 
            className="prose prose-lg max-w-none prose-headings:font-bold prose-headings:text-foreground prose-p:text-muted-foreground prose-p:leading-relaxed prose-h2:text-2xl prose-h2:mt-12 prose-h2:mb-6"
            dangerouslySetInnerHTML={{ __html: blogPost.content }}
          />
        </div>
      </section>

      {/* Related Posts */}
      <section className="py-12 px-4 sm:px-6 lg:px-8 border-t border-border">
        <div className="max-w-4xl mx-auto">
          <h3 className="text-2xl font-bold mb-8">Related Articles</h3>
          <div className="grid md:grid-cols-2 gap-6">
            {relatedPosts.map((post) => (
              <Link key={post.id} to={`/blog/${post.id}`} className="group">
                <div className="bg-card border border-border rounded-lg overflow-hidden card-hover">
                  <img 
                    src={post.image} 
                    alt={post.title}
                    className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                  <div className="p-6">
                    <h4 className="text-lg font-semibold group-hover:brand-turquoise transition-colors">
                      {post.title}
                    </h4>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default BlogDetail;

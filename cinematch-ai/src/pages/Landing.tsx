import { Link } from "react-router-dom";
import { Search, Sparkles, Radio, Dna, Gem, Users, ArrowRight, Play, Check } from "lucide-react";
import heroImage from "@/assets/hero-movies.jpg";

const features = [
  { icon: Sparkles, title: "Hybrid AI Recommendations", desc: "Deep learning meets collaborative filtering for eerily accurate picks." },
  { icon: Radio, title: "Vibe Engine", desc: "Context-aware suggestions based on your mood, time, and weather." },
  { icon: Search, title: "Live Streaming Availability", desc: "Real-time data across every platform. No more app-hopping." },
  { icon: Dna, title: "Cinematic DNA Profile", desc: "A unique taste fingerprint built from your entire watch history." },
  { icon: Gem, title: "Hidden Gems Detector", desc: "Surface critically-loved films that flew under the radar." },
  { icon: Users, title: "Watch Together Mode", desc: "Find the perfect movie for any group in seconds." },
];

const pricing = [
  { name: "Free", price: "$0", period: "/forever", features: ["5 recommendations/day", "Basic streaming info", "Public DNA profile", "Community access"], cta: "Get Started", highlighted: false },
  { name: "Pro", price: "$9", period: "/month", features: ["Unlimited recommendations", "All streaming platforms", "Advanced DNA analytics", "Watch Together", "Hidden Gems alerts", "Priority API access"], cta: "Start Free Trial", highlighted: true },
  { name: "Enterprise", price: "$49", period: "/month", features: ["Everything in Pro", "Team analytics", "Custom API limits", "Dedicated support", "White-label options"], cta: "Contact Sales", highlighted: false },
];

const Landing = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-[hsl(var(--glass-border))] bg-background/80 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-gradient-gold">CineMatch</Link>
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors duration-300">Features</a>
            <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors duration-300">Pricing</a>
            <span className="text-muted-foreground hover:text-foreground transition-colors duration-300 cursor-pointer">API</span>
            <span className="text-muted-foreground hover:text-foreground transition-colors duration-300 cursor-pointer">GitHub</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/login" className="btn-ghost-cinema text-sm hidden sm:inline-flex">Sign In</Link>
            <Link to="/signup" className="btn-gold text-sm">Get Started Free</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        <div className="orb w-96 h-96 bg-gold top-20 -left-48" />
        <div className="orb w-72 h-72 bg-cinema-red top-40 right-10" />
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-12">
          <div className="flex-1 animate-fade-in">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight mb-6">
              <span className="text-gradient-gold">Discover Movies</span>
              <br />
              <span className="text-foreground">That Actually Match</span>
              <br />
              <span className="text-foreground">Your Soul</span>
            </h1>
            <p className="text-lg text-muted-foreground max-w-lg mb-8">
              AI-powered recommendations with real-time streaming availability. Stop scrolling. Start watching.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/signup" className="btn-gold inline-flex items-center gap-2">
                Find My Movies <ArrowRight className="w-4 h-4" />
              </Link>
              <button className="btn-ghost-cinema inline-flex items-center gap-2">
                <Play className="w-4 h-4" /> Watch Demo
              </button>
            </div>
          </div>
          <div className="flex-1 relative animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
            <div className="relative w-full max-w-lg mx-auto">
              <div className="animate-float rounded-lg overflow-hidden shadow-2xl border border-[hsl(var(--glass-border))]">
                <img src={heroImage} alt="Cinematic movie posters" className="w-full h-auto" />
              </div>
              <div className="absolute -top-4 -right-4 w-20 h-28 rounded-lg glass-card animate-float-delayed overflow-hidden opacity-80" />
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Intelligence Meets Cinema</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">Every feature is designed to make your movie discovery feel effortless and deeply personal.</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <div key={f.title} className="glass-card-hover p-6 opacity-0 animate-fade-in-up" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="w-12 h-12 rounded-xl bg-[hsl(var(--cinema-gold)/0.1)] flex items-center justify-center mb-4">
                  <f.icon className="w-6 h-6 text-gold" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Simple, Transparent Pricing</h2>
            <p className="text-muted-foreground">Start free. Upgrade when you're ready.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {pricing.map((plan) => (
              <div key={plan.name} className={`glass-card p-8 flex flex-col ${plan.highlighted ? "border-gold glow-gold scale-105 relative z-10" : ""}`}>
                {plan.highlighted && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gold text-background text-xs font-bold px-4 py-1 rounded-full">
                    Most Popular
                  </span>
                )}
                <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="text-muted-foreground">{plan.period}</span>
                </div>
                <ul className="space-y-3 mb-8 flex-1">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm">
                      <Check className="w-4 h-4 text-cinema-teal flex-shrink-0" />
                      <span className="text-muted-foreground">{f}</span>
                    </li>
                  ))}
                </ul>
                <Link to="/signup" className={plan.highlighted ? "btn-gold text-center" : "btn-ghost-cinema text-center"}>
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[hsl(var(--glass-border))] py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <span className="text-gradient-gold font-bold text-lg">CineMatch</span>
          <p className="text-sm text-muted-foreground">© 2026 CineMatch AI. All rights reserved.</p>
          <div className="flex gap-6 text-sm text-muted-foreground">
            <span className="hover:text-foreground cursor-pointer transition-colors">Privacy</span>
            <span className="hover:text-foreground cursor-pointer transition-colors">Terms</span>
            <span className="hover:text-foreground cursor-pointer transition-colors">Contact</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;

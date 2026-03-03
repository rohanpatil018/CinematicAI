import { Link } from "react-router-dom";
import { useState } from "react";

const genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror", "Romance", "Thriller", "Documentary", "Animation", "Fantasy"];

const Signup = () => {
  const [selected, setSelected] = useState<string[]>([]);

  const toggle = (g: string) => {
    setSelected((prev) => prev.includes(g) ? prev.filter((x) => x !== g) : [...prev, g]);
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-cinema-teal -top-40 -left-40" />
      <div className="orb w-64 h-64 bg-gold bottom-10 -right-32" />

      <div className="glass-card w-full max-w-md p-8 animate-scale-in relative z-10">
        <Link to="/" className="text-2xl font-bold text-gradient-gold block text-center mb-2">CineMatch</Link>
        <p className="text-center text-muted-foreground text-sm mb-8">Create your account and build your Cinematic DNA.</p>

        <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Email</label>
            <input type="email" placeholder="you@example.com" className="w-full h-11 rounded-lg bg-muted border border-[hsl(var(--glass-border))] px-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Password</label>
            <input type="password" placeholder="••••••••" className="w-full h-11 rounded-lg bg-muted border border-[hsl(var(--glass-border))] px-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Confirm Password</label>
            <input type="password" placeholder="••••••••" className="w-full h-11 rounded-lg bg-muted border border-[hsl(var(--glass-border))] px-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Preferred Genres</label>
            <div className="flex flex-wrap gap-2">
              {genres.map((g) => (
                <button
                  key={g}
                  type="button"
                  onClick={() => toggle(g)}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-300 ${
                    selected.includes(g)
                      ? "bg-gold text-background border-gold"
                      : "border-[hsl(var(--glass-border))] text-muted-foreground hover:border-gold hover:text-foreground"
                  }`}
                >
                  {g}
                </button>
              ))}
            </div>
          </div>
          <Link to="/dashboard" className="btn-gold w-full block text-center">Create Account</Link>
        </form>

        <p className="text-center text-sm text-muted-foreground mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-gold hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;

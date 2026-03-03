import { Link } from "react-router-dom";
import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";

const Login = () => {
  const [showPass, setShowPass] = useState(false);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-gold -top-40 -right-40" />
      <div className="orb w-64 h-64 bg-cinema-red bottom-20 -left-32" />

      <div className="glass-card w-full max-w-md p-8 animate-scale-in relative z-10">
        <Link to="/" className="text-2xl font-bold text-gradient-gold block text-center mb-2">CineMatch</Link>
        <p className="text-center text-muted-foreground text-sm mb-8">Welcome back. Let's find your next favorite film.</p>

        <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Email</label>
            <input type="email" placeholder="you@example.com" className="w-full h-11 rounded-lg bg-muted border border-[hsl(var(--glass-border))] px-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1.5 block">Password</label>
            <div className="relative">
              <input type={showPass ? "text" : "password"} placeholder="••••••••" className="w-full h-11 rounded-lg bg-muted border border-[hsl(var(--glass-border))] px-4 pr-10 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors" />
              <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
                {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <div className="flex items-center justify-between text-sm">
            <label className="flex items-center gap-2 text-muted-foreground">
              <input type="checkbox" className="rounded" /> Remember me
            </label>
            <span className="text-gold cursor-pointer hover:underline">Forgot password?</span>
          </div>
          <Link to="/dashboard" className="btn-gold w-full block text-center">Sign In</Link>
        </form>

        <p className="text-center text-sm text-muted-foreground mt-6">
          Don't have an account?{" "}
          <Link to="/signup" className="text-gold hover:underline">Create one</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;

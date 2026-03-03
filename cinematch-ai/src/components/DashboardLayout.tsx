import { Outlet, Link, useLocation } from "react-router-dom";
import { Home, Search, Gem, Users, User, Settings, BarChart3, LogOut, Menu, X } from "lucide-react";
import { useState } from "react";
import MoodSelector from "./MoodSelector";

const navItems = [
  { label: "Home", icon: Home, path: "/dashboard" },
  { label: "Discover", icon: Search, path: "/dashboard/discover" },
  { label: "Hidden Gems", icon: Gem, path: "/dashboard/discover" },
  { label: "Watch Together", icon: Users, path: "/dashboard/watch-together" },
  { label: "My Profile", icon: User, path: "/dashboard/profile" },
  { label: "Settings", icon: Settings, path: "/dashboard/profile" },
  { label: "Admin", icon: BarChart3, path: "/dashboard/admin" },
];

const DashboardLayout = () => {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background flex">
      {/* Mobile overlay */}
      {sidebarOpen && <div className="fixed inset-0 bg-background/60 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />}

      {/* Sidebar */}
      <aside className={`fixed lg:sticky top-0 left-0 z-50 h-screen w-60 bg-card border-r border-[hsl(var(--glass-border))] flex flex-col transition-transform duration-300 ${sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}`}>
        <div className="h-16 flex items-center px-6 border-b border-[hsl(var(--glass-border))]">
          <Link to="/" className="text-xl font-bold text-gradient-gold">CineMatch</Link>
        </div>
        <nav className="flex-1 py-4 px-3 space-y-1">
          {navItems.map((item) => {
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.label}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-300 ${
                  active ? "sidebar-active text-gold font-medium" : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
                }`}
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        <div className="p-3 border-t border-[hsl(var(--glass-border))]">
          <Link to="/" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-muted-foreground hover:text-foreground transition-colors">
            <LogOut className="w-4 h-4" /> Logout
          </Link>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top nav */}
        <header className="sticky top-0 z-30 h-16 border-b border-[hsl(var(--glass-border))] bg-background/80 backdrop-blur-lg flex items-center px-4 lg:px-6 gap-4">
          <button className="lg:hidden text-muted-foreground" onClick={() => setSidebarOpen(true)}>
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          <div className="flex-1 max-w-xl">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input placeholder="Search movies, actors, directors..." className="w-full h-10 rounded-full bg-muted border border-[hsl(var(--glass-border))] pl-10 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors" />
            </div>
          </div>
          <MoodSelector />
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-gold text-background">Pro</span>
            <div className="w-8 h-8 rounded-full bg-muted border border-[hsl(var(--glass-border))] flex items-center justify-center text-sm font-medium">R</div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;

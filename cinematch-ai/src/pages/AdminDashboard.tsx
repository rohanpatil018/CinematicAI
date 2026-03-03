import { Users, UserCheck, DollarSign, Zap, TrendingUp } from "lucide-react";

const metrics = [
  { label: "Total Users", value: "12,847", change: "+12%", icon: Users },
  { label: "Active Users", value: "8,234", change: "+8%", icon: UserCheck },
  { label: "Revenue", value: "$34,560", change: "+23%", icon: DollarSign },
  { label: "API Requests", value: "2.4M", change: "+15%", icon: Zap },
];

const topGenres = [
  { name: "Sci-Fi", pct: 28 },
  { name: "Drama", pct: 24 },
  { name: "Thriller", pct: 18 },
  { name: "Romance", pct: 14 },
  { name: "Comedy", pct: 10 },
  { name: "Other", pct: 6 },
];

const AdminDashboard = () => {
  return (
    <div className="p-6 lg:p-8 space-y-8 max-w-6xl">
      <div>
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <p className="text-sm text-muted-foreground mt-1">Platform analytics at a glance</p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((m) => (
          <div key={m.label} className="glass-card p-5">
            <div className="flex items-center justify-between mb-3">
              <m.icon className="w-5 h-5 text-muted-foreground" />
              <span className="text-xs text-cinema-teal font-medium flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> {m.change}
              </span>
            </div>
            <p className="text-2xl font-bold">{m.value}</p>
            <p className="text-xs text-muted-foreground mt-1">{m.label}</p>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* User Growth */}
        <div className="glass-card p-6">
          <h3 className="text-sm font-semibold mb-4">User Growth</h3>
          <div className="h-48 flex items-end gap-2">
            {[30, 45, 40, 55, 65, 60, 70, 78, 85, 90, 88, 95].map((v, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t transition-all duration-500"
                  style={{
                    height: `${v * 1.6}px`,
                    background: `linear-gradient(to top, hsl(var(--cinema-gold) / 0.6), hsl(var(--cinema-gold) / 0.2))`,
                  }}
                />
                <span className="text-[9px] text-muted-foreground">{["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"][i]}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Most Recommended Genres */}
        <div className="glass-card p-6">
          <h3 className="text-sm font-semibold mb-4">Most Recommended Genres</h3>
          <div className="space-y-3">
            {topGenres.map((g) => (
              <div key={g.name} className="flex items-center gap-3">
                <span className="text-sm text-muted-foreground w-20">{g.name}</span>
                <div className="flex-1 h-3 rounded-full bg-muted overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${g.pct * 3.5}%`,
                      background: `linear-gradient(90deg, hsl(var(--cinema-gold)), hsl(var(--cinema-teal)))`,
                    }}
                  />
                </div>
                <span className="text-xs text-muted-foreground w-8 text-right">{g.pct}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Conversion */}
      <div className="glass-card p-6">
        <h3 className="text-sm font-semibold mb-4">Conversion Funnel</h3>
        <div className="flex items-end gap-6 justify-center h-40">
          {[
            { label: "Visitors", val: 100 },
            { label: "Signups", val: 68 },
            { label: "Active", val: 45 },
            { label: "Pro", val: 22 },
          ].map((step) => (
            <div key={step.label} className="flex flex-col items-center gap-2">
              <span className="text-xs font-medium">{step.val}%</span>
              <div
                className="w-16 rounded-t transition-all duration-500"
                style={{
                  height: `${step.val * 1.2}px`,
                  background: `linear-gradient(to top, hsl(var(--cinema-gold) / 0.7), hsl(var(--cinema-gold) / 0.15))`,
                }}
              />
              <span className="text-xs text-muted-foreground">{step.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;

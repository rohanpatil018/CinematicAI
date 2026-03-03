import { Share2, Star, Film, Compass, Gem } from "lucide-react";

const stats = [
  { label: "Movies Rated", value: "342", icon: Star },
  { label: "Avg Rating", value: "4.2", icon: Star },
  { label: "Genres Explored", value: "18", icon: Compass },
  { label: "Hidden Gems Found", value: "47", icon: Gem },
];

const genres = [
  { name: "Sci-Fi", value: 92 },
  { name: "Drama", value: 88 },
  { name: "Thriller", value: 76 },
  { name: "Romance", value: 70 },
  { name: "Comedy", value: 65 },
  { name: "Horror", value: 40 },
  { name: "Animation", value: 55 },
  { name: "Documentary", value: 60 },
];

const directors = [
  { name: "Denis Villeneuve", films: 7 },
  { name: "Christopher Nolan", films: 9 },
  { name: "Bong Joon-ho", films: 5 },
  { name: "Greta Gerwig", films: 4 },
];

const history = [
  { title: "Dune: Part Two", date: "Feb 28, 2026", rating: 5 },
  { title: "Past Lives", date: "Feb 25, 2026", rating: 4.5 },
  { title: "The Holdovers", date: "Feb 20, 2026", rating: 4 },
  { title: "Poor Things", date: "Feb 15, 2026", rating: 4.5 },
  { title: "Oppenheimer", date: "Feb 10, 2026", rating: 5 },
];

const DNAProfile = () => {
  return (
    <div className="p-6 lg:p-8 space-y-10 max-w-5xl">
      {/* Hero Banner */}
      <div className="glass-card p-8 text-center relative overflow-hidden">
        <div className="orb w-48 h-48 bg-gold top-0 left-1/2 -translate-x-1/2 -translate-y-1/2" />
        <div className="relative z-10">
          <div className="w-24 h-24 rounded-full border-2 border-gold mx-auto mb-4 flex items-center justify-center text-3xl bg-muted glow-gold">
            R
          </div>
          <h1 className="text-2xl font-bold">Rohan</h1>
          <p className="text-gold text-lg mt-1">🎭 The Melancholic Visionary</p>
          <button className="btn-ghost-cinema text-xs mt-4 inline-flex items-center gap-2">
            <Share2 className="w-3.5 h-3.5" /> Share DNA
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="glass-card p-4 text-center">
            <s.icon className="w-5 h-5 text-gold mx-auto mb-2" />
            <p className="text-2xl font-bold">{s.value}</p>
            <p className="text-xs text-muted-foreground mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Radar Chart (simplified bar version) */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold mb-6 flex items-center gap-2"><Film className="w-5 h-5 text-gold" /> Genre Radar</h2>
        <div className="space-y-3">
          {genres.map((g) => (
            <div key={g.name} className="flex items-center gap-3">
              <span className="text-sm text-muted-foreground w-28">{g.name}</span>
              <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${g.value}%`,
                    background: `linear-gradient(90deg, hsl(var(--cinema-gold)), hsl(var(--cinema-teal)))`,
                  }}
                />
              </div>
              <span className="text-xs text-muted-foreground w-8 text-right">{g.value}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* Top Directors */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold mb-4">Top Directors</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {directors.map((d) => (
            <div key={d.name} className="text-center">
              <div className="w-16 h-16 rounded-full bg-muted border border-[hsl(var(--glass-border))] mx-auto mb-2 flex items-center justify-center text-lg">🎬</div>
              <p className="text-sm font-medium">{d.name}</p>
              <p className="text-xs text-muted-foreground">{d.films} films watched</p>
            </div>
          ))}
        </div>
      </div>

      {/* Watch History */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold mb-4">Recent Watch History</h2>
        <div className="space-y-4">
          {history.map((h) => (
            <div key={h.title} className="flex items-center gap-4 pb-4 border-b border-[hsl(var(--glass-border))] last:border-0 last:pb-0">
              <div className="w-10 h-14 rounded bg-muted flex items-center justify-center text-lg flex-shrink-0">🎬</div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{h.title}</p>
                <p className="text-xs text-muted-foreground">{h.date}</p>
              </div>
              <div className="flex items-center gap-0.5">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} className={`w-3.5 h-3.5 ${i < Math.floor(h.rating) ? "text-gold fill-gold" : "text-muted"}`} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Taste Evolution insight */}
      <div className="glass-card p-6 border-gold">
        <p className="text-xs text-gold font-medium mb-2">AI Insight</p>
        <p className="text-sm text-muted-foreground">
          Your taste has evolved significantly over the past 6 months. You've shifted from mainstream blockbusters toward arthouse and international cinema, with a growing appreciation for slow-burn narratives and visual storytelling.
        </p>
      </div>
    </div>
  );
};

export default DNAProfile;

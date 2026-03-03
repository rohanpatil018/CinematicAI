import { useState } from "react";
import { Heart, ThumbsDown, Plus, Share2, Compass, Filter } from "lucide-react";
import MovieCard from "@/components/MovieCard";

const tabs = ["All", "Streaming Now", "Hidden Gems", "Watch Together"];
const sorts = ["Match %", "Release Year", "IMDB Rating"];

const results = [
  { title: "Dune: Part Two", genre: "Sci-Fi", match: 96, year: "2024", platforms: ["HBO", "Prime"] },
  { title: "Oppenheimer", genre: "Drama", match: 94, year: "2023", platforms: ["Peacock"] },
  { title: "The Zone of Interest", genre: "Drama", match: 91, year: "2023", platforms: ["Prime"] },
  { title: "Poor Things", genre: "Comedy", match: 89, year: "2023", platforms: ["Hulu", "Disney+"] },
  { title: "Anatomy of a Fall", genre: "Thriller", match: 87, year: "2023", platforms: ["MUBI"] },
  { title: "All of Us Strangers", genre: "Romance", match: 85, year: "2023", platforms: ["Hulu"] },
  { title: "The Holdovers", genre: "Comedy", match: 88, year: "2023", platforms: ["Peacock"] },
  { title: "Saltburn", genre: "Thriller", match: 83, year: "2023", platforms: ["Prime"] },
  { title: "Killers of the Flower Moon", genre: "Drama", match: 90, year: "2023", platforms: ["Apple TV+"] },
];

const Discover = () => {
  const [activeTab, setActiveTab] = useState("All");

  return (
    <div className="p-6 lg:p-8 space-y-8 max-w-6xl">
      {/* Tabs & Sort */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex gap-2 flex-wrap">
          {tabs.map((t) => (
            <button
              key={t}
              onClick={() => setActiveTab(t)}
              className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${
                activeTab === t ? "bg-gold text-background font-medium" : "border border-[hsl(var(--glass-border))] text-muted-foreground hover:text-foreground"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-muted-foreground" />
          <select className="bg-muted border border-[hsl(var(--glass-border))] rounded-lg px-3 py-1.5 text-sm text-foreground">
            {sorts.map((s) => <option key={s}>{s}</option>)}
          </select>
        </div>
      </div>

      {/* Hero Result */}
      <div className="glass-card-hover p-6 flex flex-col lg:flex-row gap-8">
        <div className="w-full lg:w-64 h-80 rounded-lg bg-gradient-to-b from-muted to-card flex items-center justify-center text-5xl flex-shrink-0">🎬</div>
        <div className="flex-1 space-y-4">
          <div>
            <h2 className="text-2xl font-bold">Dune: Part Two</h2>
            <p className="text-sm text-muted-foreground">2024 · Sci-Fi, Adventure · 2h 46m</p>
          </div>
          {/* Match score */}
          <div className="flex items-center gap-4">
            <div className="relative w-20 h-20">
              <svg className="w-20 h-20 -rotate-90" viewBox="0 0 36 36">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="hsl(var(--muted))" strokeWidth="2" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="hsl(var(--cinema-gold))" strokeWidth="2" strokeDasharray="96, 100" strokeLinecap="round" />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-lg font-bold text-gold">96%</span>
            </div>
            <div>
              <p className="text-sm font-medium text-gold">Exceptional Match</p>
              <p className="text-xs text-muted-foreground">Based on your Cinematic DNA</p>
            </div>
          </div>
          {/* AI Reason */}
          <div className="glass-card p-4">
            <p className="text-xs text-gold font-medium mb-1">Why CineMatch picked this for you</p>
            <p className="text-sm text-muted-foreground">Your love for grand sci-fi worldbuilding combined with your appreciation for stunning cinematography makes this a perfect continuation of your Villeneuve journey.</p>
          </div>
          {/* Streaming */}
          <div>
            <p className="text-xs text-muted-foreground mb-2">Available on</p>
            <div className="flex gap-2">
              {["HBO Max", "Amazon Prime"].map((p) => (
                <span key={p} className="px-3 py-1.5 rounded-full text-xs font-medium border border-[hsl(var(--glass-border))] text-foreground">{p}</span>
              ))}
              <span className="px-3 py-1.5 rounded-full text-xs font-medium border border-[hsl(var(--glass-border))] text-muted-foreground">Rent $5.99</span>
            </div>
          </div>
          {/* Actions */}
          <div className="flex flex-wrap gap-2">
            {[
              { icon: Heart, label: "Save" },
              { icon: ThumbsDown, label: "Not for me" },
              { icon: Plus, label: "Watchlist" },
              { icon: Share2, label: "Share" },
              { icon: Compass, label: "Explore Universe" },
            ].map((a) => (
              <button key={a.label} className="btn-ghost-cinema text-xs inline-flex items-center gap-1.5 px-3 py-2">
                <a.icon className="w-3.5 h-3.5" /> {a.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {results.slice(1).map((m) => (
          <MovieCard key={m.title} {...m} />
        ))}
      </div>
    </div>
  );
};

export default Discover;

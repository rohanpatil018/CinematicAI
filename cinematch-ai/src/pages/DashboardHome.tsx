import { Search, Share2, Users } from "lucide-react";
import MovieCard from "@/components/MovieCard";

const trendingTags = ["Mind-bending", "Visually Stunning", "Emotional", "Based on True Story", "Dark Comedy", "Feel Good"];

const recommendedMovies = [
  { title: "Arrival", genre: "Sci-Fi", match: 97, year: "2016", platforms: ["Netflix", "Prime"] },
  { title: "Eternal Sunshine", genre: "Romance", match: 94, year: "2004", platforms: ["Hulu"] },
  { title: "Blade Runner 2049", genre: "Sci-Fi", match: 92, year: "2017", platforms: ["HBO", "Prime"] },
  { title: "Moonlight", genre: "Drama", match: 91, year: "2016", platforms: ["Netflix"] },
  { title: "The Grand Budapest Hotel", genre: "Comedy", match: 89, year: "2014", platforms: ["Disney+", "Prime"] },
  { title: "Her", genre: "Romance", match: 88, year: "2013", platforms: ["Netflix", "Hulu"] },
];

const hiddenGems = [
  { title: "The Lobster", genre: "Absurdist", match: 86, year: "2015", platforms: ["Prime"] },
  { title: "Columbus", genre: "Drama", match: 84, year: "2017", platforms: ["Hulu"] },
  { title: "Capernaum", genre: "Drama", match: 82, year: "2018", platforms: ["Netflix"] },
  { title: "The Handmaiden", genre: "Thriller", match: 90, year: "2016", platforms: ["Prime", "Tubi"] },
  { title: "Perfect Days", genre: "Drama", match: 87, year: "2023", platforms: ["MUBI"] },
  { title: "Past Lives", genre: "Romance", match: 93, year: "2023", platforms: ["Prime"] },
];

const DashboardHome = () => {
  return (
    <div className="p-6 lg:p-8 space-y-10 max-w-6xl">
      {/* Greeting */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Good Evening, Rohan</h1>
          <p className="text-muted-foreground text-sm mt-1">Your Cinematic DNA: <span className="text-gold">The Melancholic Visionary</span></p>
        </div>
        <div className="glass-card px-4 py-3 flex items-center gap-3 border-gold animate-pulse-glow">
          <span className="text-2xl">🎭</span>
          <div>
            <p className="text-xs text-muted-foreground">DNA Type</p>
            <p className="text-sm font-semibold text-gold">The Melancholic Visionary</p>
          </div>
          <button className="ml-2 text-muted-foreground hover:text-gold transition-colors">
            <Share2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="relative max-w-2xl">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
        <input
          placeholder="Search by title, actor, director, or describe your mood…"
          className="w-full h-14 rounded-2xl bg-muted border border-[hsl(var(--glass-border))] pl-12 pr-4 text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-gold transition-colors"
        />
        <div className="flex flex-wrap gap-2 mt-3">
          {trendingTags.map((t) => (
            <span key={t} className="text-xs px-3 py-1.5 rounded-full border border-[hsl(var(--glass-border))] text-muted-foreground hover:text-gold hover:border-gold cursor-pointer transition-all duration-300">
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* Because You Watched */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Because You Watched <span className="text-gold">Interstellar</span></h2>
        <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
          {recommendedMovies.map((m) => (
            <MovieCard key={m.title} {...m} />
          ))}
        </div>
      </section>

      {/* Hidden Gems */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Hidden Gems This Week 💎</h2>
        <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
          {hiddenGems.map((m) => (
            <MovieCard key={m.title} {...m} />
          ))}
        </div>
      </section>

      {/* Watch Together CTA */}
      <section className="glass-card-hover p-6 flex flex-col sm:flex-row items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="w-12 h-12 rounded-full bg-muted border border-[hsl(var(--glass-border))] flex items-center justify-center text-lg">R</div>
          <span className="text-2xl">🎬</span>
          <div className="w-12 h-12 rounded-full bg-muted border border-[hsl(var(--glass-border))] flex items-center justify-center text-lg">?</div>
        </div>
        <div className="flex-1 text-center sm:text-left">
          <h3 className="font-semibold mb-1">Watch Together</h3>
          <p className="text-sm text-muted-foreground">Find movies you'll both love</p>
        </div>
        <a href="/dashboard/watch-together" className="btn-gold text-sm inline-flex items-center gap-2">
          <Users className="w-4 h-4" /> Start Matching
        </a>
      </section>
    </div>
  );
};

export default DashboardHome;

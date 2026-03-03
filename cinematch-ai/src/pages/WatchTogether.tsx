import { useState } from "react";
import { Link2, UserPlus, Film } from "lucide-react";
import MovieCard from "@/components/MovieCard";

const matchMovies = [
  { title: "Inception", genre: "Sci-Fi", match: 98, year: "2010", platforms: ["Netflix"] },
  { title: "The Prestige", genre: "Thriller", match: 95, year: "2006", platforms: ["HBO"] },
  { title: "Interstellar", genre: "Sci-Fi", match: 93, year: "2014", platforms: ["Prime"] },
  { title: "Parasite", genre: "Thriller", match: 91, year: "2019", platforms: ["Hulu"] },
  { title: "Whiplash", genre: "Drama", match: 89, year: "2014", platforms: ["Netflix"] },
  { title: "La La Land", genre: "Musical", match: 87, year: "2016", platforms: ["HBO"] },
];

const tabs = ["Both Will Love", "Fair Compromise", "Take Turns"];

const WatchTogether = () => {
  const [activeTab, setActiveTab] = useState(tabs[0]);
  const [step, setStep] = useState(1);

  return (
    <div className="p-6 lg:p-8 space-y-10 max-w-4xl">
      {/* Hero */}
      <div className="text-center">
        <div className="flex items-center justify-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-full bg-muted border border-[hsl(var(--glass-border))] flex items-center justify-center text-xl">R</div>
          <Film className="w-8 h-8 text-gold" />
          <div className="w-16 h-16 rounded-full bg-muted border-2 border-dashed border-[hsl(var(--glass-border))] flex items-center justify-center text-muted-foreground text-xl">?</div>
        </div>
        <h1 className="text-2xl font-bold mb-2">Watch Together</h1>
        <p className="text-muted-foreground text-sm">Find the perfect movie for any duo</p>
      </div>

      {step === 1 && (
        <div className="grid md:grid-cols-2 gap-6">
          {/* You */}
          <div className="glass-card p-6 text-center">
            <div className="w-14 h-14 rounded-full bg-muted border border-gold mx-auto mb-3 flex items-center justify-center text-lg glow-gold">R</div>
            <p className="font-semibold mb-1">You</p>
            <p className="text-xs text-muted-foreground">Rohan · The Melancholic Visionary</p>
          </div>
          {/* Friend */}
          <div className="glass-card p-6 text-center space-y-4">
            <p className="font-semibold mb-4">Add a Friend</p>
            <button className="btn-ghost-cinema w-full text-sm inline-flex items-center justify-center gap-2">
              <Link2 className="w-4 h-4" /> Invite via Link
            </button>
            <button className="btn-ghost-cinema w-full text-sm inline-flex items-center justify-center gap-2">
              <UserPlus className="w-4 h-4" /> Enter Username
            </button>
            <button onClick={() => setStep(2)} className="btn-gold w-full text-sm">
              Pick 5 Movies Manually
            </button>
          </div>
        </div>
      )}

      {step >= 2 && (
        <>
          {/* Compatibility */}
          <div className="glass-card p-8 text-center">
            <p className="text-sm text-muted-foreground mb-4">Compatibility Score</p>
            <div className="relative w-32 h-32 mx-auto mb-4">
              <svg className="w-32 h-32 -rotate-90" viewBox="0 0 36 36">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="hsl(var(--muted))" strokeWidth="2" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="hsl(var(--cinema-gold))" strokeWidth="2.5" strokeDasharray="94, 100" strokeLinecap="round" />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-2xl font-bold text-gold">94%</span>
            </div>
            <p className="text-lg font-semibold text-gold">Movie Soulmates 🎬</p>
            <p className="text-xs text-muted-foreground mt-1">You share a deep love for cerebral sci-fi and visual storytelling</p>
          </div>

          {/* Tabs */}
          <div className="flex gap-2 justify-center">
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

          {/* Movie results */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            {matchMovies.map((m) => (
              <MovieCard key={m.title} {...m} />
            ))}
          </div>

          <div className="text-center">
            <button className="btn-ghost-cinema text-sm">📋 Copy Watch List</button>
          </div>
        </>
      )}
    </div>
  );
};

export default WatchTogether;

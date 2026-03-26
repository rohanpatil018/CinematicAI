import { useState } from "react";
import { Gem, Star, Calendar, Play, Heart, Share2, TrendingUp, Award } from "lucide-react";
import MovieCard from "@/components/MovieCard";

interface HiddenGem {
  title: string;
  genre: string;
  match: number;
  year: string;
  platforms: string[];
  imdbRating: number;
  rtScore: number;
  hiddenGemScore: number;
  description: string;
  whyHidden: string;
  director: string;
}

const HiddenGems = () => {
  const [sortBy, setSortBy] = useState("hgs");

  // Mock hidden gems data - in real app this would come from API
  const hiddenGems: HiddenGem[] = [
    {
      title: "The Holdovers",
      genre: "Comedy",
      match: 88,
      year: "2023",
      platforms: ["Peacock"],
      imdbRating: 8.1,
      rtScore: 97,
      hiddenGemScore: 91,
      description: "A cranky history teacher at a remote boarding school is forced to remain on campus over the holidays with a troubled student.",
      whyHidden: "Critically acclaimed but overshadowed by blockbuster releases",
      director: "Alexander Payne"
    },
    {
      title: "The Zone of Interest",
      genre: "Drama",
      match: 91,
      year: "2023",
      platforms: ["Prime"],
      imdbRating: 7.6,
      rtScore: 93,
      hiddenGemScore: 89,
      description: "The commandant of Auschwitz, Rudolf Höss, and his wife Hedwig, strive to build a dream life for their family.",
      whyHidden: "Uncomfortable subject matter limited mainstream appeal",
      director: "Jonathan Glazer"
    },
    {
      title: "Past Lives",
      genre: "Romance",
      match: 86,
      year: "2023",
      platforms: ["Showtime"],
      imdbRating: 8.0,
      rtScore: 95,
      hiddenGemScore: 87,
      description: "Nora and Hae Sung, two deeply connected childhood friends, are wrest apart after Nora's family emigrates from South Korea.",
      whyHidden: "Indie romance with limited marketing budget",
      director: "Celine Song"
    },
    {
      title: "Anatomy of a Fall",
      genre: "Thriller",
      match: 87,
      year: "2023",
      platforms: ["MUBI"],
      imdbRating: 7.8,
      rtScore: 91,
      hiddenGemScore: 85,
      description: "A woman is suspected of her husband's murder, and their blind son faces a moral dilemma as the sole witness.",
      whyHidden: "French-language film with limited theatrical release",
      director: "Justine Triet"
    },
    {
      title: "All of Us Strangers",
      genre: "Romance",
      match: 85,
      year: "2023",
      platforms: ["Hulu"],
      imdbRating: 7.7,
      rtScore: 89,
      hiddenGemScore: 83,
      description: "One night in his near-empty tower block in contemporary London, Adam has a chance encounter with a mysterious neighbor.",
      whyHidden: "LGBTQ+ themes limited mainstream distribution",
      director: "Andrew Haigh"
    },
    {
      title: "The Eternal Daughter",
      genre: "Drama",
      match: 82,
      year: "2022",
      platforms: ["HBO Max"],
      imdbRating: 7.3,
      rtScore: 85,
      hiddenGemScore: 80,
      description: "A mother and daughter journey to a remote hotel, but once there, secrets unravel and their bond is tested.",
      whyHidden: "Slow-paced drama that flew under the radar",
      director: "Joanna Hogg"
    }
  ];

  const sortOptions = [
    { value: "hgs", label: "Hidden Gem Score" },
    { value: "match", label: "Your Match" },
    { value: "imdb", label: "IMDB Rating" },
    { value: "rt", label: "Rotten Tomatoes" },
    { value: "year", label: "Release Year" }
  ];

  const sortedGems = [...hiddenGems].sort((a, b) => {
    switch (sortBy) {
      case "hgs":
        return b.hiddenGemScore - a.hiddenGemScore;
      case "match":
        return b.match - a.match;
      case "imdb":
        return b.imdbRating - a.imdbRating;
      case "rt":
        return b.rtScore - a.rtScore;
      case "year":
        return parseInt(b.year) - parseInt(a.year);
      default:
        return 0;
    }
  });

  return (
    <div className="p-6 lg:p-8 space-y-8 max-w-6xl">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center gap-3">
          <Gem className="w-8 h-8 text-gold" />
          <h1 className="text-3xl font-bold">Hidden Gems</h1>
        </div>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Discover critically acclaimed films that flew under the radar. Our Hidden Gem Score identifies 
          movies with high ratings but low popularity - perfect for finding your next favorite.
        </p>
        <div className="flex items-center justify-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <Award className="w-4 h-4 text-gold" />
            <span>IMDB 7.5+ & Rotten Tomatoes 85%+</span>
          </div>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-gold" />
            <span>Limited mainstream exposure</span>
          </div>
        </div>
      </div>

      {/* Sort */}
      <div className="flex justify-end">
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="bg-muted border border-[hsl(var(--glass-border))] rounded-lg px-3 py-1.5 text-sm text-foreground"
        >
          {sortOptions.map(option => (
            <option key={option.value} value={option.value}>
              Sort by {option.label}
            </option>
          ))}
        </select>
      </div>

      {/* Top Hidden Gem */}
      {sortedGems.length > 0 && (
        <div className="glass-card-hover p-6">
          <div className="flex flex-col lg:flex-row gap-8">
            <div className="w-full lg:w-64 h-80 rounded-lg bg-gradient-to-b from-muted to-card flex items-center justify-center text-5xl flex-shrink-0">
              💎
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h2 className="text-2xl font-bold">{sortedGems[0].title}</h2>
                <p className="text-sm text-muted-foreground">
                  {sortedGems[0].year} · {sortedGems[0].genre} · Directed by {sortedGems[0].director}
                </p>
              </div>
              
              {/* Hidden Gem Score */}
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <div className="relative w-16 h-16">
                    <svg className="w-16 h-16 -rotate-90" viewBox="0 0 36 36">
                      <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                            fill="none" stroke="hsl(var(--muted))" strokeWidth="2" />
                      <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                            fill="none" stroke="hsl(var(--cinema-gold))" strokeWidth="2" 
                            strokeDasharray={`${sortedGems[0].hiddenGemScore}, 100`} strokeLinecap="round" />
                    </svg>
                    <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-gold">
                      {sortedGems[0].hiddenGemScore}
                    </span>
                  </div>
                  <p className="text-xs text-gold font-medium mt-1">HGS</p>
                </div>
                
                <div className="flex gap-4 text-sm">
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 text-yellow-500" />
                    <span>{sortedGems[0].imdbRating}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-4 h-4 bg-red-500 rounded-full" />
                    <span>{sortedGems[0].rtScore}%</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Gem className="w-4 h-4 text-gold" />
                    <span>{sortedGems[0].match}% Match</span>
                  </div>
                </div>
              </div>

              <p className="text-sm text-muted-foreground">{sortedGems[0].description}</p>
              
              <div className="glass-card p-4">
                <p className="text-xs text-gold font-medium mb-1">Why it's a Hidden Gem</p>
                <p className="text-sm text-muted-foreground">{sortedGems[0].whyHidden}</p>
              </div>

              <div className="flex flex-wrap gap-2">
                <button className="btn-ghost-cinema text-xs inline-flex items-center gap-1.5 px-3 py-2">
                  <Play className="w-3.5 h-3.5" /> Watch Trailer
                </button>
                <button className="btn-ghost-cinema text-xs inline-flex items-center gap-1.5 px-3 py-2">
                  <Heart className="w-3.5 h-3.5" /> Save
                </button>
                <button className="btn-ghost-cinema text-xs inline-flex items-center gap-1.5 px-3 py-2">
                  <Share2 className="w-3.5 h-3.5" /> Share
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {sortedGems.slice(1).map((gem) => (
          <MovieCard key={gem.title} {...gem} />
        ))}
      </div>

      {/* Algorithm Info */}
      <div className="glass-card p-6 text-center">
        <h3 className="text-lg font-semibold mb-3">How Hidden Gem Score Works</h3>
        <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
          HGS = (IMDB Rating × 0.35) + (Rotten Tomatoes × 0.25) + (Content Similarity × 0.25) - (Popularity × 0.15)
        </p>
        <p className="text-xs text-muted-foreground mt-2">
          Only includes movies with &lt;100K votes and ratings above 7.5 on IMDB
        </p>
      </div>
    </div>
  );
};

export default HiddenGems;

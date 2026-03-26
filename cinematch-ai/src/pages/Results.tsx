import { useState } from "react";
import { ArrowLeft, Heart, ThumbsDown, Plus, Share2, Filter, SlidersHorizontal } from "lucide-react";
import { useNavigate } from "react-router-dom";
import MovieCard from "@/components/MovieCard";

interface MovieResult {
  title: string;
  genre: string;
  match: number;
  year: string;
  platforms: string[];
  description?: string;
  director?: string;
  cast?: string[];
}

const Results = () => {
  const navigate = useNavigate();
  const [sortBy, setSortBy] = useState("match");
  const [filterGenre, setFilterGenre] = useState("all");

  // Mock data - in real app this would come from API
  const results: MovieResult[] = [
    { title: "Dune: Part Two", genre: "Sci-Fi", match: 96, year: "2024", platforms: ["HBO", "Prime"], description: "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.", director: "Denis Villeneuve", cast: ["Timothée Chalamet", "Zendaya", "Rebecca Ferguson"] },
    { title: "Oppenheimer", genre: "Drama", match: 94, year: "2023", platforms: ["Peacock"], description: "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.", director: "Christopher Nolan", cast: ["Cillian Murphy", "Emily Blunt", "Matt Damon"] },
    { title: "The Zone of Interest", genre: "Drama", match: 91, year: "2023", platforms: ["Prime"], description: "The commandant of Auschwitz, Rudolf Höss, and his wife Hedwig, strive to build a dream life for their family.", director: "Jonathan Glazer", cast: ["Christian Friedel", "Sandra Hüller"] },
    { title: "Poor Things", genre: "Comedy", match: 89, year: "2023", platforms: ["Hulu", "Disney+"], description: "The incredible tale about the fantastical evolution of Bella Baxter, a young woman brought back to life by the brilliant scientist.", director: "Yorgos Lanthimos", cast: ["Emma Stone", "Mark Ruffalo", "Willem Dafoe"] },
    { title: "Anatomy of a Fall", genre: "Thriller", match: 87, year: "2023", platforms: ["MUBI"], description: "A woman is suspected of her husband's murder, and their blind son faces a moral dilemma as the sole witness.", director: "Justine Triet", cast: ["Sandra Hüller", "Swann Arlaud", "Milo Machado-Graner"] },
    { title: "All of Us Strangers", genre: "Romance", match: 85, year: "2023", platforms: ["Hulu"], description: "One night in his near-empty tower block in contemporary London, Adam has a chance encounter with a mysterious neighbor.", director: "Andrew Haigh", cast: ["Andrew Scott", "Paul Mescal", "Jamie Bell"] },
    { title: "The Holdovers", genre: "Comedy", match: 88, year: "2023", platforms: ["Peacock"], description: "A cranky history teacher at a remote boarding school is forced to remain on campus over the holidays with a troubled student.", director: "Alexander Payne", cast: ["Paul Giamatti", "Da'Vine Joy Randolph", "Dominic Sessa"] },
    { title: "Saltburn", genre: "Thriller", match: 83, year: "2023", platforms: ["Prime"], description: "A student at Oxford University finds himself drawn into the world of a charming and aristocratic classmate.", director: "Emerald Fennell", cast: ["Barry Keoghan", "Jacob Elordi", "Rosamund Pike"] },
  ];

  const genres = ["all", "Sci-Fi", "Drama", "Comedy", "Thriller", "Romance"];
  const sortOptions = [
    { value: "match", label: "Match %" },
    { value: "year", label: "Release Year" },
    { value: "rating", label: "IMDB Rating" },
    { value: "title", label: "Title" }
  ];

  const sortedResults = [...results].sort((a, b) => {
    switch (sortBy) {
      case "match":
        return b.match - a.match;
      case "year":
        return parseInt(b.year) - parseInt(a.year);
      case "title":
        return a.title.localeCompare(b.title);
      default:
        return 0;
    }
  });

  const filteredResults = sortedResults.filter(result => 
    filterGenre === "all" || result.genre === filterGenre
  );

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b border-[hsl(var(--glass-border))]">
        <div className="max-w-6xl mx-auto px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(-1)}
                className="btn-ghost-cinema p-2"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div>
                <h1 className="text-2xl font-bold">Your Recommendations</h1>
                <p className="text-sm text-muted-foreground">
                  {filteredResults.length} movies found based on your preferences
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-muted-foreground" />
                <select
                  value={filterGenre}
                  onChange={(e) => setFilterGenre(e.target.value)}
                  className="bg-muted border border-[hsl(var(--glass-border))] rounded-lg px-3 py-1.5 text-sm text-foreground"
                >
                  {genres.map(genre => (
                    <option key={genre} value={genre}>
                      {genre === "all" ? "All Genres" : genre}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-muted-foreground" />
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="bg-muted border border-[hsl(var(--glass-border))] rounded-lg px-3 py-1.5 text-sm text-foreground"
                >
                  {sortOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="max-w-6xl mx-auto px-6 lg:px-8 py-8">
        {filteredResults.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎬</div>
            <h3 className="text-xl font-semibold mb-2">No movies found</h3>
            <p className="text-muted-foreground">Try adjusting your filters or search criteria</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {filteredResults.map((movie) => (
              <MovieCard key={movie.title} {...movie} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Results;

interface MovieCardProps {
  title: string;
  genre: string;
  match: number;
  year?: string;
  platforms?: string[];
  posterColor?: string;
}

const MovieCard = ({ title, genre, match, year, platforms = ["Netflix", "Prime"], posterColor = "from-muted to-card" }: MovieCardProps) => {
  return (
    <div className="glass-card-hover group cursor-pointer flex-shrink-0 w-48 overflow-hidden">
      {/* Poster placeholder */}
      <div className={`relative h-64 bg-gradient-to-b ${posterColor} overflow-hidden`}>
        <div className="absolute inset-0 bg-[hsl(var(--cinema-gold)/0.03)] group-hover:bg-[hsl(var(--cinema-gold)/0.08)] transition-colors duration-300" />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-3xl opacity-30">🎬</span>
        </div>
        <div className="match-badge">{match}%</div>
        <div className="absolute bottom-0 inset-x-0 h-20 bg-gradient-to-t from-background/80 to-transparent" />
      </div>
      <div className="p-3">
        <h4 className="text-sm font-semibold truncate">{title}</h4>
        <div className="flex items-center gap-2 mt-1">
          <span className="text-xs px-2 py-0.5 rounded-full border border-[hsl(var(--glass-border))] text-muted-foreground">{genre}</span>
          {year && <span className="text-xs text-muted-foreground">{year}</span>}
        </div>
        <div className="flex items-center gap-1 mt-2">
          {platforms.slice(0, 3).map((p) => (
            <span key={p} className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground">{p}</span>
          ))}
          {platforms.length > 3 && <span className="text-[10px] text-muted-foreground">+{platforms.length - 3}</span>}
        </div>
      </div>
    </div>
  );
};

export default MovieCard;

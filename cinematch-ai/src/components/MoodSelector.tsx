import { useState } from "react";
import { Smile, Heart, Zap, Skull, Droplets } from "lucide-react";

const moods = [
  { label: "Happy", icon: Smile },
  { label: "Romantic", icon: Heart },
  { label: "Motivated", icon: Zap },
  { label: "Thriller Night", icon: Skull },
  { label: "Emotional", icon: Droplets },
];

const MoodSelector = () => {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState("Happy");

  return (
    <div className="relative hidden sm:block">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 rounded-full border border-[hsl(var(--glass-border))] text-sm text-muted-foreground hover:text-foreground hover:border-gold transition-all duration-300"
      >
        {moods.find((m) => m.label === selected)?.icon && (() => {
          const Icon = moods.find((m) => m.label === selected)!.icon;
          return <Icon className="w-4 h-4" />;
        })()}
        {selected}
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-2 glass-card p-2 w-48 animate-scale-in z-50">
          {moods.map((m) => (
            <button
              key={m.label}
              onClick={() => { setSelected(m.label); setOpen(false); }}
              className={`flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm transition-all ${
                selected === m.label ? "text-gold bg-[hsl(var(--cinema-gold)/0.08)]" : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
              }`}
            >
              <m.icon className="w-4 h-4" /> {m.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default MoodSelector;

import React from "react";
import { createRoot } from "react-dom/client";
import { AnimeCard } from "./components/AnimeCard";
import { CharacterView } from "./components/CharacterView";
import { MediaList } from "./components/MediaList";

const root = createRoot(document.getElementById("root")!);

root.render(
  <React.StrictMode>
    <main className="app">
      <h1>AniList ChatGPT App UI</h1>
      <AnimeCard
        title="Frieren: Beyond Journey's End"
        score={93}
        description="A calm fantasy journey with heartfelt storytelling."
      />
      <CharacterView name="Frieren" description="An elven mage with centuries of memories." />
      <MediaList
        items={[
          { id: 1, title: "Fullmetal Alchemist: Brotherhood", progress: 12 },
          { id: 2, title: "Violet Evergarden", progress: 4 }
        ]}
      />
    </main>
  </React.StrictMode>
);

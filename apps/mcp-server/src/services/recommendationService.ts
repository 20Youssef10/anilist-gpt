export type TasteProfile = {
  genres: Record<string, number>;
  studios: Record<string, number>;
  vector?: number[];
};

export function scoreRecommendations<T extends { genres?: string[]; studios?: string[] }>(
  items: T[],
  profile: TasteProfile
): (T & { score: number })[] {
  return items.map((item) => {
    const genreScore = (item.genres ?? []).reduce(
      (sum, genre) => sum + (profile.genres[genre] ?? 0),
      0
    );
    const studioScore = (item.studios ?? []).reduce(
      (sum, studio) => sum + (profile.studios[studio] ?? 0),
      0
    );
    return { ...item, score: genreScore + studioScore };
  });
}

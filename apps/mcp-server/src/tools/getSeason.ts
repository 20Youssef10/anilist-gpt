import { fetchAniList } from "../services/anilistService.js";
import { getCache, setCache } from "../services/cacheService.js";
import { seasonAnimeSchema } from "../schemas/toolSchemas.js";

const QUERY = `
  query SeasonalAnime($season: MediaSeason, $seasonYear: Int, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
      media(type: ANIME, season: $season, seasonYear: $seasonYear, sort: POPULARITY_DESC) {
        id
        title { romaji english }
        coverImage { large }
        averageScore
        popularity
        status
      }
    }
  }
`;

export async function getSeasonAnime(input: unknown) {
  const params = seasonAnimeSchema.parse(input);
  const cacheKey = `season:anime:${params.season}:${params.year}:${params.page}:${params.perPage}`;
  const cached = await getCache(cacheKey);
  if (cached) return cached;

  const data = await fetchAniList(QUERY, {
    season: params.season,
    seasonYear: params.year,
    page: params.page,
    perPage: params.perPage
  });
  await setCache(cacheKey, data, 1800);
  return data;
}

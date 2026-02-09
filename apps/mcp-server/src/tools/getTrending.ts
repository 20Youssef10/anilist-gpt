import { fetchAniList } from "../services/anilistService.js";
import { getCache, setCache } from "../services/cacheService.js";
import { trendingAnimeSchema } from "../schemas/toolSchemas.js";

const QUERY = `
  query TrendingAnime($page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
      media(type: ANIME, sort: TRENDING_DESC) {
        id
        title { romaji english }
        coverImage { large }
        averageScore
        trending
      }
    }
  }
`;

export async function getTrendingAnime(input: unknown) {
  const params = trendingAnimeSchema.parse(input);
  const cacheKey = `trending:anime:${params.page}:${params.perPage}`;
  const cached = await getCache(cacheKey);
  if (cached) return cached;

  const data = await fetchAniList(QUERY, params);
  await setCache(cacheKey, data, 900);
  return data;
}

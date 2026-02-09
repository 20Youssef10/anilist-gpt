import { fetchAniList } from "../services/anilistService.js";
import { getCache, setCache } from "../services/cacheService.js";
import { searchAnimeSchema } from "../schemas/toolSchemas.js";

const QUERY = `
  query SearchAnime($query: String, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
      media(search: $query, type: ANIME) {
        id
        title { romaji english native }
        coverImage { large color }
        genres
        averageScore
        popularity
        description
        episodes
        season
        seasonYear
      }
    }
  }
`;

export async function searchAnime(input: unknown) {
  const params = searchAnimeSchema.parse(input);
  const cacheKey = `search:anime:${params.query}:${params.page}:${params.perPage}`;
  const cached = await getCache(cacheKey);
  if (cached) return cached;

  const data = await fetchAniList(QUERY, params);
  await setCache(cacheKey, data);
  return data;
}

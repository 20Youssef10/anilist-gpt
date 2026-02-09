import { z } from "zod";

export const searchAnimeSchema = z.object({
  query: z.string(),
  genres: z.array(z.string()).optional(),
  season: z.enum(["WINTER", "SPRING", "SUMMER", "FALL"]).optional(),
  year: z.number().int().optional(),
  page: z.number().int().default(1),
  perPage: z.number().int().default(10)
});

export const trendingAnimeSchema = z.object({
  page: z.number().int().default(1),
  perPage: z.number().int().default(10)
});

export const seasonAnimeSchema = z.object({
  season: z.enum(["WINTER", "SPRING", "SUMMER", "FALL"]),
  year: z.number().int(),
  page: z.number().int().default(1),
  perPage: z.number().int().default(20)
});

export const userListSchema = z.object({
  status: z.enum(["CURRENT", "COMPLETED", "DROPPED", "PAUSED", "PLANNING"]).optional(),
  page: z.number().int().default(1),
  perPage: z.number().int().default(50)
});

export const characterSchema = z.object({
  characterId: z.number().int().optional(),
  name: z.string().optional()
});

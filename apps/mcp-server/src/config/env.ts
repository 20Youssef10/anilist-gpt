import { z } from "zod";

const envSchema = z.object({
  ANILIST_API_URL: z.string().url().default("https://graphql.anilist.co"),
  REDIS_URL: z.string().optional(),
  ANILIST_CLIENT_ID: z.string().optional(),
  ANILIST_CLIENT_SECRET: z.string().optional(),
  OAUTH_REDIRECT_URI: z.string().optional()
});

export const env = envSchema.parse({
  ANILIST_API_URL: process.env.ANILIST_API_URL,
  REDIS_URL: process.env.REDIS_URL,
  ANILIST_CLIENT_ID: process.env.ANILIST_CLIENT_ID,
  ANILIST_CLIENT_SECRET: process.env.ANILIST_CLIENT_SECRET,
  OAUTH_REDIRECT_URI: process.env.OAUTH_REDIRECT_URI
});

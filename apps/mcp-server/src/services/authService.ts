import { env } from "../config/env.js";

export function buildAniListAuthUrl(state: string) {
  if (!env.ANILIST_CLIENT_ID || !env.OAUTH_REDIRECT_URI) return null;
  const params = new URLSearchParams({
    client_id: env.ANILIST_CLIENT_ID,
    redirect_uri: env.OAUTH_REDIRECT_URI,
    response_type: "code",
    state
  });
  return `https://anilist.co/api/v2/oauth/authorize?${params.toString()}`;
}

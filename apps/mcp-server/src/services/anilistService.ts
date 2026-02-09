import { anilistClient } from "../clients/anilistClient.js";

export async function fetchAniList<T>(query: string, variables?: Record<string, unknown>) {
  return anilistClient.request<T>(query, variables);
}

import { redisClient } from "../clients/redisClient.js";

export async function getCache<T>(key: string): Promise<T | null> {
  if (!redisClient) return null;
  const value = await redisClient.get(key);
  return value ? (JSON.parse(value) as T) : null;
}

export async function setCache(key: string, payload: unknown, ttlSeconds = 3600) {
  if (!redisClient) return;
  await redisClient.set(key, JSON.stringify(payload), "EX", ttlSeconds);
}

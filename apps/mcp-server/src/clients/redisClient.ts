import Redis from "ioredis";
import { env } from "../config/env.js";

export const redisClient = env.REDIS_URL ? new Redis(env.REDIS_URL) : null;

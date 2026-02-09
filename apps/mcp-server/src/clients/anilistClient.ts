import { GraphQLClient } from "graphql-request";
import { env } from "../config/env.js";

export const anilistClient = new GraphQLClient(env.ANILIST_API_URL, {
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json"
  }
});

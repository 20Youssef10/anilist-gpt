import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { searchAnime } from "./tools/searchAnime.js";
import { getTrendingAnime } from "./tools/getTrending.js";
import { getSeasonAnime } from "./tools/getSeason.js";
import { getUserList } from "./tools/getUserList.js";
import { getCharacterInfo } from "./tools/getCharacter.js";

const server = new McpServer({
  name: "anilist-mcp",
  version: "0.1.0"
});

server.tool(
  "search_anime",
  "Search anime by title, genre, season, or filters.",
  async (input) => searchAnime(input)
);

server.tool(
  "get_trending_anime",
  "Return current trending anime.",
  async (input) => getTrendingAnime(input)
);

server.tool(
  "get_season_anime",
  "Seasonal anime list.",
  async (input) => getSeasonAnime(input)
);

server.tool(
  "get_user_list",
  "Fetch user anime list from AniList using OAuth.",
  async (input, context) => {
    const userId = Number(context?.user?.id ?? 0);
    if (!userId) throw new Error("Missing user context.");
    return getUserList(input, userId);
  }
);

server.tool(
  "get_character_info",
  "Retrieve character details and media appearances.",
  async (input) => getCharacterInfo(input)
);

server.listen();

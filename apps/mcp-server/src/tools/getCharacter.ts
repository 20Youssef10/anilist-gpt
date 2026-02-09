import { fetchAniList } from "../services/anilistService.js";
import { characterSchema } from "../schemas/toolSchemas.js";

const QUERY = `
  query CharacterInfo($id: Int, $search: String) {
    Character(id: $id, search: $search) {
      id
      name { full native }
      image { large }
      favourites
      description
      media(sort: POPULARITY_DESC) {
        nodes {
          id
          title { romaji english }
          coverImage { large }
        }
      }
    }
  }
`;

export async function getCharacterInfo(input: unknown) {
  const params = characterSchema.parse(input);
  return fetchAniList(QUERY, {
    id: params.characterId,
    search: params.name
  });
}

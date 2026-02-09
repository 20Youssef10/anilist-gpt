import { fetchAniList } from "../services/anilistService.js";
import { userListSchema } from "../schemas/toolSchemas.js";

const QUERY = `
  query UserList($userId: Int, $status: MediaListStatus, $page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
      mediaList(userId: $userId, type: ANIME, status: $status) {
        media {
          id
          title { romaji english }
          coverImage { large }
        }
        progress
        score
        status
      }
    }
  }
`;

export async function getUserList(input: unknown, userId: number) {
  const params = userListSchema.parse(input);
  return fetchAniList(QUERY, {
    userId,
    status: params.status,
    page: params.page,
    perPage: params.perPage
  });
}

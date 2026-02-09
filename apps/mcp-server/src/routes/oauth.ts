import { buildAniListAuthUrl } from "../services/authService.js";

export function getAuthRedirect(state: string) {
  const url = buildAniListAuthUrl(state);
  if (!url) {
    throw new Error("OAuth configuration missing.");
  }
  return url;
}

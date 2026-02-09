import type { ReactNode } from "react";

export type AnimeCardProps = {
  title: string;
  coverUrl?: string;
  score?: number;
  description?: string;
  footer?: ReactNode;
};

export function AnimeCard({ title, coverUrl, score, description, footer }: AnimeCardProps) {
  return (
    <article className="anime-card">
      {coverUrl ? <img src={coverUrl} alt={title} /> : null}
      <div className="anime-card__body">
        <h3>{title}</h3>
        {score ? <p className="anime-card__score">Score: {score}</p> : null}
        {description ? <p className="anime-card__description">{description}</p> : null}
        {footer ? <div className="anime-card__footer">{footer}</div> : null}
      </div>
    </article>
  );
}

export type MediaListItem = {
  id: number;
  title: string;
  coverUrl?: string;
  progress?: number;
};

export type MediaListProps = {
  items: MediaListItem[];
};

export function MediaList({ items }: MediaListProps) {
  return (
    <ul className="media-list">
      {items.map((item) => (
        <li key={item.id}>
          {item.coverUrl ? <img src={item.coverUrl} alt={item.title} /> : null}
          <div>
            <h4>{item.title}</h4>
            {item.progress !== undefined ? <p>Progress: {item.progress}</p> : null}
          </div>
        </li>
      ))}
    </ul>
  );
}

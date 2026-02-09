export type CharacterViewProps = {
  name: string;
  imageUrl?: string;
  description?: string;
};

export function CharacterView({ name, imageUrl, description }: CharacterViewProps) {
  return (
    <section className="character-view">
      {imageUrl ? <img src={imageUrl} alt={name} /> : null}
      <div>
        <h3>{name}</h3>
        {description ? <p>{description}</p> : null}
      </div>
    </section>
  );
}

import { getPageBySlug } from "../lib/content";

export default function HomePage() {
  const page = getPageBySlug("");
  if (!page) return null;

  return (
    <section>
      <h1>{page.title_en}</h1>
      <h2>{page.title_zh}</h2>
      <p>{page.summary_en}</p>
      <p>{page.summary_zh}</p>
    </section>
  );
}

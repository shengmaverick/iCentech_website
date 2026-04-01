import { notFound } from "next/navigation";
import { getPageBySlug, pages } from "../../lib/content";

export function generateStaticParams() {
  return pages
    .filter((p) => p.slug !== "")
    .map((p) => ({
      slug: p.slug
    }));
}

export default function DynamicPage({ params }: { params: { slug: string } }) {
  const page = getPageBySlug(params.slug);
  if (!page) return notFound();

  return (
    <section>
      <h1>{page.title_en}</h1>
      <h2>{page.title_zh}</h2>
      <p>{page.summary_en}</p>
      <p>{page.summary_zh}</p>
    </section>
  );
}

import data from "../site-content.json";

export type NavItem = {
  key: string;
  label_zh: string;
  label_en: string;
  slug: string;
};

export type PageItem = {
  slug: string;
  title_zh: string;
  title_en: string;
  summary_zh: string;
  summary_en: string;
};

export const navigation = data.navigation as NavItem[];
export const pages = data.pages as PageItem[];

export function getPageBySlug(slug: string): PageItem | undefined {
  return pages.find((p) => p.slug === slug);
}

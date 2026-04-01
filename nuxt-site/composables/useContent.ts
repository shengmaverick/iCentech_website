import data from "../site-content.json";

type NavItem = {
  key: string;
  label_zh: string;
  label_en: string;
  slug: string;
};

type PageItem = {
  slug: string;
  title_zh: string;
  title_en: string;
  summary_zh: string;
  summary_en: string;
};

export const useContent = () => {
  const navigation = data.navigation as NavItem[];
  const pages = data.pages as PageItem[];
  const getPage = (slug: string) => pages.find((p) => p.slug === slug);
  return { navigation, pages, getPage };
};

import type { ReactNode } from "react";
import { navigation } from "../lib/content";

export const metadata = {
  title: "iCentech",
  description: "Bilingual website skeleton for iCentech"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "Arial, sans-serif", margin: 0 }}>
        <header style={{ borderBottom: "1px solid #e5e7eb", padding: "14px 20px" }}>
          <strong style={{ marginRight: 16 }}>iCentech</strong>
          {navigation.map((item) => {
            const href = item.slug ? `/${item.slug}` : "/";
            return (
              <a key={item.key} href={href} style={{ marginRight: 10, color: "#334155" }}>
                {item.label_en} / {item.label_zh}
              </a>
            );
          })}
        </header>
        <main style={{ maxWidth: 900, margin: "40px auto", padding: "0 16px" }}>{children}</main>
      </body>
    </html>
  );
}

// src/types.ts
export interface PageSection {
  title: string;
  body: string;
  // …
}

export interface BlogPost {
  slug: string;
  title: string;
  content: string;
  // any other fields (published_date, excerpt, etc.)
}

export interface LinkItem {
  url: string;
  label: string;
  // any other fields (icon, description, etc.)
}

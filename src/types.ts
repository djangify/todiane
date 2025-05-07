// src/types.ts

/** BlogPost model */
export interface BlogPost {
  title: string;
  slug: string;
  content: string;
  created_at: string;
  is_published: boolean;
  published_at: string | null;
  featured_image?: string;
  youtube_url?: string;
  attachment?: string;
  is_featured: boolean;
}

/** Page model */
export interface Page {
  title: string;
  slug: string;
  subtitle?: string;
  hero_image?: string;
  content: string;
  meta_description?: string;
  is_published: boolean;
  published_at?: string;
  order: number;
  created_at: string;
  updated_at: string;
}

/** Link within a LinkHub */
export interface Link {
  title: string;
  url: string;
  icon_url?: string;
  order: number;
}

/** LinkHub model */
export interface LinkHub {
  title: string;
  slug: string;
  description?: string;
  created_at: string;
  is_published: boolean;
  published_at?: string;
  links: Link[];
}

import type { PageSection, BlogPost, LinkItem } from '../types';

const API = import.meta.env.PUBLIC_API_BASE_URL;

export async function fetchPages(): Promise<PageSection[]> {
  const res = await fetch(`${API}/pages/`);
  if (!res.ok) throw new Error(`Error fetching pages: ${res.status}`);
  return res.json();
}

export async function fetchPosts(): Promise<BlogPost[]> {
  const res = await fetch(`${API}/blog/posts/`);
  if (!res.ok) throw new Error(`Error fetching posts: ${res.status}`);
  return res.json();
}

export async function fetchLinks(): Promise<LinkItem[]> {
  const res = await fetch(`${API}/linkhubs/`);
  if (!res.ok) throw new Error(`Error fetching links: ${res.status}`);
  return res.json();
}

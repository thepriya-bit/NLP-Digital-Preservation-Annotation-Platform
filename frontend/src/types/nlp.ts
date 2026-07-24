export interface RawPhrase {
  id: number;
  language: string;
  phrase: string;
  audio_url: string | null;
  submitted_by: number;
  status: string;
  created_at?: string;
}

export interface Annotation {
  id: number;
  raw_phrase_id: number;
  translated_text: string;
  pos_tags: Record<string, unknown> | null;
  named_entities: Record<string, unknown> | null;
  syntax: Record<string, unknown> | null;
  created_by: number;
  created_at?: string;
}

export interface SyntaxTagResponse {
  tokens: string[];
  pos_tags: { token: string; pos: string }[];
  named_entities: { token: string; label: string }[];
  syntax_tree: Record<string, unknown> | null;
}

export interface AnnotationCreatePayload {
  raw_phrase_id: number;
  translated_text: string;
  pos_tags?: Record<string, unknown> | null;
  named_entities?: Record<string, unknown> | null;
  syntax?: Record<string, unknown> | null;
}

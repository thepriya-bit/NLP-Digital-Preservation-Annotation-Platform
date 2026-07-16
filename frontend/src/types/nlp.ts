

export interface RawPhrase {
  id: number;
  language: string;
  phrase: string;
  audio_url: string | null; // The '| null' means it can be empty if there's no audio
  submitted_by: number;
  status: string;
  created_at: string; // Dates are sent as ISO strings over APIs
}
//create an interface for Annotaion based on raw phrase

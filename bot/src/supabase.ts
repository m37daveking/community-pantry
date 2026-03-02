import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export type Item = {
  id: string;
  name: string;
  emoji: string;
  quantity: string;
  from_name: string;
  pickup_note: string | null;
  is_taken: boolean;
  taken_at: string | null;
  created_at: string;
};

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const SUPABASE_URL = 'https://kdxrgzoopojtduadtisf.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkeHJnem9vcG9qdGR1YWR0aXNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcwNDg3MzAsImV4cCI6MjEwMjYyNDczMH0.iFU2g8V63pCWH0Zj6VpD9Sj_hNjVNMEhuu2WHMqohA4';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
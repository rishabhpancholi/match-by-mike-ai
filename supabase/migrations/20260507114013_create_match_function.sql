create or replace function match_candidates(
    query_embedding vector(1536),
    required_skills text[],
    min_experience_years int
)
returns setof candidates
language sql
as $$
   select * 
   from candidates
   where
     skills && required_skills
     and years_experience >= min_experience_years
   order by 
     embedding <=> query_embedding,
     created_at desc
   limit 10;
$$;
create extension if not exists vector;

create table candidates (
    id uuid primary key default gen_random_uuid(),
    name text,
    skills text[],
    years_experience int,
    last_ctc_inr int,
    current_location text,
    embedding vector(1536),
    created_at timestamp with time zone default current_timestamp
);


CREATE TABLE IF NOT EXISTS public.rss_articles (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Check title and link existence before inserting new articles
WITH candidates AS (
    SELECT title, link
    FROM jsonb_to_recordset($1::jsonb)
    AS x(title TEXT, link TEXT)
),
inserted AS (
    INSERT INTO rss_articles (title, link)
    SELECT DISTINCT ON (link) title, link
    FROM candidates
    WHERE title IS NOT NULL
      AND link IS NOT NULL
    ON CONFLICT (link) DO NOTHING
    RETURNING title, link
)
SELECT
    CASE
        WHEN COUNT(*) > 0 THEN 'NEW'
        ELSE 'NONE'
    END AS status,
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'title', title,
                'link', link
            )
        ),
        '[]'::jsonb
    ) AS articles
FROM inserted;
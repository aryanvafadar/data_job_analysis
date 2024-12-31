/*
What skills are required for the top paying roles, that are not at the senior or director level?
*/
WITH jobs_with_skills AS (
    SELECT
        jp.company_id,
        cd.name AS company_name,
        jp.job_title,
        jp.salary_year_avg,
        STRING_AGG(sd.skills, ', ') AS skills
    FROM
        job_postings_fact AS jp
    LEFT JOIN
        company_dim AS cd
        ON jp.company_id = cd.company_id
    LEFT JOIN
        skills_job_dim AS skd
        ON jp.job_id = skd.job_id
    LEFT JOIN
        skills_dim AS sd
        ON skd.skill_id = sd.skill_id
    WHERE 
        jp.salary_year_avg IS NOT NULL AND
        skd.skill_id IS NOT NULL
    GROUP BY
        jp.company_id, cd.name, jp.job_title, jp.salary_year_avg
)
SELECT 
    company_id,
    company_name,
    job_title,
    salary_year_avg,
    skills
FROM 
    jobs_with_skills
WHERE 
    NOT (job_title LIKE '%Senior%' OR job_title LIKE '%Director%')
ORDER BY 
    salary_year_avg DESC;


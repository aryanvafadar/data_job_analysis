/*
What are the top 3 skills that are highest in demand for remote jobs? Group by the job title and retrieve the min, max and average salary for each job by skill.
*/

-- Create a cte for remote jobs that include the skills for each job_id
WITH remote_jobs_with_skills AS (
    SELECT
        jp.job_title,
        jp.salary_year_avg,
        sd.skills
    FROM
        job_postings_fact AS jp
    INNER JOIN 
        skills_job_dim AS skd ON jp.job_id = skd.job_id
    INNER JOIN
        skills_dim AS sd ON skd.skill_id = sd.skill_id
    WHERE 
        jp.job_location = 'Anywhere' AND -- Remote only roles
        jp.salary_year_avg IS NOT NULL -- Exclude roles without salaries
),

skills_ranked AS (
    SELECT 
        rjws.job_title,
        rjws.skills,
        COUNT(*) AS skill_count,
        RANK() OVER (PARTITION BY rjws.job_title ORDER BY COUNT(*) DESC) AS skill_rank
    FROM 
        remote_jobs_with_skills AS rjws
    GROUP BY 
        rjws.job_title, rjws.skills
)

SELECT 
    sr.job_title AS position, 
    STRING_AGG(DISTINCT sr.skills, ', ') AS top_skills, -- Combine skills into a single string
    MIN(rjws.salary_year_avg) AS min_salary,
    MAX(rjws.salary_year_avg) AS max_salary,
    ROUND(AVG(rjws.salary_year_avg), 2) AS avg_salary
FROM 
    skills_ranked AS sr
INNER JOIN 
    remote_jobs_with_skills AS rjws ON sr.job_title = rjws.job_title
WHERE 
    sr.skill_rank <= 3
GROUP BY 
    sr.job_title
ORDER BY 
    sr.job_title;



/*
What are the top 3 skills that are highest in demand for remote jobs? Group by the job title and retrieve the min, max and average salary for each job.
*/

-- Create a cte for remote jobs that include the skills for each job_id
WITH remote_jobs_with_skills AS (
    SELECT
        jp.job_title_short,
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
-- cte to group by skills and job titles
skills_ranked AS (
    SELECT 
        rjws.job_title_short,
        rjws.skills,
        COUNT(*) AS skill_count,
        RANK() OVER (PARTITION BY rjws.job_title_short ORDER BY COUNT(*) DESC) AS skill_rank
    FROM 
        remote_jobs_with_skills AS rjws
    GROUP BY 
        rjws.job_title_short, rjws.skills
)

SELECT *
FROM skills_ranked
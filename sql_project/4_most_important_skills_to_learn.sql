/*
What are the top 5 most important skills to learn for entry level, mid-level and senior roles. And what is the salary band for these levels?
- We will group roles by salary bands. Entry = 50 - 80k, Mid = 80k - 120k, Senior = 120k - 175k, Exec = 175k+
*/

-- cte to group job titles by job_category (role)
WITH position_grouping AS (
    SELECT
        job_id,
        job_title,
        ROUND(salary_year_avg, 2) AS salary,
        job_location,
        CASE
            WHEN salary_year_avg BETWEEN 0 AND 79999.99 THEN 'Entry Level'
            WHEN salary_year_avg BETWEEN 80000 AND 119999.99 THEN 'Mid Level'
            WHEN salary_year_avg BETWEEN 120000 AND 174999.99 THEN 'Senior Level'
            WHEN salary_year_avg >= 175000 THEN 'Executive Level'
        ELSE NULL
    END AS job_category
    FROM job_postings_fact
    WHERE job_title IS NOT NULL AND salary_year_avg IS NOT NULL
    ORDER BY salary
),

-- cte to find the top skills by job_category descending
important_skills_by_role AS (
    SELECT
        job_category,
        COUNT(skills_dim.skills) skill_count,
        skills_dim.skills as skill,
        RANK() OVER (PARTITION BY job_category ORDER BY COUNT(skills_dim.skills) DESC) AS skill_rank
    FROM 
        position_grouping
    INNER JOIN
        skills_job_dim ON position_grouping.job_id = skills_job_dim.job_id
    INNER JOIN
        skills_dim ON skills_job_dim.skill_id = skills_dim.skill_id
    GROUP BY
        job_category, skills_dim.skills
    ORDER BY
        job_category,
        skill_count DESC
)

SELECT 
    important_skills_by_role.job_category,
    STRING_AGG(DISTINCT skill, ', ') as top_skills,
    MIN(position_grouping.salary) as min_salary,
    MAX(position_grouping.salary) as max_salary,
    ROUND(AVG(position_grouping.salary), 2) as avg_salary
FROM 
    important_skills_by_role
INNER JOIN
    position_grouping
    ON important_skills_by_role.job_category = position_grouping.job_category
WHERE
    skill_rank <= 5
GROUP BY
    important_skills_by_role.job_category
ORDER BY
    min_salary
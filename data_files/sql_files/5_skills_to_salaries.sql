/*
List of skills and their salaries
*/

WITH salary_by_skill AS (
    SELECT job_title_short, salary_year_avg, skills
    FROM job_postings_fact
    INNER JOIN
    skills_job_dim
    ON job_postings_fact.job_id = skills_job_dim.job_id
    INNER JOIN
    skills_dim
    ON skills_job_dim.skill_id = skills_dim.skill_id
    WHERE salary_year_avg IS NOT NULL
)

SELECT skills, salary_year_avg
FROM salary_by_skill
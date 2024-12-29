/*
1. What are the top paying data analyst jobs?
- Identify the top 10 highest paying data analyst roles that are available remotely.
- Focus on job postings with specified salaries.
*/

WITH jobs_with_salaries AS(
    SELECT
    jp.company_id,
    cd.name,
    jp.job_title_short,
    jp.salary_year_avg

    FROM
        job_postings_fact as jp
    LEFT JOIN
        company_dim as cd
        ON jp.company_id = cd.company_id
    WHERE
        jp.job_location = 'Anywhere'
)
SELECT 
    * 
FROM 
    jobs_with_salaries
WHERE 
    jobs_with_salaries.salary_year_avg IS NOT NULL AND
    jobs_with_salaries.job_title_short = 'Data Analyst'

ORDER BY jobs_with_salaries DESC

LIMIT 10

/*
Count the number of job postings by country
*/

WITH total_postings_by_country AS (
    SELECT job_country, COUNT(job_id) AS total_jobs
    FROM job_postings_fact
    WHERE job_country IS NOT NULL 
    GROUP BY job_country
    ORDER BY job_country DESC
)

SELECT * 
FROM total_postings_by_country
WHERE total_jobs >= 5 
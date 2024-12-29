## Introduction

This project leverages SQL to analyze job postings and identify trends in the job market for data-related roles. The queries aim to uncover actionable insights such as top-paying roles, skills required for those roles, and the most in-demand skills across different job categories. These analyses can assist job seekers, recruiters, and decision-makers in understanding the landscape of data-related positions.

## Background

The dataset analyzed in this project includes information about job postings, companies, salaries, locations, and skills associated with various roles. By using SQL, we delve into different aspects of the job market, such as:

- Identifying the highest-paying jobs in the data domain.
- Highlighting essential skills required for top-paying roles.
- Discovering skills in high demand for remote jobs.
- Grouping job titles by salary levels to determine skill relevance for entry-level, mid-level, senior, and executive positions.

The queries are structured to extract meaningful insights by combining, filtering, and aggregating data. Techniques such as Common Table Expressions (CTEs), window functions, and string aggregation are utilized to perform advanced analyses.

## Folders

- The SQL files can be found within the sql_project folder here - [SQL FILES](/sql_project/)
- THE CSV files used to create the database can be found here - [CSV FILES](/csv_files/)

## Tools Used

This project is implemented using:

1. SQL:

- All queries are executed in a SQL-based environment to interact with structured datasets.
- Advanced SQL techniques such as CTEs, window functions (RANK()), and aggregation functions (STRING_AGG, ROUND) are heavily used.

2. Database Tables:

- job_postings_fact: Contains job postings with details such as job title, location, and salary.
- company_dim: Contains information about companies.
- skills_job_dim: Links job postings to relevant skills.
- skills_dim: Lists skills required for various job postings.

The queries are designed to be modular, focusing on individual aspects of the data while enabling flexible analysis.

## Analysis

The SQL queries in this project provide a multi-faceted analysis of job market data. Below are the key analyses performed:

1. Top-Paying Jobs:

- Identified the top 10 highest-paying roles for remote data analyst positions.
- Filtered job postings to include only those with non-null salary data for accurate comparisons.

2. Skills for Top-Paying Jobs:

- Extracted skills associated with high-paying roles that are not at senior or director levels.
- Aggregated skills into a single line for each job title using STRING_AGG, making the output concise and readable.

3. Highest Demand Skills for Remote Jobs:

- Analyzed remote job postings to determine the top 3 most frequently requested skills for each job title.
- Used window functions (RANK()) and grouping to rank skills by frequency within each job title.

4. Important Skills by Role:

- Grouped job titles into categories (e.g., Entry Level, Mid Level, Senior Level, Executive Level) based on salary bands.
- Identified the top 5 skills in demand for each category and calculated the salary range for each level.

## Learnings

1. Top-Paying Jobs:

- Remote data analyst roles can command competitive salaries, especially at higher levels. However, salary visibility (non-null salary data) is critical for meaningful analysis.

2. Skills Required for High-Paying Roles:

- High-paying roles consistently emphasize technical skills such as Python, SQL, and data visualization tools.
- Non-senior roles often prioritize practical, hands-on skills rather than leadership or managerial expertise.

3. Demand for Remote Job Skills:

- Skills like Python, SQL, and machine learning are highly sought after across multiple job titles for remote positions.
- The ranking of skills provides insights into what employers value most, enabling targeted skill development.

4. Skills by Role Category:

- Entry-level roles focus on foundational skills (e.g., SQL, Excel, basic programming).
- Mid-level roles require more specialized tools and languages (e.g., Python, Power BI).
- Senior and executive roles emphasize advanced technical expertise (e.g., cloud computing, machine learning) alongside leadership abilities.

## Query Examples

### Top Skills Requested by Employers For Non Senior or Director Roles

```sql
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
```

### Top Skills Required by Job Category (Entry, Mid, Senior & Executive Level)

```sql
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
```

## Conclusions

1. Strategic Skill Development:

- Aspiring professionals should focus on mastering high-demand skills like Python, SQL, and machine learning to increase employability and earning potential.
- Entry-level job seekers should start with foundational skills, while those aiming for senior roles should pursue expertise in advanced tools and leadership.

2. Value of Remote Work:

- Remote jobs in the data field offer competitive salaries, making them a viable option for professionals seeking flexibility without sacrificing earnings.

3. Salary-Based Career Planning:

- Categorizing jobs by salary bands helps individuals set realistic expectations and tailor their skill-building efforts for specific levels.

4. Insights for Employers:

- Companies can use this analysis to benchmark salaries and refine job descriptions to attract top talent by highlighting in-demand skills.

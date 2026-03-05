CREATE OR REPLACE VIEW player_value_percentile AS
WITH base AS (
    SELECT
        ps.name,
        ps.team,
        ps.season,
        ps.mpg,
        ps.gp,
        s.salary,
        (ps.p_r_a / NULLIF(ps.mpg, 0)) AS ipm
    FROM player_stats ps
    JOIN player_salary s
        ON ps.name = s.name
       AND ps.season = s.season
    WHERE ps.mpg >= 15
      AND ps.gp >= 20
),

percentiles AS (
    SELECT
        *,
        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY ipm
        ) AS impact_percentile,
        PERCENT_RANK() OVER (
            PARTITION BY season
            ORDER BY salary
        ) AS salary_percentile
    FROM base
)

SELECT
    name,
    team,
    season,
    salary,
    ipm,
    impact_percentile,
    salary_percentile,
    (impact_percentile - salary_percentile) AS value_gap,
    CASE
        WHEN impact_percentile >= 0.75 AND salary_percentile <= 0.40
            THEN 'Underpaid'
        WHEN impact_percentile <= 0.40 AND salary_percentile >= 0.75
            THEN 'Overpaid'
        ELSE 'Fair Value'
    END AS contract_label
FROM percentiles;
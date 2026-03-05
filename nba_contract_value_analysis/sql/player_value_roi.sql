CREATE OR REPLACE VIEW player_value_roi AS
WITH cap_data AS (
    SELECT '2022-2023' AS season, 123655000 AS cap_amount
    UNION ALL SELECT '2023-2024', 136021000
    UNION ALL SELECT '2024-2025', 140588000
    UNION ALL SELECT '2025-2026', 154647000
),

impact_calc AS (
    SELECT
        ps.name,
        ps.team,
        ps.season,
        ps.mpg,
        ps.gp,
        s.salary,
        cd.cap_amount,
        (s.salary / cd.cap_amount) * 100 AS cap_hit_pct,
        (ps.p_r_a / NULLIF(ps.mpg, 0)) AS ipm
    FROM player_stats ps
    JOIN player_salary s
        ON ps.name = s.name
       AND ps.season = s.season
    JOIN cap_data cd
        ON ps.season = cd.season
    WHERE ps.mpg >= 15
      AND ps.gp >= 20
)

SELECT
    name,
    team,
    season,
    salary,
    cap_hit_pct,
    ipm,
    (ipm / NULLIF(cap_hit_pct, 0)) AS value_index,
    RANK() OVER (
        PARTITION BY season
        ORDER BY (ipm / NULLIF(cap_hit_pct, 0)) DESC
    ) AS seasonal_rank
FROM impact_calc;
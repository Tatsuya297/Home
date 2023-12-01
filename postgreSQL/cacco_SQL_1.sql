WITH subtable AS (
    SELECT
        EXTRACT('year' FROM o_orderdate) AS year
        , EXTRACT('month' FROM o_orderdate) AS month
        , SUM(o_totalprice) AS sum_total
        , LAG(SUM(o_totalprice)) OVER (PARTITION BY o_custkey ORDER BY o_orderdate) AS sum_before 
    FROM 
        orders
    WHERE
        o_orderdate < '1995-01-01'
    GROUP BY
        o_custkey
        , o_orderdate
)

SELECT
    year
    , month
    , COUNT(*) AS o_orderdate_cnt
FROM
    subtable
WHERE
    sum_total >= sum_before
GROUP BY
    year
    , month
HAVING
    COUNT(*) >= 8500
ORDER BY 
    year
    , month
;
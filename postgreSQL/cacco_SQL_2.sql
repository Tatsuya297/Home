WITH subtable AS (
    SELECT
        EXTRACT('year' FROM o_orderdate) AS year
        , EXTRACT('month' FROM o_orderdate) AS month
        , o_custkey
        , SUM(o_totalprice) AS totalprice
        , LAG(SUM(o_totalprice)) OVER (PARTITION BY o_custkey ORDER BY o_orderdate) AS LAG1 
        , LAG(SUM(o_totalprice),2) OVER (PARTITION BY o_custkey ORDER BY o_orderdate) AS LAG2
    FROM 
        orders
    WHERE
        o_orderdate < '1994-01-01'
    GROUP BY
        o_custkey
        , o_orderdate
)
SELECT
    year
    , month
    , COUNT(*)
    , SUM(totalprice) AS totalprice_sum
FROM
    subtable
WHERE
    LAG1 IS NOT NULL
    AND
    LAG2 IS NULL
GROUP BY
    year
    , month
HAVING
    COUNT(*)  >= 2000
ORDER BY 
    year
    , month
;

WITH subtable AS (
    SELECT
        EXTRACT('year' FROM o_orderdate) AS year
        , EXTRACT('month' FROM o_orderdate) AS month
        , o_totalprice
        , LAG(o_totalprice) OVER (PARTITION BY o_custkey ORDER BY o_orderdate)
    FROM 
        orders
    WHERE
        o_orderdate < '1995-01-01'
)

SELECT
    year
    , month
    , COUNT(*) AS o_order_cnt
FROM
    subtable
WHERE
    o_totalprice >= LAG
GROUP BY
    year
    , month
HAVING
    COUNT(*) >= 8500
ORDER BY 
    year
    , month
;

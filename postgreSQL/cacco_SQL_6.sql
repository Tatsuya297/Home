WITH cust_orders AS (
    SELECT
        o_orderdate
        , o_custkey
        , SUM(o_totalprice) AS totalprice
    FROM 
        orders
    GROUP BY
        o_custkey
        , o_orderdate
)
,low_cust_orders AS (
    SELECT
        o_custkey
        , SUM(CASE WHEN totalprice < 20000 THEN totalprice ELSE NULL END) AS o_sumprice
        , MAX(o_orderdate) AS o_latestdate
    FROM 
        cust_orders
    GROUP BY
        o_custkey
)
SELECT
    o_custkey
    , o_latestdate
    , o_sumprice
FROM
    low_cust_orders
WHERE
    o_latestdate >= '1998-01-04'
    AND
    o_sumprice IS NOT NULL
ORDER BY 
    o_custkey
;

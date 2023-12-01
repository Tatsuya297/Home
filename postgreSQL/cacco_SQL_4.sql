SELECT
    c_custkey
    , c_name
    , CASE WHEN SUM(o_totalprice) IS NULL THEN 0 ELSE SUM(o_totalprice) END AS o_sumprice
FROM
    customer
    LEFT JOIN
    orders
    ON c_custkey = o_custkey
GROUP BY
    c_custkey
    , c_name
LIMIT 
    100
;
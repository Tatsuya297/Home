SELECT
    n_name
    , COUNT(*) AS count_cust
FROM
    customer
JOIN
    nation
ON 
    c_nationkey = n_nationkey
WHERE
    c_custkey 
    IN (
        SELECT 
            c_custkey
        FROM
            customer
        LEFT JOIN
            orders
        ON 
            c_custkey = o_custkey
        JOIN
            nation
        ON 
            c_nationkey = n_nationkey 
        GROUP BY
            c_custkey
        HAVING
            MIN(o_orderdate) >= '1997-01-01'
            OR
            SUM(o_totalprice) IS NULL
        )
    
GROUP BY
    n_name
ORDER BY
    n_name
;
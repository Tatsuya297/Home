--- 対象商品の併売率を求める

--- 1.レシートデータ全体から、2022年、首都圏のコンビニXにおける「商品A」のレシートデータを抽出
WITH tmp1 AS (
    SELECT
        *
        ,SUBSTRING(購入日,1,4) AS buy_year
    FROM receipt_data
    WHERE
        都道府県 IN ('東京都','千葉県','神奈川県','埼玉県')
        AND 流通名 = 'コンビニX'
        AND buy_year = '2022'
        AND 商品名 = '商品A'

--- 2.レシートデータ全体から、2022年、首都圏のコンビニXにおける「商品A」を含む購買のレシートデータを抽出
),tmp2 AS(
SELECT
    レシートid,商品名,参考細分類名称
FROM
    receipt_data
WHERE
    レシートid IN (SELECT レシートid
                FROM receipt_data
                WHERE 商品名 = '商品A')
                    AND 購入日 BETWEEN '2022-01-01' AND '2023-01-01'
                    AND 流通名 = 'コンビニX'
                    AND 都道府県 IN ('東京都','千葉県','神奈川県','埼玉県')

--- 3.1,2で抽出したデータを使用して、商品Aにおける併売率を計算
),tmp3 AS(
    SELECT
        '商品A' AS 品1
        ,参考細分類名称
        ,COUNT(DISTINCT レシートid) AS heibai_count --商品Aを含む購買において、併売数(商品A以外も購入しているレシート数)をカウント
        ,CAST(heibai_count AS float) / (SELECT COUNT(レシートid) FROM tmp1) * 100 AS rate_heibai --併売率 = 併売のあったレシート数/「商品A」を含むレシートデータ数
    FROM
        tmp2
    WHERE
        商品名 != '商品A'
    GROUP BY
        参考細分類名称
    ORDER BY
        rate_heibai DESC
)
--- 4計算結果を出力
SELECT
    *
FROM
    tmp3
;

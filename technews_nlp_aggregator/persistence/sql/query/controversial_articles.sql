SELECT
    `S`.`ID`         AS `ID`,
    `S`.`DATE`       AS `DATE`,
    `S`.`TITLE`      AS `TITLE`,
    `S`.`URL`        AS `URL`,
    sum(`S`.`SCORE`) AS `SUM_SCORE`
  FROM (SELECT
          `TFIDF_SCORE`.`ID_1`       AS `ID`,
          `TFIDF_SCORE`.`DATE_1`     AS `DATE`,
          `TFIDF_SCORE`.`TITLE_1`    AS `TITLE`,
          `TFIDF_SCORE`.`URL_1`      AS `URL`,
          `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
        FROM `tnaggregator`.`TFIDF_SCORE`
        WHERE SUBSTRING_INDEX(URL_1, '.com', 1) <> SUBSTRING_INDEX(URL_2, '.com', 1)
        UNION SELECT
                `TFIDF_SCORE`.`ID_2`       AS `ID`,
                `TFIDF_SCORE`.`DATE_2`     AS `DATE`,
                `TFIDF_SCORE`.`TITLE_2`    AS `TITLE`,
                `TFIDF_SCORE`.`URL_2`      AS `URL`,
                `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
              FROM `tnaggregator`.`TFIDF_SCORE`
              WHERE SUBSTRING_INDEX(URL_1, '.com', 1) <> SUBSTRING_INDEX(URL_2, '.com', 1)

       ) `S`
  GROUP BY `S`.`ID`, `S`.`DATE`, `S`.`TITLE`, `S`.`URL`
  ORDER BY `S`.`DATE` DESC, `SUM_SCORE` DESC;
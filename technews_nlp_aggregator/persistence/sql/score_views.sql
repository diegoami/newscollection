create or replace view DOC2VEC_SCORE as
SELECT
    `A1`.`AIN_ID`      AS `ID_1`,
    `A2`.`AIN_ID`      AS `ID_2`,
    `A1`.`AIN_DATE`      AS `DATE_1`,
    `A2`.`AIN_DATE`      AS `DATE_2`,
    `A1`.`AIN_TITLE`     AS `TITLE_1`,
    `A2`.`AIN_TITLE`     AS `TITLE_2`,
    `A1`.`AIN_URL`       AS `URL_1`,
    `A2`.`AIN_URL`       AS `URL_2`,
    `S`.`SST_SIMILARITY` AS `SIMILARITY`
  FROM `tnaggregator`.`ARTICLE_INFO` `A1`
    JOIN `tnaggregator`.`ARTICLE_INFO` `A2`
    JOIN `tnaggregator`.`SAME_STORY` `S`
  WHERE ((`S`.`SST_AIN_ID_1` = `A1`.`AIN_ID`) AND (`S`.`SST_AIN_ID_2` = `A2`.`AIN_ID`) AND
         (`S`.`SST_AGENT` = 'DOC2VEC-V1-500'))
 -- AND SUBSTRING_INDEX(A1.AIN_URL, '.com', 1) <> SUBSTRING_INDEX(A2.AIN_URL, '.com', 1)
  ORDER BY `A1`.`AIN_DATE` DESC;



create or replace view TFIDF_SCORE as
SELECT
    `A1`.`AIN_ID`        AS `ID_1`,
    `A2`.`AIN_ID`        AS `ID_2`,
    `A1`.`AIN_DATE`      AS `DATE_1`,
    `A2`.`AIN_DATE`      AS `DATE_2`,
    `A1`.`AIN_TITLE`     AS `TITLE_1`,
    `A2`.`AIN_TITLE`     AS `TITLE_2`,
    `A1`.`AIN_URL`       AS `URL_1`,
    `A2`.`AIN_URL`       AS `URL_2`,
    `S`.`SST_SIMILARITY` AS `SIMILARITY`
  FROM `tnaggregator`.`ARTICLE_INFO` `A1`
    JOIN `tnaggregator`.`ARTICLE_INFO` `A2`
    JOIN `tnaggregator`.`SAME_STORY` `S`
  WHERE ((`S`.`SST_AIN_ID_1` = `A1`.`AIN_ID`) AND (`S`.`SST_AIN_ID_2` = `A2`.`AIN_ID`) AND
         (`S`.`SST_AGENT` = 'TFIDF-V1-500'))
 -- AND SUBSTRING_INDEX(A1.AIN_URL, '.com', 1) <> SUBSTRING_INDEX(A2.AIN_URL, '.com', 1)
  ORDER BY `A1`.`AIN_DATE` DESC;



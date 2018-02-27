create or replace view CONTROVERSIAL_ARTICLES as
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
        FROM `TFIDF_SCORE`
        UNION SELECT
                `TFIDF_SCORE`.`ID_2`       AS `ID`,
                `TFIDF_SCORE`.`DATE_2`     AS `DATE`,
                `TFIDF_SCORE`.`TITLE_2`    AS `TITLE`,
                `TFIDF_SCORE`.`URL_2`      AS `URL`,
                `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
              FROM `TFIDF_SCORE`) `S`
  GROUP BY `S`.`ID`, `S`.`DATE`, `S`.`TITLE`, `S`.`URL`
  ORDER BY `S`.`DATE` DESC, `SUM_SCORE` DESC;

create or replace view DOC2VEC_SCORE as
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
  FROM ((`ARTICLE_INFO` `A1`
    JOIN `ARTICLE_INFO` `A2`) JOIN `SAME_STORY` `S`)
  WHERE ((`S`.`SST_AIN_ID_1` = `A1`.`AIN_ID`) AND (`S`.`SST_AIN_ID_2` = `A2`.`AIN_ID`) AND
         (`S`.`SST_AGENT` = 'DOC2VEC-V4-600') AND
         (substring_index(`A1`.`AIN_URL`, '.com', 1) <> substring_index(`A2`.`AIN_URL`, '.com', 1)))
  ORDER BY `A1`.`AIN_DATE` DESC;

create or replace view DOC2VEC_SCORE_NORM as
SELECT
    `S`.`ID`          AS `ID`,
    `S`.`OTHER_ID`    AS `OTHER_ID`,
    `S`.`DATE`        AS `DATE`,
    `S`.`OTHER_DATE`  AS `OTHER_DATE`,
    `S`.`TITLE`       AS `TITLE`,
    `S`.`OTHER_TITLE` AS `OTHER_TITLE`,
    `S`.`URL`         AS `URL`,
    `S`.`OTHER_URL`   AS `OTHER_URL`,
    `S`.`SCORE`       AS `SCORE`
  FROM (SELECT
          `DOC2VEC_SCORE`.`ID_1`       AS `ID`,
          `DOC2VEC_SCORE`.`ID_2`       AS `OTHER_ID`,
          `DOC2VEC_SCORE`.`DATE_1`     AS `DATE`,
          `DOC2VEC_SCORE`.`DATE_2`     AS `OTHER_DATE`,
          `DOC2VEC_SCORE`.`TITLE_1`    AS `TITLE`,
          `DOC2VEC_SCORE`.`TITLE_2`    AS `OTHER_TITLE`,
          `DOC2VEC_SCORE`.`URL_1`      AS `URL`,
          `DOC2VEC_SCORE`.`URL_2`      AS `OTHER_URL`,
          `DOC2VEC_SCORE`.`SIMILARITY` AS `SCORE`
        FROM `DOC2VEC_SCORE`
        UNION SELECT
                `DOC2VEC_SCORE`.`ID_2`       AS `ID`,
                `DOC2VEC_SCORE`.`ID_1`       AS `OTHER_ID`,
                `DOC2VEC_SCORE`.`DATE_2`     AS `DATE`,
                `DOC2VEC_SCORE`.`DATE_1`     AS `OTHER_DATE`,
                `DOC2VEC_SCORE`.`TITLE_2`    AS `TITLE`,
                `DOC2VEC_SCORE`.`TITLE_1`    AS `OTHER_TITLE`,
                `DOC2VEC_SCORE`.`URL_2`      AS `URL`,
                `DOC2VEC_SCORE`.`URL_1`      AS `OTHER_URL`,
                `DOC2VEC_SCORE`.`SIMILARITY` AS `SCORE`
              FROM `DOC2VEC_SCORE`) `S`;

create view P_SCORES as
SELECT
    `P`.`PRED_AIN_ID_1` AS `ID_1`,
    `P`.`PRED_AIN_ID_2` AS `ID_2`,
    `P`.`PRED_PROBA`    AS `P_SCORE`,
    `P`.`PRED_CAT`      AS `C_SCORE`,
    `P`.`PRED_REGR`     AS `R_SCORE`,
    `P`.`PRED_VERSION`  AS `VERSION`,
    `A1`.`AIN_TITLE`    AS `TITLE_1`,
    `A2`.`AIN_TITLE`    AS `TITLE_2`,
    `A1`.`AIN_DATE`     AS `DATE_1`,
    `A2`.`AIN_DATE`     AS `DATE_2`,
    `U`.`SCORE`         AS `U_SCORE`,
    `A1`.`AIN_URL`      AS `URL_1`,
    `A2`.`AIN_URL`      AS `URL_2`
  FROM (((`tnaggregator`.`PREDICTIONS` `P` LEFT JOIN `tnaggregator`.`ARTICLE_INFO` `A1`
      ON ((`P`.`PRED_AIN_ID_1` = `A1`.`AIN_ID`))) LEFT JOIN `tnaggregator`.`ARTICLE_INFO` `A2`
      ON ((`P`.`PRED_AIN_ID_2` = `A2`.`AIN_ID`))) LEFT JOIN (SELECT
                                                               avg(
                                                                   `tnaggregator`.`SAME_STORY_USER`.`SSU_SIMILARITY`) AS `SCORE`,
                                                               `tnaggregator`.`SAME_STORY_USER`.`SSU_AIN_ID_1`        AS `SSU_AIN_ID_1`,
                                                               `tnaggregator`.`SAME_STORY_USER`.`SSU_AIN_ID_2`        AS `SSU_AIN_ID_2`
                                                             FROM `tnaggregator`.`SAME_STORY_USER`
                                                             GROUP BY `tnaggregator`.`SAME_STORY_USER`.`SSU_AIN_ID_1`,
                                                               `tnaggregator`.`SAME_STORY_USER`.`SSU_AIN_ID_2`) `U`
      ON (((`P`.`PRED_AIN_ID_1` = `U`.`SSU_AIN_ID_1`) AND (`P`.`PRED_AIN_ID_2` = `U`.`SSU_AIN_ID_2`))))
  ORDER BY `A2`.`AIN_DATE` DESC, `A1`.`AIN_DATE` DESC, `U`.`SCORE` DESC, `P`.`PRED_PROBA` DESC, `A2`.`AIN_TITLE` DESC,
    `A1`.`AIN_TITLE` DESC;



create or replace view TEST_SCORES as
SELECT
    `SCORES`.`SCO_AIN_ID_1`     AS `SCO_AIN_ID_1`,
    `SCORES`.`SCO_AIN_ID_2`     AS `SCO_AIN_ID_2`,
    `SCORES`.`SCO_T_TITLE`      AS `SCO_T_TITLE`,
    `SCORES`.`SCO_D_TITLE`      AS `SCO_D_TITLE`,
    `SCORES`.`SCO_T_TEXT`       AS `SCO_T_TEXT`,
    `SCORES`.`SCO_D_TEXT`       AS `SCO_D_TEXT`,
    `SCORES`.`SCO_T_SUMMARY`    AS `SCO_T_SUMMARY`,
    `SCORES`.`SCO_D_SUMMARY`    AS `SCO_D_SUMMARY`,
    `SCORES`.`SCO_T_SUMMARY_2`  AS `SCO_T_SUMMARY_2`,
    `SCORES`.`SCO_D_SUMMARY_2`  AS `SCO_D_SUMMARY_2`,
    `SCORES`.`SCO_CW_TITLE`     AS `SCO_CW_TITLE`,
    `SCORES`.`SCO_CW_SUMMARY`   AS `SCO_CW_SUMMARY`,
    `SCORES`.`SCO_CW_SUMMARY_2` AS `SCO_CW_SUMMARY_2`,
    `SCORES`.`SCO_CW_TEXT`      AS `SCO_CW_TEXT`,
    `SCORES`.`SCO_DAYS`         AS `SCO_DAYS`,
    `SCORES`.`SCO_VERSION`      AS `SCO_VERSION`
  FROM (`SCORES`
    JOIN (SELECT
            `SAME_STORY`.`SST_AIN_ID_1` AS `SST_AIN_ID_1`,
            `SAME_STORY`.`SST_AIN_ID_2` AS `SST_AIN_ID_2`
          FROM `SAME_STORY`
          GROUP BY `SAME_STORY`.`SST_AIN_ID_1`,
            `SAME_STORY`.`SST_AIN_ID_2`) `SAME_STORY_GRP`)
  WHERE ((`SCORES`.`SCO_AIN_ID_1` = `SAME_STORY_GRP`.`SST_AIN_ID_1`) AND
         (`SCORES`.`SCO_AIN_ID_2` = `SAME_STORY_GRP`.`SST_AIN_ID_2`));

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
  FROM ((`ARTICLE_INFO` `A1`
    JOIN `ARTICLE_INFO` `A2`) JOIN `SAME_STORY` `S`)
  WHERE (
    (`S`.`SST_AIN_ID_1` = `A1`.`AIN_ID`) AND (`S`.`SST_AIN_ID_2` = `A2`.`AIN_ID`) AND (`S`.`SST_AGENT` = 'TFIDF-V4-500')
    AND (substring_index(`A1`.`AIN_URL`, '.com', 1) <> substring_index(`A2`.`AIN_URL`, '.com', 1)))
  ORDER BY `A1`.`AIN_DATE` DESC;

create or replace view TFIDF_SCORE_NORM as
SELECT
    `S`.`ID`          AS `ID`,
    `S`.`OTHER_ID`    AS `OTHER_ID`,
    `S`.`DATE`        AS `DATE`,
    `S`.`OTHER_DATE`  AS `OTHER_DATE`,
    `S`.`TITLE`       AS `TITLE`,
    `S`.`OTHER_TITLE` AS `OTHER_TITLE`,
    `S`.`URL`         AS `URL`,
    `S`.`OTHER_URL`   AS `OTHER_URL`,
    `S`.`SCORE`       AS `SCORE`
  FROM (SELECT
          `TFIDF_SCORE`.`ID_1`       AS `ID`,
          `TFIDF_SCORE`.`ID_2`       AS `OTHER_ID`,
          `TFIDF_SCORE`.`DATE_1`     AS `DATE`,
          `TFIDF_SCORE`.`DATE_2`     AS `OTHER_DATE`,
          `TFIDF_SCORE`.`TITLE_1`    AS `TITLE`,
          `TFIDF_SCORE`.`TITLE_2`    AS `OTHER_TITLE`,
          `TFIDF_SCORE`.`URL_1`      AS `URL`,
          `TFIDF_SCORE`.`URL_2`      AS `OTHER_URL`,
          `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
        FROM `TFIDF_SCORE`
        UNION SELECT
                `TFIDF_SCORE`.`ID_2`       AS `ID`,
                `TFIDF_SCORE`.`ID_1`       AS `OTHER_ID`,
                `TFIDF_SCORE`.`DATE_2`     AS `DATE`,
                `TFIDF_SCORE`.`DATE_1`     AS `OTHER_DATE`,
                `TFIDF_SCORE`.`TITLE_2`    AS `TITLE`,
                `TFIDF_SCORE`.`TITLE_1`    AS `OTHER_TITLE`,
                `TFIDF_SCORE`.`URL_2`      AS `URL`,
                `TFIDF_SCORE`.`URL_1`      AS `OTHER_URL`,
                `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
              FROM `TFIDF_SCORE`) `S`;

create or replace view TRAIN_SCORES as
SELECT
    `SCORES`.`SCO_AIN_ID_1`     AS `SCO_AIN_ID_1`,
    `SCORES`.`SCO_AIN_ID_2`     AS `SCO_AIN_ID_2`,
    `SCORES`.`SCO_T_TITLE`      AS `SCO_T_TITLE`,
    `SCORES`.`SCO_D_TITLE`      AS `SCO_D_TITLE`,
    `SCORES`.`SCO_T_TEXT`       AS `SCO_T_TEXT`,
    `SCORES`.`SCO_D_TEXT`       AS `SCO_D_TEXT`,
    `SCORES`.`SCO_T_SUMMARY`    AS `SCO_T_SUMMARY`,
    `SCORES`.`SCO_D_SUMMARY`    AS `SCO_D_SUMMARY`,
    `SCORES`.`SCO_T_SUMMARY_2`  AS `SCO_T_SUMMARY_2`,
    `SCORES`.`SCO_D_SUMMARY_2`  AS `SCO_D_SUMMARY_2`,
    `SCORES`.`SCO_CW_TITLE`     AS `SCO_CW_TITLE`,
    `SCORES`.`SCO_CW_SUMMARY`   AS `SCO_CW_SUMMARY`,
    `SCORES`.`SCO_CW_SUMMARY_2` AS `SCO_CW_SUMMARY_2`,
    `SCORES`.`SCO_CW_TEXT`      AS `SCO_CW_TEXT`,
    `SCORES`.`SCO_DAYS`         AS `SCO_DAYS`,
    `SCORES`.`SCO_VERSION`      AS `SCO_VERSION`,
    `SAME_STORY_USER_GRP`.`SSU_SCORE`          AS `SCO_USER`
  FROM (`SCORES`
    JOIN (SELECT
            `SAME_STORY_USER`.`SSU_AIN_ID_1`        AS `SSU_AIN_ID_1`,
            `SAME_STORY_USER`.`SSU_AIN_ID_2`        AS `SSU_AIN_ID_2`,
            avg(`SAME_STORY_USER`.`SSU_SIMILARITY`) AS `SSU_SCORE`
          FROM `SAME_STORY_USER`
          GROUP BY `SAME_STORY_USER`.`SSU_AIN_ID_1`,
            `SAME_STORY_USER`.`SSU_AIN_ID_2`) `SAME_STORY_USER_GRP`)
  WHERE ((`SCORES`.`SCO_AIN_ID_1` = `SAME_STORY_USER_GRP`.`SSU_AIN_ID_1`) AND
         (`SCORES`.`SCO_AIN_ID_2` = `SAME_STORY_USER_GRP`.`SSU_AIN_ID_2`));


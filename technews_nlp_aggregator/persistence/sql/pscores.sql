create view P_SCORES as
SELECT
    `P`.`PRED_AIN_ID_1` AS `ID_1`,
    `P`.`PRED_AIN_ID_2` AS `ID_2`,
    `P`.`PRED_PROBA`    AS `P_SCORE`,
    `A1`.`AIN_TITLE`    AS `TITLE_1`,
    `A2`.`AIN_TITLE`    AS `TITLE_2`,
    `A1`.`AIN_DATE`     AS `DATE_1`,
    `A2`.`AIN_DATE`     AS `DATE_2`,
    `U`.`SCORE`         AS `U_SCORE`,
    `A1`.`AIN_URL`      AS `URL_1`,
    `A2`.`AIN_URL`      AS `URL_2`
  FROM (((`tnaggregator_phrases`.`PREDICTIONS` `P` LEFT JOIN `tnaggregator_phrases`.`ARTICLE_INFO` `A1`
      ON ((`P`.`PRED_AIN_ID_1` = `A1`.`AIN_ID`))) LEFT JOIN `tnaggregator_phrases`.`ARTICLE_INFO` `A2`
      ON ((`P`.`PRED_AIN_ID_2` = `A2`.`AIN_ID`))) LEFT JOIN (SELECT
                                                               avg(
                                                                   `tnaggregator_phrases`.`SAME_STORY_USER`.`SSU_SIMILARITY`) AS `SCORE`,
                                                               `tnaggregator_phrases`.`SAME_STORY_USER`.`SSU_AIN_ID_1`        AS `SSU_AIN_ID_1`,
                                                               `tnaggregator_phrases`.`SAME_STORY_USER`.`SSU_AIN_ID_2`        AS `SSU_AIN_ID_2`
                                                             FROM `tnaggregator_phrases`.`SAME_STORY_USER`
                                                             GROUP BY
                                                               `tnaggregator_phrases`.`SAME_STORY_USER`.`SSU_AIN_ID_1`,
                                                               `tnaggregator_phrases`.`SAME_STORY_USER`.`SSU_AIN_ID_2`) `U`
      ON (((`P`.`PRED_AIN_ID_1` = `U`.`SSU_AIN_ID_1`) AND (`P`.`PRED_AIN_ID_2` = `U`.`SSU_AIN_ID_2`))))
  ORDER BY `A2`.`AIN_DATE` DESC, `A1`.`AIN_DATE` DESC, `U`.`SCORE` DESC, `P`.`PRED_PROBA` DESC, `A2`.`AIN_TITLE` DESC,
    `A1`.`AIN_TITLE` DESC;


CREATE OR REPLACE VIEW TFIDF_SCORE_NORM AS
SELECT * FROM

(SELECT
   `TFIDF_SCORE`.`ID_1`       AS `ID`,
   `TFIDF_SCORE`.`ID_2`       AS `OTHER_ID`,
   `TFIDF_SCORE`.`DATE_1`     AS `DATE`,
   `TFIDF_SCORE`.`DATE_2`     AS `OTHER_DATE`,
   `TFIDF_SCORE`.`TITLE_1`    AS `TITLE`,
   `TFIDF_SCORE`.`TITLE_2`    AS `OTHER_TITLE`,
   `TFIDF_SCORE`.`URL_1`      AS `URL`,
   `TFIDF_SCORE`.`URL_2`      AS `OTHER_URL`,
   `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
 FROM `tnaggregator`.`TFIDF_SCORE`
 UNION
 SELECT
   `TFIDF_SCORE`.`ID_2`       AS `ID`,
   `TFIDF_SCORE`.`ID_1`       AS `OTHER_ID`,
   `TFIDF_SCORE`.`DATE_2`     AS `DATE`,
   `TFIDF_SCORE`.`DATE_1`     AS `OTHER_DATE`,
   `TFIDF_SCORE`.`TITLE_2`    AS `TITLE`,
   `TFIDF_SCORE`.`TITLE_1`    AS `OTHER_TITLE`,
   `TFIDF_SCORE`.`URL_2`      AS `URL`,
   `TFIDF_SCORE`.`URL_1`      AS `OTHER_URL`,
   `TFIDF_SCORE`.`SIMILARITY` AS `SCORE`
 FROM `tnaggregator`.`TFIDF_SCORE`
) S;


CREATE OR REPLACE VIEW DOC2VEC_SCORE_NORM AS
SELECT * FROM

(SELECT
   `DOC2VEC_SCORE`.`ID_1`       AS `ID`,
   `DOC2VEC_SCORE`.`ID_2`       AS `OTHER_ID`,
   `DOC2VEC_SCORE`.`DATE_1`     AS `DATE`,
   `DOC2VEC_SCORE`.`DATE_2`     AS `OTHER_DATE`,
   `DOC2VEC_SCORE`.`TITLE_1`    AS `TITLE`,
   `DOC2VEC_SCORE`.`TITLE_2`    AS `OTHER_TITLE`,
   `DOC2VEC_SCORE`.`URL_1`      AS `URL`,
   `DOC2VEC_SCORE`.`URL_2`      AS `OTHER_URL`,
   `DOC2VEC_SCORE`.`SIMILARITY` AS `SCORE`
 FROM `tnaggregator`.`DOC2VEC_SCORE`
 UNION
 SELECT
   `DOC2VEC_SCORE`.`ID_2`       AS `ID`,
   `DOC2VEC_SCORE`.`ID_1`       AS `OTHER_ID`,
   `DOC2VEC_SCORE`.`DATE_2`     AS `DATE`,
   `DOC2VEC_SCORE`.`DATE_1`     AS `OTHER_DATE`,
   `DOC2VEC_SCORE`.`TITLE_2`    AS `TITLE`,
   `DOC2VEC_SCORE`.`TITLE_1`    AS `OTHER_TITLE`,
   `DOC2VEC_SCORE`.`URL_2`      AS `URL`,
   `DOC2VEC_SCORE`.`URL_1`      AS `OTHER_URL`,
   `DOC2VEC_SCORE`.`SIMILARITY` AS `SCORE`
 FROM `tnaggregator`.`DOC2VEC_SCORE`
) S;
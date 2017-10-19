CREATE OR REPLACE VIEW TFIDF_SCORE AS
SELECT A1.AIN_DATE AS DATE_1, A2.AIN_DATE AS DATE_2, A1.AIN_TITLE AS TITLE_1, A2.AIN_TITLE AS TITLE_2,
     A1.AIN_URL AS URL_1, A2.AIN_URL AS URL_2, S.SST_SIMILARITY AS SIMILARITY
   FROM          ARTICLE_INFO A1,
                 ARTICLE_INFO A2,
                 SAME_STORY S
   WHERE S.SST_AIN_ID_1 = A1.AIN_ID   AND  S.SST_AIN_ID_2   = A2.AIN_ID AND S.SST_AGENT = 'TFIDF-V1-500'
   ORDER BY A1.AIN_DATE DESC;

CREATE OR REPLACE VIEW DOC2VEC_SCORE AS
SELECT A1.AIN_DATE AS DATE_1, A2.AIN_DATE AS DATE_2, A1.AIN_TITLE AS TITLE_1, A2.AIN_TITLE AS TITLE_2,
     A1.AIN_URL AS URL_1, A2.AIN_URL AS URL_2, S.SST_SIMILARITY AS SIMILARITY
   FROM          ARTICLE_INFO A1,
                 ARTICLE_INFO A2,
                 SAME_STORY S
   WHERE S.SST_AIN_ID_1 = A1.AIN_ID   AND  S.SST_AIN_ID_2   = A2.AIN_ID AND S.SST_AGENT = 'DOC2VEC-V1-500'
   ORDER BY A1.AIN_DATE DESC;

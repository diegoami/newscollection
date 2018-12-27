 SELECT * FROM PREDICTIONS P1,
              (
          SELECT PRED_AIN_ID_1, PRED_AIN_ID_2 FROM PREDICTIONS GROUP BY PRED_AIN_ID_1, PRED_AIN_ID_2 HAVING COUNT(*) > 1
  ) P2 WHERE P1.PRED_AIN_ID_1 = P2.PRED_AIN_ID_1 and P1.PRED_AIN_ID_2= P2.PRED_AIN_ID_2;


DELETE FROM PREDICTIONS WHERE (PRED_AIN_ID_1, PRED_AIN_ID_2) IN
              (
                (114140, 114427),
                (114278,114453),
                (114344,114419),
                (114346,114427),
                (114347,114410),
                (114364,114426),
                (114376,114419),
                (114415,114420),
                (114417,114447),
                (114432,114436)
);

ALTER TABLE PREDICTIONS ADD UNIQUE (PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_VERSION);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114140, 114427, 0.0213506, 15, null, 0.131725, 114140, 114427);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114278, 114453, 0.727864, 15, null, 0.896244, 114278, 114453);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114344, 114419, 0.960304, 15, null, 0.989606, 114344, 114419);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114346, 114427, 0.565913, 15, null, 0.802565, 114346, 114427);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114347, 114410, 0.00337189, 15, null, 0.00813356, 114347, 114410);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114364, 114426, 0.969837, 15, null, 0.97653, 114364, 114426);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114376, 114419, 0.990544, 15, null, 0.995763, 114376, 114419);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114415, 114420, 0.624761, 15, null, 0.770236, 114415, 114420);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114417, 114447, 0.876213, 15, null, 0.9586, 114417, 114447);
INSERT INTO PREDICTIONS(PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA, PRED_VERSION, PRED_CAT, PRED_REGR, PRED_AIN_ID_1, PRED_AIN_ID_2) VALUES (114432, 114436, 0.969573, 15, null, 0.992327, 114432, 114436);
COMMIT;


 SELECT * FROM SCORES S1,
              (
          SELECT SCO_AIN_ID_1, SCO_AIN_ID_2 FROM SCORES GROUP BY SCO_AIN_ID_1, SCO_AIN_ID_2 HAVING COUNT(*) > 1
  ) S2 WHERE S1.SCO_AIN_ID_1 = S2.SCO_AIN_ID_1 and S1.SCO_AIN_ID_2= S2.SCO_AIN_ID_2;





DELETE FROM SCORES WHERE (SCO_AIN_ID_1, SCO_AIN_ID_2) IN
              (
                (114140, 114427),
                (114278,114453),
                (114344,114419),
                (114346,114427),
                (114347,114410),
                (114364,114426),
                (114376,114419),
                (114415,114420),
                (114417,114447),
                (114432,114436)


  );



ALTER TABLE SCORES ADD UNIQUE (SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_VERSION);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982112, 114140, 114427, 3, 0.43439, 0.397943, 0, 0.634484, 0.671011, 0, 0.529196, 0.462569, 0, 0.582066, 0.557843, 0, 15, 1);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982189, 114278, 114453, 2, 0.680936, 0.601005, 0, 0.836601, 0.876803, 1, 0.601652, 0.68847, 1, 0.751746, 0.784753, 1, 15, 1);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982036, 114344, 114419, 1, 0.488293, 0.748119, 0, 0.86003, 0.918282, 1, 0.60677, 0.842258, 0, 0.749468, 0.853402, 1, 15, 0);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982109, 114346, 114427, 1, 0.531239, 0.662669, 0, 0.668311, 0.854892, 0, 0.500256, 0.70684, 0, 0.533148, 0.760343, 0, 15, 0);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982038, 114347, 114410, 2, 0.0636615, 0.100309, 0, 0.720411, 0.419757, 0, 0.323497, 0.292896, 0, 0.46234, 0.412057, 0, 15, 1);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982107, 114364, 114426, 1, 0.979876, 0.743016, 0, 0.857359, 0.875341, 1, 0.933507, 0.747612, 0, 0.670042, 0.714048, 0, 15, 1);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982018, 114376, 114419, 0, 0.770251, 0.866407, 0, 0.881246, 0.938364, 1, 0.81112, 0.881633, 0, 0.80463, 0.879471, 1, 15, 0);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982027, 114415, 114420, 0, -0.00922512, 0.144701, 0, 0.849491, 0.840423, 1, 0.7245, 0.762108, 0, 0.816186, 0.799934, 0, 15, 0);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982172, 114417, 114447, 1, 0.773409, 0.354999, 0, 0.88868, 0.863991, 0, 0.671088, 0.651843, 0, 0.788784, 0.767016, 0, 15, 1);
INSERT INTO SCORES(SCO_ID, SCO_AIN_ID_1, SCO_AIN_ID_2, SCO_DAYS, SCO_T_TITLE, SCO_D_TITLE, SCO_CW_TITLE, SCO_T_TEXT, SCO_D_TEXT, SCO_CW_TEXT, SCO_T_SUMMARY, SCO_D_SUMMARY, SCO_CW_SUMMARY, SCO_T_SUMMARY_2, SCO_D_SUMMARY_2, SCO_CW_SUMMARY_2, SCO_VERSION, SCO_W_DAYS) VALUES (982141, 114432, 114436, 0, 0.454067, 0.555481, 0, 0.733095, 0.880127, 2, 0.541796, 0.732025, 1, 0.63879, 0.831412, 1, 15, 0);

COMMIT;

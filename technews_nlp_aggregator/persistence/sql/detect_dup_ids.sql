DELIMITER $$
DROP PROCEDURE IF EXISTS  detect_dup_ids $$
CREATE PROCEDURE `detect_dup_ids`()
BEGIN
DECLARE id   INT;
DECLARE exit_loop BOOLEAN;
DECLARE DUP_AIN_ID_CURSOR CURSOR FOR SELECT AIN_ID, AIN_TITLE, MAXA_ID FROM ARTICLE_INFO,
    (select AIN_TITLE AS TITLE, COUNT(*)AS CNT, MIN(AIN_ID) AS MINA_ID, MAX(AIN_ID) AS MAXA_ID from ARTICLE_INFO GROUP BY AIN_TITLE HAVING CNT > 1 ORDER BY CNT DESC ) AIN_DUP
  WHERE TITLE = AIN_TITLE AND AIN_ID != MAXA_ID;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
OPEN DUP_AIN_ID_CURSOR;
  dup_aid_loop: LOOP
       FETCH  DUP_AIN_ID_CURSOR INTO id;
       INSERT INTO TODELETE (TOD_AIN_ID) VALUES(id);
       IF exit_loop THEN
           CLOSE DUP_AIN_ID_CURSOR;
           LEAVE dup_aid_loop;
       END IF;
  END LOOP dup_aid_loop;
END
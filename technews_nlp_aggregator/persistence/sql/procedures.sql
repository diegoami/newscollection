DROP PROCEDURE delete_article;
CREATE PROCEDURE delete_article(IN id INT)
  BEGIN
    DELETE FROM SAME_STORY WHERE (SST_AIN_ID_1 = id OR SST_AIN_ID_2 = id);
    DELETE FROM SAME_STORY_USER WHERE (SSU_AIN_ID_1 = id OR SSU_AIN_ID_2 = id);
    DELETE FROM ARTICLE_AUTHORS WHERE AAU_AIN_ID = id;
    DELETE FROM ARTICLE_TAGS WHERE ATA_AIN_ID = id;
    DELETE FROM ARTICLE_TEXT WHERE ATX_AIN_ID = id;
    DELETE FROM ARTICLE_INFO WHERE AIN_ID = id ;
  COMMIT;
END;

DROP PROCEDURE delete_id;
create procedure delete_ids ()
BEGIN
DECLARE id   INT;
DECLARE exit_loop BOOLEAN;
DECLARE TOD_AIN_CURSOR CURSOR FOR SELECT TOD_AIN_ID FROM TODELETE;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
OPEN TOD_AIN_CURSOR;
  dup_aid_loop: LOOP
       FETCH  TOD_AIN_CURSOR INTO id;
       call delete_article(id);
       IF exit_loop THEN
           CLOSE TOD_AIN_CURSOR;
           LEAVE dup_aid_loop;
       END IF;
  DELETE FROM TODELETE;
  END LOOP dup_aid_loop;
END;


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
END;

DROP PROCEDURE detect_dup_txts;
CREATE PROCEDURE detect_dup_txts()
  BEGIN
DECLARE id   INT;
DECLARE exit_loop BOOLEAN;
DECLARE DUP_ATX_TXT_ID_CURSOR CURSOR FOR SELECT ATX_ID FROM ARTICLE_TEXT,
    (select ATX_AIN_ID AS AAI,  COUNT(*) AS CNT, MAX(ATX_ID) AS MAXA_ID from ARTICLE_TEXT GROUP BY ATX_AIN_ID HAVING CNT > 1 ORDER BY CNT DESC ) AIN_DUP
  WHERE AAI = ATX_AIN_ID AND ATX_ID != MAXA_ID;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
OPEN DUP_ATX_TXT_ID_CURSOR ;
  dup_aid_loop: LOOP
       FETCH  DUP_ATX_TXT_ID_CURSOR INTO id;
       INSERT INTO TODELETE_TXT (TOD_TXT_ID) VALUES(id);
       IF exit_loop THEN
           CLOSE DUP_ATX_TXT_ID_CURSOR;
           LEAVE dup_aid_loop;
       END IF;
  END LOOP dup_aid_loop;
END;

DROP PROCEDURE detect_uninteresting;

create procedure detect_uninteresting ()
BEGIN
DECLARE id   INT;
DECLARE exit_loop BOOLEAN;
DECLARE UNINTERESTING_ATX_TXT_ID_CURSOR CURSOR FOR

  SELECT AIN_ID FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID AND
                                                      (
                                                        AIN_TITLE LIKE '%Vergecast%'
                                                        OR
                                                        AIN_TITLE LIKE '%teaser%'
                                                        OR
                                                          AIN_TITLE LIKE '%trailer%'
                                                        OR
                                                        AIN_TITLE LIKE '%Dealmaster%'
                                                        OR
                                                        ((AIN_TITLE LIKE 'watch %' OR AIN_TITLE LIKE '% watch %') AND
                                                         (AIN_TITLE LIKE '% live %' OR AIN_TITLE LIKE '% keynote %' OR
                                                          AIN_TITLE LIKE '% stream %' OR AIN_TITLE LIKE '% trailer %' OR AIN_TITLE LIKE '% event %' OR AIN_TITLE LIKE '% spot %'  ))
                                                        OR
                                                        AIN_TITLE LIKE '%Poll: %'
                                                          OR
                                                        AIN_TITLE LIKE '%Show Notes: %'
                                                           OR
                                                        AIN_TITLE LIKE 'Video:%'
                                                                        OR
                                                          AIN_URL LIKE 'http://www.techrepublic.com/blog/microsoft-office/%'
                                                        OR
                                                        (AIN_TITLE LIKE '%Best Buy%' AND AIN_URL LIKE 'https://www.theverge.com/%')
                                                        OR
                                                        (AIN_URL LIKE 'https://thenextweb.com/offers/%')
                                                          OR
                                                        (AIN_URL LIKE 'https://www.theverge.com/circuitbreaker/%')

                                                      ;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
OPEN UNINTERESTING_ATX_TXT_ID_CURSOR ;
  uninteresting_text_loop: LOOP
       FETCH  UNINTERESTING_ATX_TXT_ID_CURSOR   INTO id;
       INSERT INTO TODELETE (TOD_AIN_ID) VALUES(id);
       IF exit_loop THEN
           CLOSE UNINTERESTING_ATX_TXT_ID_CURSOR ;
           LEAVE uninteresting_text_loop;
       END IF;
  END LOOP uninteresting_text_loop;
END;

CREATE PROCEDURE detect_short_txts()
  BEGIN
DECLARE id   INT;
DECLARE exit_loop BOOLEAN;
DECLARE SHORT_ATX_TXT_ID_CURSOR CURSOR FOR SELECT AIN_ID FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID AND (LENGTH(ATX_TEXT) < 600 OR LENGTH(AIN_TITLE) < 10);
DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
OPEN SHORT_ATX_TXT_ID_CURSOR ;
  short_text_loop: LOOP
       FETCH  SHORT_ATX_TXT_ID_CURSOR INTO id;
       INSERT INTO TODELETE (TOD_AIN_ID) VALUES(id);
       IF exit_loop THEN
           CLOSE SHORT_ATX_TXT_ID_CURSOR;
           LEAVE short_text_loop;
       END IF;
  END LOOP short_text_loop;
END;




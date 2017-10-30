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

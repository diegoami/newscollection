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

                                                      )
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
COMMIT;



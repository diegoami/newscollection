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
  END LOOP dup_aid_loop;
END;


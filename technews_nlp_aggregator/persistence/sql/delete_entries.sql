DELETE FROM ARTICLE_AUTHORS WHERE AAU_AIN_ID IN (29065, 29066 );
DELETE FROM ARTICLE_TAGS WHERE ATA_AIN_ID IN (29065, 29066 );
DELETE FROM ARTICLE_TEXT WHERE ATX_AIN_ID IN (29065, 29066 );
DELETE FROM ARTICLE_INFO WHERE AIN_ID IN (29065, 29066 );
COMMIT;


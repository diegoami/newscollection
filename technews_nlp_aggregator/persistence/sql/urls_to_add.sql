create table URLS_TO_ADD
(
	UTA_ID int auto_increment
		primary key,
	UTA_SPIDER varchar(32) null,
	UTA_URL varchar(256) null,
	UTA_PROCESSED datetime null,
	constraint URLS_TO_ADD_UTA_ID_uindex
		unique (UTA_ID)
)
;


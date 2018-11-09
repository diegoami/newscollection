create table ARTICLE_AUTHORS
(
	AAU_ID int auto_increment
		primary key,
	AAU_AIN_ID int not null,
	AAU_AUT_ID int not null,
	constraint ARTICLE_AUTHORS_AAU_ID_uindex
		unique (AAU_ID)
)
;

create index ARTICLE_AUTHORS_ARTICLE_INFO_AIN_ID_fk
	on ARTICLE_AUTHORS (AAU_AIN_ID)
;

create index ARTICLE_AUTHORS_AUTHORS_AUT_ID_fk
	on ARTICLE_AUTHORS (AAU_AUT_ID)
;

create table ARTICLE_INFO
(
	AIN_ID int auto_increment
		primary key,
	AIN_URL varchar(256) not null,
	AIN_DATE date null,
	AIN_TITLE varchar(256) not null,
	AIN_FILENAME varchar(256) null,
	AIN_PROCESSED datetime null,
	AIN_SAVED datetime null,
	constraint ARTICLE_INFO_AIN_ID_uindex
		unique (AIN_ID),
	constraint ARTICLE_INFO_AIN_URL_uindex
		unique (AIN_URL)
)
;


alter table ARTICLE_AUTHORS
	add constraint ARTICLE_AUTHORS_ARTICLE_INFO_AIN_ID_fk
		foreign key (AAU_AIN_ID) references ARTICLE_INFO (AIN_ID)
;

create table ARTICLE_TAGS
(
	ATA_ID int auto_increment
		primary key,
	ATA_AIN_ID int not null,
	ATA_TAG_ID int not null,
	constraint ARTICLE_TAGS_ATA_ID_uindex
		unique (ATA_ID),
	constraint ARTICLE_TAGS_ARTICLE_INFO_AIN_ID_fk
		foreign key (ATA_AIN_ID) references ARTICLE_INFO (AIN_ID)
)
;

create index ARTICLE_TAGS_ARTICLE_INFO_AIN_ID_fk
	on ARTICLE_TAGS (ATA_AIN_ID)
;

create index ARTICLE_TAGS_TAGS_TAG_ID_fk
	on ARTICLE_TAGS (ATA_TAG_ID)
;

create table ARTICLE_TEXT
(
	ATX_ID int auto_increment
		primary key,
	ATX_AIN_ID int not null,
	ATX_TEXT text null,
	ATX_TEXT_ORIG text null,
	ATX_MODIFIED tinyint(1) null,

	constraint ARTICLE_TEXT_ATX_ID_uindex
		unique (ATX_ID),
	constraint ARTICLE_TEXT_ARTICLE_INFO_AIN_ID_fk
		foreign key (ATX_AIN_ID) references ARTICLE_INFO (AIN_ID)
)
;

create index ARTICLE_TEXT_ARTICLE_INFO_AIN_ID_fk
	on ARTICLE_TEXT (ATX_AIN_ID)
;

create table AUTHORS
(
	AUT_ID int auto_increment
		primary key,
	AUT_NAME varchar(64) not null,
	AUT_URL varchar(128) null,
	constraint AUTHORS_AUT_ID_uindex
		unique (AUT_ID)
)
;

alter table ARTICLE_AUTHORS
	add constraint ARTICLE_AUTHORS_AUTHORS_AUT_ID_fk
		foreign key (AAU_AUT_ID) references AUTHORS (AUT_ID)
;

create table TAGS
(
	TAG_ID int auto_increment
		primary key,
	TAG_NAME varchar(64) not null,
	TAG_URL varchar(128) null,
	constraint TAGS_TAG_ID_uindex
		unique (TAG_ID)
)
;

alter table ARTICLE_TAGS
	add constraint ARTICLE_TAGS_TAGS_TAG_ID_fk
		foreign key (ATA_TAG_ID) references TAGS (TAG_ID)
;


create table TODELETE
(
	TOD_AIN_ID int not null
)
;
create table TODELETE_TXT
(
	TOD_TXT_ID int null
)
;



ALTER TABLE AUTHORS CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_AUTHORS CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_TAGS CONVERT TO CHARACTER SET utf8;
ALTER TABLE TAGS CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_TEXT CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_INFO CONVERT TO CHARACTER SET utf8;


create table SAME_STORY
(
	SST_ID int auto_increment
		primary key,
	SST_AIN_ID_1 int not null,
	SST_AIN_ID_2 int not null,
	SST_AGENT varchar(32) null,
	SST_SIMILARITY float null,
	SST_UPDATED timestamp null,
	constraint SAME_STORY_SST_ID_uindex
		unique (SST_ID),
	constraint SAME_STORY_ARTICLE_INFO_AIN_ID_1_fk
		foreign key (SST_AIN_ID_1) references ARTICLE_INFO (AIN_ID),
	constraint SAME_STORY_ARTICLE_INFO_AIN_ID_2_fk
		foreign key (SST_AIN_ID_2) references ARTICLE_INFO (AIN_ID)
)
;

create index SAME_STORY_ARTICLE_INFO_AIN_ID_1_fk
	on SAME_STORY (SST_AIN_ID_1)
;

create index SAME_STORY_ARTICLE_INFO_AIN_ID_2_fk
	on SAME_STORY (SST_AIN_ID_2)
;


create table SAME_STORY_USER
(
	SSU_ID int auto_increment
		primary key,
	SSU_AIN_ID_1 int not null,
	SSU_AIN_ID_2 int not null,
	SSU_SIMILARITY float null,
	SSU_UPDATED timestamp null,
	SSU_ORIGIN varchar(32) null,
	constraint SAME_STORY_USER_SSU_ID_uindex
		unique (SSU_ID),
	constraint SAME_STORY_USER_ARTICLE_INFO_AIN_ID_1_fk
		foreign key (SSU_AIN_ID_1) references ARTICLE_INFO (AIN_ID),
	constraint SAME_STORY_USER_ARTICLE_INFO_AIN_ID_2_fk
		foreign key (SSU_AIN_ID_2) references ARTICLE_INFO (AIN_ID)
)
;

create index SAME_STORY_USER_ARTICLE_INFO_AIN_ID_1_fk
	on SAME_STORY_USER (SSU_AIN_ID_1)
;

create index SAME_STORY_USER_ARTICLE_INFO_AIN_ID_2_fk
	on SAME_STORY_USER (SSU_AIN_ID_2)
;

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

create table SCORES
(
	SCO_ID int auto_increment
		primary key,
	SCO_AIN_ID_1 int not null,
	SCO_AIN_ID_2 int not null,
	SCO_DAYS int null,
	SCO_T_TITLE float null,
	SCO_D_TITLE float null,
	SCO_CW_TITLE float null,
	SCO_T_TEXT float null,
	SCO_D_TEXT float null,
	SCO_CW_TEXT float null,
	SCO_T_SUMMARY float null,
	SCO_D_SUMMARY float null,
	SCO_CW_SUMMARY float null,
	SCO_T_SUMMARY_2 float null,
	SCO_D_SUMMARY_2 float null,
	SCO_CW_SUMMARY_2 float null,
	constraint SCORES_SCO_ID_uindex
		unique (SCO_ID)

);


ALTER TABLE SCORES
			ADD CONSTRAINT SCORES_ARTICLE_INFO_AIN_ID_2_fk
			FOREIGN KEY (SCO_AIN_ID_2) REFERENCES ARTICLE_INFO (AIN_ID);

ALTER TABLE SCORES DROP FOREIGN KEY SCORES_ARTICLE_INFO_AIN_ID_fk;

ALTER TABLE SCORES
			ADD CONSTRAINT SCORES_ARTICLE_INFO_AIN_ID_1_fk
			FOREIGN KEY (SCO_AIN_ID_1) REFERENCES ARTICLE_INFO (AIN_ID);



CREATE TABLE `TRAINING_MODEL` (
  `TMO_ID` int(11) NOT NULL AUTO_INCREMENT,
  `TMO_DATE` datetime DEFAULT NULL,
  `TMO_TRAINING_SET` int(11) DEFAULT NULL,
  `TMO_F1` float DEFAULT NULL,
  `TMO_PRECISION` float DEFAULT NULL,
  `TMO_RECALL` float DEFAULT NULL,
  `TMO_ACCURACY` float DEFAULT NULL,
  `TMO_LOG_LOSS` float DEFAULT NULL,
  `TMO_NMSE` float DEFAULT NULL,
  PRIMARY KEY (`TMO_ID`)
) ;





COMMIT;

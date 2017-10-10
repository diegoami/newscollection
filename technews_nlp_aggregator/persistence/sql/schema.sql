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


ALTER TABLE AUTHORS CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_AUTHORS CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_TAGS CONVERT TO CHARACTER SET utf8;
ALTER TABLE TAGS CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_TEXT CONVERT TO CHARACTER SET utf8;
ALTER TABLE ARTICLE_INFO CONVERT TO CHARACTER SET utf8;
COMMIT;

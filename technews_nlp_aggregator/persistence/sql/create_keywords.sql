create table ARTICLE_KEYWORDS
(
	AKE_ID int auto_increment
		primary key,
	AKE_AIN_ID int null,
	KEYWORDS varchar(256) null,
	constraint ARTICLE_KEYWORDS_AKE_ID_uindex
		unique (AKE_ID),
	constraint ARTICLE_KEYWORDS_ARTICLE_INFO_AIN_ID_fk
		foreign key (AKE_AIN_ID) references ARTICLE_INFO (AIN_ID)
)
;

create index ARTICLE_KEYWORDS_ARTICLE_INFO_AIN_ID_fk
	on ARTICLE_KEYWORDS (AKE_AIN_ID)
;


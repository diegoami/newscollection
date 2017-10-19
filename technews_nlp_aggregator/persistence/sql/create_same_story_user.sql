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


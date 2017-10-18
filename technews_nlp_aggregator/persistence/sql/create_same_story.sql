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


create table SAME_STORY_JOBS
(
	SSJ_ID int auto_increment
		primary key,
	SSJ_START date null,
	SSJ_END date null,
	SSJ_AGENT varchar(32) null,
	SSJ_EXEC_DATE timestamp default CURRENT_TIMESTAMP not null,
	SSJ_THRESHOLD_LO float null,
	SSJ_THRESHOLD_HI float null,
	constraint SAME_STORY_JOBS_SSJ_ID_uindex
		unique (SSJ_ID)
)
;


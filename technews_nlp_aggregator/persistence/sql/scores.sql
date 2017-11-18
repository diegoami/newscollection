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
		unique (SCO_ID),
	constraint SCORES_ARTICLE_INFO_AIN_ID_fk
		foreign key (SCO_AIN_ID_1) references ARTICLE_INFO (AIN_ID),
  constraint SCORES_ARTICLE_INFO_AIN_ID_2_fk
		foreign key (SCO_AIN_ID_2) references ARTICLE_INFO (AIN_ID)

);



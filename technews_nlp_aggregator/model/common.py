import numpy as np


RELEVANT_COLUMNS = ['SCO_DAYS', 'SCO_W_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]

def retrieve_X_y_clf(train_df, threshold=0.65):
    result_columns = 'SCO_USER'
    X_train = np.array(train_df[RELEVANT_COLUMNS])
    y_train = np.array(train_df[result_columns].map(lambda x: 1 if x > threshold else 0))
    return X_train, y_train

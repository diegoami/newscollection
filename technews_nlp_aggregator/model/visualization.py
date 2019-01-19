import os

import matplotlib.pyplot as plt
from .common import retrieve_X_y_clf
from sklearn.model_selection import cross_val_score, cross_val_predict

from sklearn.metrics import precision_recall_curve, roc_curve

PROJECT_ROOT_DIR = '.'


def save_fig(fig_id, tight_layout=True):
    path = os.path.join(PROJECT_ROOT_DIR, "images", fig_id + ".png")
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds, model_name):
    plt.figure(figsize=(8, 6))
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
    plt.xlabel("Threshold", fontsize=16)
    plt.legend(loc="upper left", fontsize=16)
    plt.ylim([0, 1])
    save_fig("{} precision_vs_recall_plot".format(model_name))
    plt.clf()

def plot_roc_curve(fpr, tpr, model_name=None):
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, linewidth=2, label=model_name)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)
    save_fig("{} roc_curve_plot".format(model_name))
    plt.clf()


def plot_precision_vs_recall(precisions, recalls, model_name):
    plt.figure(figsize=(8, 4))
    plt.plot(recalls, precisions, "b-", linewidth=2)
    plt.xlabel("Recall", fontsize=16)
    plt.ylabel("Precision", fontsize=16)
    plt.axis([0, 1, 0, 1])
    save_fig("{} precision_recall_vs_threshold_plot".format(model_name))
    plt.clf()


def map_threshold(train_df, clf):

    X_train, y_train = retrieve_X_y_clf(train_df)
    y_scores = cross_val_predict(clf, X_train, y_train, cv=5, method="predict_proba")

    precisions, recalls, thresholds = precision_recall_curve(y_train, y_scores[:,1])
    fpr, tpr, thresholds_r = roc_curve(y_train, y_scores[:, 1])
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds )
    plot_precision_vs_recall(precisions, recalls)
    plot_roc_curve(fpr, tpr)
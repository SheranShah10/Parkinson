import numpy as np

def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)

def f1_score_macro(y_true, y_pred):
    classes = np.unique(y_true)
    f1s = []
    for c in classes:
        tp = np.sum((y_pred == c) & (y_true == c))
        fp = np.sum((y_pred == c) & (y_true != c))
        fn = np.sum((y_pred != c) & (y_true == c))
        if (tp+fp) == 0 and (tp+fn) == 0: continue
        prec = tp / (tp + fp) if (tp+fp)>0 else 0
        rec = tp / (tp + fn) if (tp+fn)>0 else 0
        f1 = 2 * (prec * rec) / (prec + rec) if (prec+rec)>0 else 0
        f1s.append(f1)
    return np.mean(f1s) if f1s else 0.0

def rmse_score(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def mae_score(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

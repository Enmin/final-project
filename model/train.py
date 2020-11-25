import sys
sys.path.append("..")
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, make_scorer
import numpy as np
from math import sqrt
from model.prepare_data import generate_data


def MLpipe_KFold_RMSE(X,y, preprocessor, ML_algo, param_grid):
    test_scores = []
    best_models = []
    std_ftrs = X.columns
    # loop through 10 random states (2 points)
    rmse = lambda x, y: sqrt(mean_squared_error(x, y))
    for i in range(10):
        # split data to other/test 80/20, and the use KFold with 4 folds (2 points)
        random_state = 42 * i
        X_other, X_test, y_other, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
        kf = KFold(n_splits=4, shuffle=True, random_state=random_state)
        # preprocess the data (1 point)
        pipe = make_pipeline(preprocessor, ML_algo)

        # loop through the hyperparameter combinations or use GridSearchCV (2 points)
        grid = GridSearchCV(estimator=pipe, param_grid=param_grid, scoring=make_scorer(rmse, greater_is_better=False),
                            cv=kf, return_train_score=True)

        # for each combination, calculate the train and validation scores using the evaluation metric
        grid.fit(X_other, y_other)

        # find which hyperparameter combination gives the best validation score (1 point)
        test_score = grid.score(X_test, y_test)

        # calculate the test score (1 point)
        test_scores.append(test_score)
        best_models.append(grid.best_params_)
        # append the test score and the best model to the lists (1 point)
    return best_models, test_scores


def xgboost_train(data):
    pass


if __name__ == '__main__':
    dataset = generate_data()
    y = dataset['target']
    X = dataset.loc[:, dataset.columns!= 'target']
    preprocessor = StandardScaler()  # if you had a more complex dataset, you'd have a ColumnTransformer here
    algos = {
        "l1": Lasso(),
        "l2": Ridge(),
        "Elastic Net": ElasticNet(),
        "RF": RandomForestRegressor(),
        "SVR": SVR(),
        "KNN": KNeighborsRegressor()
    }
    params = {
        "l1": {'lasso__alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2]},
        "l2": {'ridge__alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2]},
        "Elastic Net": {'elasticnet__alpha': [1e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2],
                        'elasticnet__l1_ratio': np.linspace(1e-1, 1, 10)},
        "RF": {'randomforestregressor__max_depth': [5, 10, 30, 50],
               'randomforestregressor__max_features': [0.5, 0.75, 1.0]},
        "SVR": {'svr__gamma': [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2], "svr__C": [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2]},
        "KNN": {'kneighborsregressor__n_neighbors': [1, 10, 30, 80],
                'kneighborsregressor__weights': ['uniform', 'distance']},
    }
    models_dict = {}
    scores_dict = {}
    for algo in algos:
        models, scores = MLpipe_KFold_RMSE(X, y, preprocessor, algos[algo], params[algo])
        models_dict[algo] = models
        scores_dict[algo] = (np.mean(scores), np.std(scores))
    rank_by_mean = list((k, v) for k, v in sorted(scores_dict.items(), key=lambda item: item[1][0], reverse=False))
    rank_by_std = list((k, v) for k, v in sorted(scores_dict.items(), key=lambda item: item[1][1], reverse=False))
    print("-----------------rank mean--------------------")
    for i in rank_by_mean:
        print(i[0], ": ", i[1][0], "Parameters: ", models_dict[i[0]][0])
    print("-----------------rank std--------------------")
    for i in rank_by_std:
        print(i[0], ": ", i[1][1], "Parameters: ", models_dict[i[0]][0])
print(__doc__)

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation, metrics
from sklearn.datasets import make_hastie_10_2
from sklearn.grid_search import GridSearchCV

# import matplotlib.pylab as plt
# %matplotlib inline
# from matplotlib.pylab import rcParams
# rcParams['figure.figsize'] = 12, 4

# define x_train/test and y_train/test
x_train, y_train = make_hastie_10_2(n_samples=10000)

health_score = GradientBoostingRegressor(
    loss='ls', #using least squares loss function
    learning_rate=0.1, #the lower the better -> makes for robust analysis of each specific characteristic, TUNE**
    n_estimators=100,
    subsample=0.8, #TUNE**
    min_samples_split=20, #min num of samples for node to split, should be ~0.5-1% of total data, TUNE**
    min_samples_leaf=3, #min samples in a leaf, TUNE**
    max_depth=5, #mix between low max depth(underfitting) and high max depth(overfitting), TUNE**
    # random_state=0,
    max_features='sqrt' #num of features to consider for best split, TUNE**
)
health_score.fit(x_train, y_train)
# mean_squared_error(y_test, health_score.predict(x_test))

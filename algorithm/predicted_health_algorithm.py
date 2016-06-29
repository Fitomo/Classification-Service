import sys
import random
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

###############################################################################
# import files
train_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)

###############################################################################
# tag line items
train['type'] = 'train'
test['type'] = 'test'

###############################################################################
# combine data
all_data = pd.concat([train,test], axis=0)
all_data.columns
all_data.head(10)
all_data.describe()

###############################################################################
# identify types of variables
ID_cols = ['user_id']
target_cols = ['health_score_in_week']
cat_cols = ['date']
num_cols = ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
other_cols = list(set(list(all_data.columns))-set(ID_cols)-set(target_cols)-set(cat_cols)-set(num_cols))

###############################################################################
# fill out missing values
# remove rows that have 0 in the any of the num_cols
num_cat_cols = num_cols + cat_cols + target_cols
for cat in num_cat_cols:
    if all_data[cat].isnull().any()==True:
        all_data[cat+'_NA']=all_data[cat].isnull()*1
all_data[num_cols] = all_data[num_cols].fillna(all_data[num_cols].mean(), inplace=True)
all_data[cat_cols] = all_data[cat_cols].fillna(value=-9999)
all_data[target_cols] = all_data[target_cols].fillna(value=0)

###############################################################################
# further categorize/split data up
train = all_data[(all_data['type']=='train') & (all_data['outlier_tag']==0) & (all_data['health_score_in_week']!=0)]
test = all_data[(all_data['type']=='test') & (all_data['outlier_tag']==0) & (all_data['health_score_in_week']!=0)]

###############################################################################
# setup train and validate variables
features = ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
x_train = train[list(features)].values
y_train = train['health_score_in_week'].values
x_test = test[list(features)].values

###############################################################################
# create function to run model with specified params and cv_folds
def gbm_fit(params, cv_folds):
    gbm = GradientBoostingRegressor(**params)
    gbm.fit(x_train, y_train)

    # check accuracy of model
    # no need for validation data because of cross validation
    # training data is split up into cv_folds folds - model trained on cv_folds - 1 of the folds - last fold is validation set
    # cv_scores_me = cross_validation.cross_val_score(gbm, x_train, y_train, cv=cv_folds, scoring='mean_absolute_error')
    cv_scores_mse = cross_validation.cross_val_score(gbm, x_train, y_train, cv=cv_folds, scoring='mean_squared_error')
    print '\nModel Report'
    print ('Mean Squared Error Accuracy: %0.4g (+/- %0.4g)' % (cv_scores_mse.mean(), cv_scores_mse.std()*2))
    print ('CV Score: Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g' % (np.mean(cv_scores_mse), np.std(cv_scores_mse), np.min(cv_scores_mse), np.max(cv_scores_mse)))
    feat_imp = pd.Series(gbm.feature_importances_, features).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.show()

    # check actual performance on test data
    final_predictions = gbm.predict(x_test)
    test['health_score_in_week'] = final_predictions
    test.to_csv(output_file, columns=['user_id', 'date', 'steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score', 'health_score_in_week'])

# test various parameters
params_original = {
'min_samples_split': 500,
'min_samples_leaf': 50,
'max_depth': 8,
'max_features': 'sqrt',
'subsample': 0.8,
'learning_rate': 0.1,
'n_estimators': 500,
'random_state': 10,
'loss': 'ls'
}
# gbm_fit(params_original, 5)

###############################################################################
# tune parameters
param_test1 = { 'n_estimators':range(20,121,10) }
grid_search1 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,min_samples_split=500,min_samples_leaf=50,max_depth=8,max_features='sqrt',subsample=0.8,random_state=10),
    param_grid=param_test1,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=2
)
grid_search1.fit(x_train, y_train)
grid_search1.grid_scores_, grid_search1.best_params_, grid_search1.best_score_
# [ mean: -144.50046, std: 1.56585, params: {'n_estimators': 20}, mean: -137.16978, std: 1.26331, params: {'n_estimators': 30},
#   mean: -134.14077, std: 1.12795, params: {'n_estimators': 40}, mean: -132.88186, std: 1.03599, params: {'n_estimators': 50},
#   mean: -132.36311, std: 0.97073, params: {'n_estimators': 60}, mean: -132.14041, std: 0.91713, params: {'n_estimators': 70},
#   mean: -132.05814, std: 0.89192, params: {'n_estimators': 80}, mean: -132.01237, std: 0.87023, params: {'n_estimators': 90},
#   mean: -132.00162, std: 0.85715, params: {'n_estimators': 100}, mean: -132.00080, std: 0.84445, params: {'n_estimators': 110},
#   mean: -132.00731, std: 0.84576, params: {'n_estimators': 120} ]
# {'n_estimators': 110}
# -132.000795686

# tune max_depth and min_samples_split because they're higher impact
param_test2 = { 'max_depth':range(5,16,2), 'min_samples_split':range(200,1001,200) }
grid_search1 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,n_estimators=110,min_samples_leaf=50,max_features='sqrt',subsample=0.8,random_state=10),
    param_grid=param_test2,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=3
)
grid_search1.fit(x_train, y_train)
grid_search1.grid_scores_, grid_search1.best_params_, grid_search1.best_score_

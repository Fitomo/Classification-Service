import sys
import random
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
import matplotlib.pyplot as plt

###############################################################################
# Import files
# When calling the function from terminal, call:
# python predicted_health_algorithm.py train_file test_file output_file
train_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)

###############################################################################
# Tag line items as either training or testing items
train['type'] = 'train'
test['type'] = 'test'

###############################################################################
# Combine data
all_data = pd.concat([train,test], axis=0)
all_data.columns
all_data.head(10)
all_data.describe()

###############################################################################
# Identify types of variables
ID_cols = ['user_id']
target_cols = ['health_score_in_week']
cat_cols = ['date']
num_cols = ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
other_cols = list(set(list(all_data.columns))-set(ID_cols)-set(target_cols)-set(cat_cols)-set(num_cols))

###############################################################################
# Fill out missing values
num_cat_cols = num_cols + cat_cols + target_cols
for cat in num_cat_cols:
    if all_data[cat].isnull().any()==True:
        all_data[cat+'_NA']=all_data[cat].isnull()*1
all_data[num_cols] = all_data[num_cols].fillna(all_data[num_cols].mean(), inplace=True)
all_data[cat_cols] = all_data[cat_cols].fillna(value=-9999)

# Remove rows that have 0 in the any of the num_cols
all_data[target_cols] = all_data[target_cols].fillna(value=0)

###############################################################################
# Filter out data
train = all_data[(all_data['type']=='train') & (all_data['outlier_tag']==0) & (all_data['health_score_in_week']!=0)]
test = all_data[(all_data['type']=='test') & (all_data['outlier_tag']==0) & (all_data['health_score_in_week']!=0)]

###############################################################################
# Setup train and test variables
features = ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
x_train = train[list(features)].values
y_train = train['health_score_in_week'].values
x_test = test[list(features)].values

###############################################################################
# Create function to run model with specified parameters and cv_folds
def gbm_fit(params, cv_folds):
    gbm = GradientBoostingRegressor(**params)
    gbm.fit(x_train, y_train)

    # Check accuracy of model
    # No need for validation data because of cross validation
    # Training data is split up into cv_folds folds:
    # Model trained on (cv_folds - 1) of the folds; last fold is saved as validation set
    cv_scores_mse = cross_validation.cross_val_score(gbm, x_train, y_train, cv=cv_folds, scoring='mean_squared_error')
    print '\nModel Report'
    print ('MSE Score: Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g' %
          (np.mean(cv_scores_mse), np.std(cv_scores_mse), np.min(cv_scores_mse), np.max(cv_scores_mse)))
    feat_imp = pd.Series(gbm.feature_importances_, features).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.show()

    # Check actual performance on test data
    final_predictions = gbm.predict(x_test)
    test['health_score_in_week'] = final_predictions
    test.to_csv(output_file, columns=['user_id', 'date', 'steps', 'total_sleep', 'resting_hr',
                                      'step_week_slope', 'sleep_week_slope', 'hr_week_slope',
                                      'curr_health_score', 'health_score_in_week'])

    # Save the model to file 'health_prediction.pkl'
    joblib.dump(gbm, 'health_prediction.pkl', compress=1)

# Original parameters
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

# Final parameters after tuning
params_tuned = {
    'min_samples_split': 2000,
    'min_samples_leaf': 30,
    'max_depth': 7,
    'max_features': 2,
    'subsample': 0.8,
    'learning_rate': 0.005,
    'n_estimators': 1500,
    'random_state': 10,
    'loss': 'ls'
}
#################### UNCOMMENT LINE BELOW TO RUN ALGORITHM ####################
# gbm_fit(params_tuned, 5)

###############################################################################
# Tune n_estimators
param_test1 = { 'n_estimators':range(20,81,10) }
grid_search1 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,min_samples_split=500,min_samples_leaf=50,
                                        max_depth=8,max_features='sqrt',subsample=0.8,random_state=10),
    param_grid=param_test1,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=3
)
# grid_search1.fit(x_train, y_train)
# print grid_search1.grid_scores_, grid_search1.best_params_, grid_search1.best_score_

# Tune max_depth and min_samples_split because they're higher impact
param_test2 = { 'max_depth':range(5,16,2), 'min_samples_split':range(1600,2400,200) }
grid_search2 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,n_estimators=110,min_samples_leaf=50,
                                        max_features='sqrt',subsample=0.8,random_state=10),
    param_grid=param_test2,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=3
)
# grid_search2.fit(x_train, y_train)
# print grid_search2.grid_scores_, grid_search2.best_params_, grid_search2.best_score_

# Tune min_samples_leaf
param_test3 = { 'min_samples_leaf':range(20,61,10) }
grid_search3 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,n_estimators=110,min_samples_split=2000,
                                        max_depth=7,max_features='sqrt',subsample=0.8,random_state=10),
    param_grid=param_test3,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=3
)
# grid_search3.fit(x_train, y_train)
# print grid_search3.grid_scores_, grid_search3.best_params_, grid_search3.best_score_

# Tune max_features
param_test4 = { 'max_features':range(1,6,1) }
grid_search4 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,n_estimators=110,min_samples_split=2000,
                                        max_depth=7,min_samples_leaf=30,subsample=0.8,random_state=10),
    param_grid=param_test4,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=3
)
# grid_search4.fit(x_train, y_train)
# print grid_search4.grid_scores_, grid_search4.best_params_, grid_search4.best_score_

# Tune subsample
param_test5 = { 'subsample':[0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9] }
grid_search5 = GridSearchCV(
    estimator=GradientBoostingRegressor(learning_rate=0.05,n_estimators=110,min_samples_split=2000,
                                        max_depth=7,min_samples_leaf=30,max_features=2,random_state=10),
    param_grid=param_test5,
    scoring='mean_squared_error',
    n_jobs=4,
    iid=False,
    cv=3
)
# grid_search5.fit(x_train, y_train)
# print grid_search5.grid_scores_, grid_search5.best_params_, grid_search5.best_score_

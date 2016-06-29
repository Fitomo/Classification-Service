import sys
from decimal import Decimal
import math
import random
import numpy as np
import pandas as pd
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

# import matplotlib.pylab as plt
# %matplotlib inline
# from matplotlib.pylab import rcParams
# rcParams['figure.figsize'] = 12, 4

# import files
train_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]
train = pd.read_csv(train_file)
test = pd.read_csv(test_file)


# tag line items
train['type'] = 'train'
test['type'] = 'test'


# combine data
all_data = pd.concat([train,test], axis=0)
all_data.columns
all_data.head(10)
all_data.describe()


# identify types of variables
ID_cols = ['user_id']
target_cols = ['health_score_in_week']
cat_cols = ['date']
num_cols = ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
other_cols = list(set(list(all_data.columns))-set(ID_cols)-set(target_cols)-set(cat_cols)-set(num_cols))
# ['type', 'outlier_tag']

# fill out missing values
# remove rows that have 0 in the any of the num_cols
num_cat_cols = num_cols + cat_cols + target_cols
for cat in num_cat_cols:
    if all_data[cat].isnull().any()==True:
        all_data[cat+'_NA']=all_data[cat].isnull()*1
all_data[num_cols] = all_data[num_cols].fillna(all_data[num_cols].mean(), inplace=True)
all_data[cat_cols] = all_data[cat_cols].fillna(value=-9999)
all_data[target_cols] = all_data[target_cols].fillna(value=0)


# convert categorical data so it can be used in the algorithm
for cat in cat_cols:
    number = LabelEncoder()
    all_data[cat] = number.fit_transform(all_data[cat].astype('str'))


# further categorize/split data up
train = all_data[(all_data['type']=='train') & (all_data['outlier_tag']==0) & (all_data['health_score_in_week']!=0)]
test = all_data[(all_data['type']=='test') & (all_data['outlier_tag']==0) & (all_data['health_score_in_week']!=0)]

train['is_train'] = np.random.uniform(0, 1, len(train)) <= 0.75
train, validate = train[train['is_train']==True], train[train['is_train']==False]


# setup train and validate variables
features = ['steps', 'total_sleep', 'resting_hr', 'step_week_slope', 'sleep_week_slope', 'hr_week_slope', 'curr_health_score']
x_train = train[list(features)].values
y_train = train['health_score_in_week'].values
x_validate = validate[list(features)].values
y_validate = validate['health_score_in_week'].values
x_test = test[list(features)].values


# run model
random.seed(100)
gbm = GradientBoostingRegressor(
    loss='ls', # using least squares loss function
    learning_rate=0.1, # the lower the better -> makes for robust analysis of each specific characteristic, TUNE**
    n_estimators=100,
    subsample=0.8, # TUNE**
    min_samples_split=20, # min num of samples for node to split, should be ~0.5-1% of total data, TUNE**
    min_samples_leaf=3, # min samples in a leaf, TUNE**
    max_depth=5, # mix between low max depth(underfitting) and high max depth(overfitting), TUNE**
    # random_state=0,
    max_features='sqrt' # num of features to consider for best split, TUNE**
)
gbm.fit(x_train, y_train)
mse = mean_squared_error(y_validate, gbm.predict(x_validate))
print ('MSE: %.4f' % mse)


# check performance
status = gbm.predict(x_validate)
print status

final_status = gbm.predict(x_test)
print final_status
test['health_score_in_week'] = final_status
test.to_csv(output_file, columns=['user_id', 'health_score_in_week'])

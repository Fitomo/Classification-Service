# Parameter Tuning
## Test 1:
### Params:
- learning_rate=0.05
- min_samples_split=500
- min_samples_leaf=50
- max_depth=8
- max_features='sqrt'
- subsample=0.8
- random_state=10
### Testing:
n_estimators:range(20,81,10)
### Grid Scores:
[ mean: 144.50046, std: 1.56585, params: {'n_estimators': 20},
  mean: 137.16978, std: 1.26331, params: {'n_estimators': 30},
  mean: 134.14077, std: 1.12795, params: {'n_estimators': 40},
  mean: 132.88186, std: 1.03599, params: {'n_estimators': 50},
  mean: 132.36311, std: 0.97073, params: {'n_estimators': 60},
  mean: 132.14041, std: 0.91713, params: {'n_estimators': 70},
  mean: 132.05814, std: 0.89192, params: {'n_estimators': 80},
  mean: 132.01237, std: 0.87023, params: {'n_estimators': 90},
  mean: 132.00162, std: 0.85715, params: {'n_estimators': 100},
  mean: 132.00080, std: 0.84445, params: {'n_estimators': 110},
  mean: 132.00731, std: 0.84576, params: {'n_estimators': 120} ]
### Best Params:
{'n_estimators': 110}
### Best Score:
132.000795686

## Test 2:
### Params:
- learning_rate=0.05
- n_estimators=110
- min_samples_leaf=50
- max_features='sqrt'
- subsample=0.8
- random_state=10
### Testing:
max_depth:range(5,15,2)
min_samples_split:range(1600,2400,200)
### Grid Scores:
[ mean: 132.02205, std: 0.90746, params: {'min_samples_split': 1600, 'max_depth': 5},
  mean: 132.00114, std: 0.86938, params: {'min_samples_split': 1800, 'max_depth': 5},
  mean: 132.02837, std: 0.92583, params: {'min_samples_split': 2000, 'max_depth': 5},
  mean: 132.02668, std: 0.91052, params: {'min_samples_split': 2200, 'max_depth': 5},
  mean: 131.87399, std: 0.92580, params: {'min_samples_split': 1600, 'max_depth': 7},
  mean: 131.84520, std: 0.90404, params: {'min_samples_split': 1800, 'max_depth': 7},
  mean: 131.79836, std: 0.92241, params: {'min_samples_split': 2000, 'max_depth': 7},
  mean: 131.89466, std: 0.87572, params: {'min_samples_split': 2200, 'max_depth': 7},
  mean: 131.92016, std: 0.90009, params: {'min_samples_split': 1600, 'max_depth': 9},
  mean: 131.89327, std: 0.88209, params: {'min_samples_split': 1800, 'max_depth': 9},
  mean: 131.87804, std: 0.92080, params: {'min_samples_split': 2000, 'max_depth': 9},
  mean: 131.87007, std: 0.89008, params: {'min_samples_split': 2200, 'max_depth': 9},
  mean: 131.99323, std: 0.90087, params: {'min_samples_split': 1600, 'max_depth': 11},
  mean: 131.92444, std: 0.91064, params: {'min_samples_split': 1800, 'max_depth': 11},
  mean: 131.86591, std: 0.92035, params: {'min_samples_split': 2000, 'max_depth': 11},
  mean: 131.90265, std: 0.90073, params: {'min_samples_split': 2200, 'max_depth': 11},
  mean: 132.05908, std: 0.86780, params: {'min_samples_split': 1600, 'max_depth': 13},
  mean: 131.98959, std: 0.93917, params: {'min_samples_split': 1800, 'max_depth': 13},
  mean: 131.95606, std: 0.90084, params: {'min_samples_split': 2000, 'max_depth': 13},
  mean: 131.95021, std: 0.88395, params: {'min_samples_split': 2200, 'max_depth': 13},
  mean: 132.07220, std: 0.88168, params: {'min_samples_split': 1600, 'max_depth': 15},
  mean: 132.00883, std: 0.91234, params: {'min_samples_split': 1800, 'max_depth': 15},
  mean: 131.98008, std: 0.84146, params: {'min_samples_split': 2000, 'max_depth': 15},
  mean: 131.92188, std: 0.88942, params: {'min_samples_split': 2200, 'max_depth': 15} ]
### Best Params:
{'min_samples_split': 2000, 'max_depth': 7}
### Best Score:
131.798357547

## Test 3:
### Params:
- learning_rate=0.05
- n_estimators=110
- min_samples_split=2000
- max_depth=7
- max_features='sqrt'
- subsample=0.8
- random_state=10
### Testing:
min_samples_leaf:range(20,60,10)
### Grid Scores:
[ mean: 131.82473, std: 0.89998, params: {'min_samples_leaf': 20},
  mean: 131.79676, std: 0.89024, params: {'min_samples_leaf': 30},
  mean: 131.81459, std: 0.90244, params: {'min_samples_leaf': 40},
  mean: 131.79836, std: 0.92241, params: {'min_samples_leaf': 50},
  mean: 131.83921, std: 0.89108, params: {'min_samples_leaf': 60} ]
### Best Params:
{'min_samples_leaf': 30}
### Best Score:
131.796759794

## Test 4:
### Params:
- learning_rate=0.05
- n_estimators=110
- min_samples_split=2000
- max_depth=7
- min_samples_leaf=30
- subsample=0.8
- random_state=10
### Testing:
max_features:range(1,6,1)
### Grid Scores:
[ mean: 132.23239, std: 0.95473, params: {'max_features': 1},
  mean: 131.79676, std: 0.89024, params: {'max_features': 2},
  mean: 131.85842, std: 0.90482, params: {'max_features': 3},
  mean: 131.82599, std: 0.86581, params: {'max_features': 4},
  mean: 131.85100, std: 0.88630, params: {'max_features': 5} ]
### Best Params:
{'max_features': 2}
### Best Score:
131.796759794

## Test 5:
### Params:
- learning_rate=0.05
- n_estimators=110
- min_samples_split=2000
- max_depth=7
- min_samples_leaf=30
- max_features=2
- random_state=10
### Testing:
subsample:range(0.6,0.91,0.05)
### Grid Scores:
[ mean: 131.84650, std: 0.89927, params: {'subsample': 0.6},

  mean: 131.87023, std: 0.87768, params: {'subsample': 0.65},
  
  mean: 131.87063, std: 0.89977, params: {'subsample': 0.7},
  
  mean: 131.86186, std: 0.88008, params: {'subsample': 0.75},
  
  mean: 131.79676, std: 0.89024, params: {'subsample': 0.8},
  
  mean: 131.85638, std: 0.87975, params: {'subsample': 0.85},
  
  mean: 131.86887, std: 0.90642, params: {'subsample': 0.9} ]
### Best Params:
{'subsample': 0.8}
### Best Score:
131.796759794

# Learning Rate / N_Estimators Tuning
## Test 1:
### Params:
- min_samples_split=2000
- max_depth=7
- min_samples_leaf=30
- max_features=2
- subsample=0.8
- random_state=10
### Testing:
- learning_rate=0.05
- n_estimators=110
### MSE Stats:
- Mean: 131.9024
- Std: 1.37687
- Min: 134.2828
- Max: 130.1444
### RMSE Stats:
- Mean: 11.4849
- Std: 1.1734
- Min: 11.5880
- Max: 11.4081

## Test 2:
### Params:
- min_samples_split=2000
- max_depth=7
- min_samples_leaf=30
- max_features=2
- subsample=0.8
- random_state=10
### Testing:
- learning_rate=0.01
- n_estimators=550
### MSE Stats:
- Mean: 131.7543
- Std: 1.37157
- Min: 134.1603
- Max: 130.0827
### RMSE Stats:
- Mean: 11.4784
- Std: 1.1711
- Min: 11.5828
- Max: 11.4054

## Test 3:
### Params:
- min_samples_split=2000
- max_depth=7
- min_samples_leaf=30
- max_features=2
- subsample=0.8
- random_state=10
### Testing:
- learning_rate=0.005
- n_estimators=1100
### MSE Stats:
- Mean: 131.7341
- Std: 1.3716
- Min: 134.1210
- Max: 130.0134
### RMSE Stats:
- Mean: 11.4775
- Std: 1.1711
- Min: 11.5811
- Max: 11.4023

## Test 4:
### Params:
- min_samples_split=2000
- max_depth=7
- min_samples_leaf=30
- max_features=2
- subsample=0.8
- random_state=10
### Testing:
- learning_rate=0.005
- n_estimators=1500
### MSE Stats:
- Mean: 131.7029
- Std: 1.341887
- Min: 134.0236
- Max: 130.0048
### RMSE Stats:
- Mean: 11.4762
- Std: 1.1584
- Min: 11.5769
- Max: 11.4020

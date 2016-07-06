# Removing outliers:
# For steps, total_sleep, and resting_hr columns:
# 1. Mark bottom 3% and top 3% as outliers
# 2. Don't use this data in analysis
#
# Calculating health score:
# For steps, total_sleep, and resting_hr columns:
# 1. Calculate the following metrics for all data in each column:
#     - 3rd and 97th percentiles, range in between those percentiles
# 2. For each data point, calculate: (value - 3rd percentile) / range
#    This is the score for the respective column (step score, sleep score, hr score)
# 3. Multiply this number by the respective weight of the column (40/20/40 step/sleep/hr)
# 4. Take weighted average to calculate health score

import sys
import csv
import numpy as np
import pandas as pd
import calculation_helpers as calc

def clean_data():
    # When calling the function from terminal, call:
    # python clean_data.py output_file csv_file
    output_file = sys.argv[1]
    csv_file = sys.argv[2]

    with open(csv_file, 'rbU') as input:
        with open(output_file, 'w') as output:
            reader = csv.reader(input)
            writer = csv.writer(output)
            headers = next(reader)
            data_list = list(reader)

            user_index = headers.index('user_id')
            date_index = headers.index('date')
            steps_index = headers.index('steps')
            sleep_index = headers.index('total_sleep')
            hr_index = headers.index('resting_hr')

            # Calculate 3rd and 97th percentiles and range for steps, sleep, and hr
            steps_3rd = calc.find_percentile(data_list, steps_index, 3)
            steps_97th = calc.find_percentile(data_list, steps_index, 97)
            steps_range = steps_97th - steps_3rd
            steps_weight = 0.4
            sleep_3rd = calc.find_percentile(data_list, sleep_index, 3)
            sleep_97th = calc.find_percentile(data_list, sleep_index, 97)
            sleep_range = sleep_97th - sleep_3rd
            sleep_weight = 0.2
            hr_3rd = calc.find_percentile(data_list, hr_index, 3)
            hr_97th = calc.find_percentile(data_list, hr_index, 97)
            hr_range = hr_97th - hr_3rd
            hr_weight = 0.4

            # Create extra headers for computed fields
            added_columns = [
                'outlier_tag',
                'step_score',
                'sleep_score',
                'hr_score',
                'step_week_slope',
                'sleep_week_slope',
                'hr_week_slope',
                'curr_health_score',
                'health_score_in_week',
            ]
            for column in added_columns:
                headers.append(column)
            writer.writerow(headers);
            print 'Finished writing headers'

            # Tag outliers (<3rd or >97th percentile)
            for row in data_list:
                if (
                        float(row[steps_index]) > steps_97th or
                        float(row[steps_index]) < steps_3rd or
                        float(row[sleep_index]) > sleep_97th or
                        float(row[sleep_index]) < sleep_3rd or
                        float(row[hr_index]) > hr_97th or
                        float(row[hr_index]) < hr_3rd
                    ):
                    outlier_tag = 1
                else:
                    outlier_tag = 0
                row.append(outlier_tag)
                writer.writerow(row)

            output.close()
            print 'Finished labeling outliers'

            # Perform first set of calulcations on non-outliers
            df_first = pd.DataFrame.from_csv(output_file)
            # Don't perform calculations on outliers
            outlier = df_first['outlier_tag']!=1
            df_first = df_first[outlier]
            with open(output_file, 'w') as output_first_calcs:
                writer = csv.writer(output_first_calcs)
                writer.writerow(headers);
                
                # Perform first calculations on each row of data
                for row in data_list:
                    steps_score = np.subtract(float(row[steps_index]), steps_3rd) / steps_range
                    sleep_score = np.subtract(float(row[sleep_index]), sleep_3rd) / sleep_range
                    hr_score = 1 - (np.subtract(float(row[hr_index]), hr_3rd) / hr_range)
                    step_week_slope = calc.find_days_before_slope(df_first, row[user_index], row[date_index], 'steps', 7)
                    sleep_week_slope = calc.find_days_before_slope(df_first, row[user_index], row[date_index], 'total_sleep', 7)
                    hr_week_slope = calc.find_days_before_slope(df_first, row[user_index], row[date_index], 'resting_hr', 7)
                    curr_health_score = ((steps_score * steps_weight) + (sleep_score * sleep_weight) + (hr_score * hr_weight)) * 100

                    stats = [
                        steps_score,
                        sleep_score,
                        hr_score,
                        step_week_slope,
                        sleep_week_slope,
                        hr_week_slope,
                        curr_health_score
                    ]
                    # Commit calculations
                    for item in stats:
                        row.append(item)
                    writer.writerow(row)

            output_first_calcs.close()
            print 'Finished first set of calculations'

            # Perform second set of calulcations on non-outliers
            df_second = pd.DataFrame.from_csv(output_file)
            # Don't perform calculations on outliers
            outlier = df_second['outlier_tag']!=1
            df_second = df_second[outlier]
            with open(output_file, 'w') as output_second_calcs:
                writer = csv.writer(output_second_calcs)
                writer.writerow(headers);
                # Perform second calculations on each row of data
                for row in data_list:
                    health_score_in_week = calc.find_data(df_second, row[user_index], row[date_index], 'curr_health_score', 7)
                    stats = [health_score_in_week]
                    # Commit calculations
                    for item in stats:
                        row.append(item)
                    writer.writerow(row)
            print 'Finished second set of calculations'

clean_data()

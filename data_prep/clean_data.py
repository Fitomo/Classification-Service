# Removing outliers:
# For steps, total_sleep, and resting_hr columns:
# 1. Mark bottom 5% and top 5% as outliers
# 2. Don't use this data in analysis
#
# Calculating health score:
# For steps, total_sleep, and resting_hr columns:
# 1. Calculate the following metrics for all data in each column:
#     - min, max, range, mean, percentiles
# 2. For each data point, calculate: (value - min) / range
#    This is the score for the respective column (step score, sleep score, hr score)
# 3. Multiply this number by the respective weight of the column (40/20/40 step/sleep/hr)
# 4. Add all of these weighted numbers together to reach the health score

import sys
import csv
import numpy as np
import pandas as pd
import calculation_helpers as calc

def clean_data():
    csv_file = sys.argv[1]
    output_file = sys.argv[2]
    metrics = {}

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

            # calc mean, 3rd and 97th percentiles for steps, sleep, and hr
            steps_mean = calc.find_mean(data_list, steps_index);
            steps_3rd = calc.find_percentile(data_list, steps_index, 3)
            steps_97th = calc.find_percentile(data_list, steps_index, 97)
            steps_range = steps_97th - steps_3rd
            steps_weight = 0.4
            sleep_mean = calc.find_mean(data_list, sleep_index);
            sleep_3rd = calc.find_percentile(data_list, sleep_index, 3)
            sleep_97th = calc.find_percentile(data_list, sleep_index, 97)
            sleep_range = sleep_97th - sleep_3rd
            sleep_weight = 0.2
            hr_mean = calc.find_mean(data_list, hr_index);
            hr_3rd = calc.find_percentile(data_list, hr_index, 3)
            hr_97th = calc.find_percentile(data_list, hr_index, 97)
            hr_range = hr_97th - hr_3rd
            hr_weight = 0.4

            all_data = []
            added_columns = [
                'outlier_tag',
                'step_score',
                'sleep_score',
                'hr_score',
                'step_weight',
                'sleep_weight',
                'hr_weight',
                'step_week_slope',
                'sleep_week_slope',
                'hr_week_slope',
                'step_month_slope',
                'sleep_month_slope',
                'hr_month_slope',
                'health_score',
            ]
            for column in added_columns:
                headers.append(column)
            writer.writerow(headers);

            # tag outliers
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

            # perform calcs on non-outliers
            df = pd.DataFrame.from_csv(output_file)
            outlier = df['outlier_tag'] != 1
            df = df[outlier]
            with open(output_file, 'w') as output_calcs:
                writer = csv.writer(output_calcs)
                writer.writerow(headers);
                for row in data_list:
                    steps_score = np.subtract(float(row[steps_index]), steps_3rd) / steps_range
                    sleep_score = np.subtract(float(row[sleep_index]), sleep_3rd) / sleep_range
                    hr_score = 1 - (np.subtract(float(row[hr_index]), hr_3rd) / hr_range)
                    step_week_slope = calc.find_days_before_slope(df, row[user_index], row[date_index], 'steps', 6, 8)
                    sleep_week_slope = calc.find_days_before_slope(df, row[user_index], row[date_index], 'total_sleep', 6, 8)
                    hr_week_slope = calc.find_days_before_slope(df, row[user_index], row[date_index], 'resting_hr', 6, 8)
                    step_month_slope = calc.find_days_before_slope(df, row[user_index], row[date_index], 'steps', 29, 31)
                    sleep_month_slope = calc.find_days_before_slope(df, row[user_index], row[date_index], 'total_sleep', 29, 31)
                    hr_month_slope = calc.find_days_before_slope(df, row[user_index], row[date_index], 'resting_hr', 29, 31)
                    health_score = ((steps_score * steps_weight) + (sleep_score * sleep_weight) + (hr_score * hr_weight)) * 100

                    stats = [
                        steps_score,
                        sleep_score,
                        hr_score,
                        steps_weight,
                        sleep_weight,
                        hr_weight,
                        step_week_slope,
                        sleep_week_slope,
                        hr_week_slope,
                        step_month_slope,
                        sleep_month_slope,
                        hr_month_slope,
                        health_score
                    ]
                    for item in stats:
                        row.append(item)
                    writer.writerow(row)

clean_data()

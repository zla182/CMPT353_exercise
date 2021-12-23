'''
Author: your name
Date: 2021-10-13 15:18:42
LastEditTime: 2021-10-15 22:40:34
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \exercise_5\reddit_weekends.py
'''
import sys
import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
# import matplotlib.pyplot as plt


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    counts = pd.read_json(sys.argv[1], lines=True)

    counts = counts[((counts['date'].dt.year == 2012) 
                    | (counts['date'].dt.year == 2013)) 
                    & (counts['subreddit'] == 'canada')]
    
    weekdays = counts[((counts['date'].dt.weekday != 5) 
                        & (counts['date'].dt.weekday != 6))]
    weekends = counts[((counts['date'].dt.weekday == 5) 
                        | (counts['date'].dt.weekday == 6))]
    
    # T-test
    initial_ttest_p = stats.ttest_ind(weekends['comment_count'],weekdays['comment_count']).pvalue
    initial_weekday_normality_p = stats.normaltest(weekdays['comment_count']).pvalue
    initial_weekend_normality_p = stats.normaltest(weekends['comment_count']).pvalue
    initial_levene_p = stats.levene(weekends['comment_count'], weekdays['comment_count']).pvalue
    

    # plt.hist(weekdays['comment_count'])
    # plt.show()
    # plt.hist(weekends['comment_count'])
    # plt.show()
    
    # # log()
    # transformed_weekend = np.log(weekends['comment_count'])
    # transformed_weekend_normality_p = stats.normaltest(transformed_weekend).pvalue
    # transformed_weekday = np.log(weekdays['comment_count'])
    # transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    # transformed_levene_p = stats.levene(transformed_weekend,transformed_weekday).pvalue
    # # Transformed data normality p-values: 0.000402 0.315
    # # Transformed data equal-variance p-value: 0.000419  

    # # exp()
    # transformed_weekend = np.exp(weekends['comment_count'])
    # transformed_weekend_normality_p = stats.normaltest(transformed_weekend).pvalue
    # transformed_weekday = np.exp(weekdays['comment_count'])
    # transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    # transformed_levene_p = stats.levene(transformed_weekend,transformed_weekday).pvalue
    # # Transformed data normality p-values: nan nan
    # # Transformed data equal-variance p-value: nan


    # sqrt()
    transformed_weekend = np.sqrt(weekends['comment_count'])
    transformed_weekend_normality_p = stats.normaltest(transformed_weekend).pvalue
    transformed_weekday = np.sqrt(weekdays['comment_count'])
    transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    transformed_levene_p = stats.levene(transformed_weekend,transformed_weekday).pvalue
    # Transformed data normality p-values: 0.0369 0.108
    # Transformed data equal-variance p-value: 0.556  

    # # counts**2
    # transformed_weekend = (weekends['comment_count'])**2
    # transformed_weekend_normality_p = stats.normaltest(transformed_weekend).pvalue
    # transformed_weekday = (weekdays['comment_count'])**2
    # transformed_weekday_normality_p = stats.normaltest(transformed_weekday).pvalue
    # transformed_levene_p = stats.levene(transformed_weekend,transformed_weekday).pvalue
    # # Transformed data normality p-values: 2.78e-29 2.99e-11
    # # Transformed data equal-variance p-value: 7.39e-08


    #Fix 2 : Central Limit Theorem
    separate_weekends = weekends['date'].dt.isocalendar()
    separate_weekends = separate_weekends[['year','week']]
    weekends = pd.concat([weekends, separate_weekends], axis=1)
    
    separate_weekdays = weekdays['date'].dt.isocalendar()
    separate_weekdays = separate_weekdays[['year','week']]
    weekdays = pd.concat([weekdays,separate_weekdays], axis=1)
    
    new_weekends = weekends.groupby(by=['year','week']).aggregate('mean').reset_index()
    new_weekdays = weekdays.groupby(by=['year','week']).aggregate('mean').reset_index()
    
    weekly_weekday_normality_p = stats.normaltest(new_weekdays['comment_count']).pvalue
    weekly_weekend_normality_p = stats.normaltest(new_weekends['comment_count']).pvalue
    weekly_levene_p = stats.levene(new_weekends['comment_count'],new_weekdays['comment_count']).pvalue  
    weekly_ttest_p = stats.ttest_ind(new_weekends['comment_count'],new_weekdays['comment_count']).pvalue
    
    #Fix 3 : Non-parametric test
    utest_p = stats.mannwhitneyu(weekends['comment_count'],weekdays['comment_count'], 
                                use_continuity=True, alternative='two-sided').pvalue
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p = initial_ttest_p,
        initial_weekday_normality_p = initial_weekday_normality_p,
        initial_weekend_normality_p = initial_weekend_normality_p,
        initial_levene_p = initial_levene_p,
        transformed_weekday_normality_p = transformed_weekday_normality_p,
        transformed_weekend_normality_p = transformed_weekend_normality_p,
        transformed_levene_p = transformed_levene_p,
        weekly_weekday_normality_p = weekly_weekday_normality_p,
        weekly_weekend_normality_p = weekly_weekend_normality_p,
        weekly_levene_p = weekly_levene_p,
        weekly_ttest_p = weekly_ttest_p,
        utest_p = utest_p,
    ))


if __name__ == '__main__':
    main()

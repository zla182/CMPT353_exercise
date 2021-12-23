'''
Author: your name
Date: 2021-10-20 12:03:41
LastEditTime: 2021-10-20 13:03:43
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \e6\ab_analysis.py
'''
import sys
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import mannwhitneyu
OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]
    data = pd.read_json(searchdata_file,orient='records',lines=True)
    even_data = data[data['uid']%2==0].reset_index().drop(['index'], axis=1)
    odd_data = data[data['uid']%2!=0].reset_index().drop(['index'], axis=1)
    
    # did a different fraction of users have search count > 0
    mask_even_zero=even_data['search_count'] == 0
    even_data_zero = even_data[mask_even_zero]
    even_data_nonzero = even_data[~mask_even_zero]
    mask_odd = odd_data['search_count'] == 0
    odd_data_zero = odd_data[mask_odd]
    odd_data_nonzero = odd_data[~mask_odd]

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
    len_even_data_zero = len(even_data_zero)
    len_even_data_nonzero = len(even_data_nonzero)
    len_odd_data_zero = len(odd_data_zero)
    len_odd_data_nonzero = len(odd_data_nonzero)
    obs = [[len_even_data_nonzero,len_even_data_zero],
            [len_odd_data_nonzero,len_odd_data_zero]]
    g, more_users_p, dof, expctd = chi2_contingency(obs)

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    more_searches_p = mannwhitneyu(even_data['search_count'],odd_data['search_count']).pvalue

    # Repeat the above analysis looking only at instructors.
    instructor_even_data = even_data[even_data['is_instructor']==True].reset_index().drop(['index'], axis=1)
    instructor_odd_data = odd_data[odd_data['is_instructor']==True].reset_index().drop(['index'], axis=1)
    
    # did a different fraction of users have search count > 0
    mask_instructor_even_zero = instructor_even_data['search_count'] == 0
    instructor_even_zero = instructor_even_data[mask_instructor_even_zero]
    instructor_even_nonzero = instructor_even_data[~mask_instructor_even_zero]
    mask_instructor_odd_zero = instructor_odd_data['search_count'] == 0
    instructor_odd_zero = instructor_odd_data[mask_instructor_odd_zero]
    instructor_odd_nonzero = instructor_odd_data[~mask_instructor_odd_zero]

    len_instructor_even_zero = len(instructor_even_zero)
    len_instructor_even_nonzero = len(instructor_even_nonzero)
    len_instructor_odd_zero = len(instructor_odd_zero)
    len_instructor_odd_nonzero = len(instructor_odd_nonzero)

    obs_instructor = [[len_instructor_even_nonzero,len_instructor_even_zero],
            [len_instructor_odd_nonzero,len_instructor_odd_zero]]

    g, more_instr_p, dof, expctd = chi2_contingency(obs_instructor)

    more_instr_searches_p = mannwhitneyu(instructor_even_data['search_count'],instructor_odd_data['search_count']).pvalue
    # ...

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=more_users_p,
        more_searches_p=more_searches_p,
        more_instr_p=more_instr_p,
        more_instr_searches_p=more_instr_searches_p,
    ))


if __name__ == '__main__':
    main()

from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

movies = pd.read_csv('ratings.csv')
# movies = pd.read_csv('Data/ratings_Electronics.csv')
movies = movies.sort_values(by='userId')
print movies
dff = movies.userId.unique()
df = pd.DataFrame(columns=[
    'userid',
    '5',
    '4',
    '3',
    '2',
    '1',
    'mean',
    'lt3',
    'gt3',
    'z-score_lt3',
    'z-score_gt3',
    ])
count = 1
for id in dff:
    rating_5 = movies[(movies.userId == id) & ((movies.rating == 5.0)
                      | (movies.rating == 4.5))]
    rating_4 = movies[(movies.userId == id) & ((movies.rating == 4.0)
                      | (movies.rating == 3.5))]
    rating_3 = movies[(movies.userId == id) & ((movies.rating == 3.0)
                      | (movies.rating == 2.5))]
    rating_2 = movies[(movies.userId == id) & ((movies.rating == 2.0)
                      | (movies.rating == 1.5))]
    rating_1 = movies[(movies.userId == id) & ((movies.rating == 1.0)
                      | (movies.rating == 0.5))]
    mean_rating = (len(rating_5) + len(rating_4) + len(rating_3)
                   + len(rating_2) + len(rating_1)) / 5
    sum_of_ratings = len(rating_5) + len(rating_4) + len(rating_3) \
        + len(rating_2) + len(rating_1)
    
    if sum_of_ratings > 3 and sum_of_ratings < 5000:
        lt3 = len(rating_1) + len(rating_2) + len(rating_3)
        gt3 = len(rating_4) + len(rating_5)  
        zscore_lt3 = (mean_rating- lt3) /  sum_of_ratings
        zscore_gt3 = (mean_rating - lt3) /  sum_of_ratings
        if zscore_lt3 <=-1.65:
            print "Spam Score (Significance value = 0.05) = ",zscore_lt3," | User id = ", id ," | Reviews greater than 3 = ",gt3 ,"| Reviews less than 3 " ,lt3
        zscore_gt3 = 1-zscore_gt3
        if zscore_gt3  >= 1.65:
            print "Spam Score (Significance value = 0.05) = ",zscore_gt3 ," | User id = ", id ," | Reviews greater than 3 = ",gt3 ,"| Reviews less than 3 " ,lt3
      
        df.loc[count] = [
            id,
            len(rating_5),
            len(rating_4),
            len(rating_3),
            len(rating_2),
            len(rating_1),
            mean_rating,
            lt3,
            gt3,
            round(zscore_gt3,3),
            round(zscore_lt3,3)
            ]
        count += 1
df.to_csv('Summary.csv')
print df
freq_5 = df['5'].sum()
freq_4 = df['4'].sum()
freq_3 = df['3'].sum()
freq_2 = df['2'].sum()
freq_1 = df['1'].sum()

ax1 = plt.subplot(212)
plt.title("Average User rating Freguency histogram")
plt.xlabel('Ratings')
plt.ylabel('Frequency Of Rating')
plt.bar(['1', '2', '3', '4', '5'], [freq_1, freq_2, freq_3, freq_4,
        freq_5])

ax1 = plt.subplot(221)
plt.title("User Span Score (Significance level = 0.05 )")
plt.xlabel('User Id')
plt.ylabel('Spam-Score(z-score)')
df['z-score_lt3'].plot()
plt.axhline(y=1.65,   color='r', linestyle='-')

ax1 = plt.subplot(222)
plt.title("User Spam Score (Significance level = 0.05 )")
plt.xlabel('User Id')
plt.ylabel('Spam-Score(z-score)')
plt.axvline(x=1.65,   color='r', linestyle='-')
plt.scatter(df['z-score_lt3'],df['userid'])
plt.show()

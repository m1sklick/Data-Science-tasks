# Section 1
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('data/Section 1 data.csv')

# Question 1
unique_restaurants = data['Business_ID'].nunique()

# Question 2
review_counts = data.groupby('Business_ID').size() # total number of reviws per restaurant
most_reviewed_id = review_counts.idxmax() # Business_ID
most_reviewed_count = review_counts.max() # number of reviews for that ID
most_reviewed_name = data.loc[data['Business_ID'] == most_reviewed_id, 'Business_Name'].iloc[0] # find the restaurants name
percentage = (most_reviewed_count / review_counts.sum()) * 100 # percentage

# Question 3
nv5startreviews = data[(data['State'] == 'NV') & (data['Avg_Business_Star_Rating'] >= 5)] # filter the data to see only rows with 'NV' state and stars >= 5
unique_cities = nv5startreviews['City'].unique() # no need to show one city's name several times

# Question 4
ht_reviews = data[data['Business_Category'] == 'Hotels & Travel'] # filter rows with "Hotels & Travel" category only
city_review_counts = ht_reviews.groupby('City').size() # group by city and count the number of reviews
r_city = city_review_counts.idxmax()  # save the city name
r_city_reviews = city_review_counts.max()  # number of reviews in that city
percentage = (r_city_reviews / city_review_counts.sum()) * 100 # find the percentage

# Question 5
data['Review_Date'] = pd.to_datetime(data['Review_Date']) # cast its data type(dtype) from "object" to "datetime64[ns]" to be able to use pandas
data['Day_of_Week'] = data['Review_Date'].dt.day_name() # create a new column to save the day of the week
week_day_reviews = data['Day_of_Week'].value_counts() # count number of each days of the week in our current dataset
highest_day = week_day_reviews.idxmax() # find the day with the highest number
most_reviews = week_day_reviews.max() # find the maximum number of reviews

# Question 6
# we already casted the data type in 'Review_Date' column in "Question 5" operations so we skip this part
data['YearMonth'] = data['Review_Date'].dt.to_period('M')  # Extract year-month for grouping
plt_trend = data.groupby('YearMonth')['Avg_Business_Star_Rating'].mean()

# Question 7 *******************************

# Question 8
# Haversine function - taken from the internet
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    # Differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

data = data.sort_values(by=['User_ID', 'Review_Date']) # sort by User_ID and Review_Date

distances = [] # we will save total calculated distances for each user here

for user_id, group in data.groupby('User_ID'): # calculate the distance for each user separately and save it in distances variable
    group = group[['Latitude', 'Longitude']].values
    user_distance = 0
    for i in range(1, len(group)):
        user_distance += haversine(group[i - 1][0], group[i - 1][1], group[i][0], group[i][1]) # Haversine formula applied here
    distances.append((user_id, user_distance))

distance_df = pd.DataFrame(distances, columns=['User_ID', 'Cumulative_Distance']) # create a dataframe to be able to use abilities of pandas to just find the max distance and get its User_ID
top_user = distance_df.loc[distance_df['Cumulative_Distance'].idxmax()]


print(f"1. How many unique restaurants could be found in this data set? (Hint: Use the [Business_ID] column for this evaluation.)\nThe Number of unique restaurants: {unique_restaurants}")
print(f"2. Which restaurant received the highest number of reviews? What about percentage-wise?\nRestaurant with the highest number of reviews: {most_reviewed_name}(Business_ID: {most_reviewed_id}) with {most_reviewed_count} reviews.\nIt accounts for {percentage:.2f}% of the total reviews.")
print(f"3. Which cities have got at least one 5-star review in Nevada (NV) state?\nThe cities with at least one 5-star review: {unique_cities}")
print(f"4. Which city has the highest number of reviews in the Business Category of “Hotels & Travel”? What about percentage-wise?\nThe city with the highest number of reviews in 'Hotels & Travel' is '{r_city}' with {r_city_reviews} reviews.\nIt accounts for {percentage:.2f}% of the total reviews in this category.")
print(f"5. At what day of the week people are more likely to post their reviews?\nPeople are more likely to post their reviews on {highest_day} which stands for {most_reviews} reviews.")
print(f"6. Showcase if there are any trends regarding restaurant performance as time goes by. - shown in the plot")
# display the plot
plt.figure(figsize=(10, 6))
plt_trend.plot(kind='line', marker='o')
plt.title('Average Restaurant Ratings Over Time', fontsize=14)
plt.xlabel('Time (Year-Month)', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)
plt.grid()
plt.show()
print(f"7. Based on analyzed data showcase if there are any steps that the restaurant can take to improve their public appeal.\nAnswer is in the presentation along with the result of this application")
print(f"8. Bonus Question – Based on this data set which user had the highest cumulative travel distance? What distance has been covered by him/her?\nUser with ID: {top_user['User_ID']} covered the highest distance of: {top_user['Cumulative_Distance']:.2f} km.")

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to convert datetime.time to seconds
def time_to_seconds(time_str):
    time_obj = pd.to_datetime(time_str, format='%H:%M:%S', errors='coerce')
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

# Read the Excel file
survey_data = pd.read_excel('survey_responses.xlsx')

# Convert the time data to seconds
survey_data['ROOM1'] = survey_data['ROOM1'].apply(time_to_seconds)
survey_data['Hall'] = survey_data['Hall'].apply(time_to_seconds)
survey_data['ROOM2'] = survey_data['ROOM2'].apply(time_to_seconds).dropna()
survey_data['ROOM3'] = survey_data['ROOM3'].apply(time_to_seconds).dropna()

# Calculate the average time spent in each room
average_room1 = survey_data['ROOM1'].mean()
average_hall = survey_data['Hall'].mean()
average_room2 = survey_data['ROOM2'].mean()
average_room3 = survey_data['ROOM3'].mean()

# Convert the average times to minutes
average_room1 /= 60
average_hall /= 60
average_room2 /= 60
average_room3 /= 60

# Create a pie chart
rooms = ['Room 1', 'Hall', 'Room 2', 'Room 3']
average_durations = [average_room1, average_hall, average_room2, average_room3]

plt.figure(figsize=(10, 5))
plt.pie(average_durations, labels=rooms, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Average proportion of time spent in each room')
plt.xlabel('')
plt.ylabel('')
plt.savefig('room_durations.png', dpi=300)



# extract data for red and blue groups
red_data = survey_data.loc[survey_data['Color'] != 'Blue', 'Monster Colors']
blue_data = survey_data.loc[survey_data['Color'] == 'Blue', 'Monster Colors']

# calculate means and standard deviations
red_mean = np.mean(red_data)
red_std = np.std(red_data)
blue_mean = np.mean(blue_data)
blue_std = np.std(blue_data)

# plot the bar plot
fig, ax = plt.subplots()
ax.bar(['Red', 'Blue'], [red_mean, blue_mean], yerr=[red_std, blue_std], capsize=10, color=['red', 'blue'], alpha=0.7)
ax.set_ylabel('Ratings')
ax.set_title('Ratings of Monster Colours on Fear Perception')

# add numeric labels inside the bars
for i, mean in enumerate([red_mean, blue_mean]):
    ax.annotate(f'{mean:.2f}', xy=(i, mean), ha='center', fontsize=12, fontweight='bold',
                xytext=(0, -12), textcoords='offset points', va='top', color='white')
plt.show()




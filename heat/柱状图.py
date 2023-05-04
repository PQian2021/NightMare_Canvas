import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a DataFrame from the given data
data = """
User	Color	Sex	Complete	Total time	ROOM1	Hall	ROOM2	ROOM3	Overall Atmosphere	Monster Designs	Monster Colors	Monster Sizes	Sound Effects	Immersion	Level Design	Puzzle Mechanics	Heart Rate System	Game Controls	Enjoyment	Challenging	Recommendation	Future Interest	Expectations	resting heart rate	gaming heart rate	High heart rate	Low heart rate
MYC	Blue	Male	TRUE	0:18:40	0:04:18	0:01:35	0:06:00	0:06:47	4	4	2	5	5	5	4	4	2	5	4	4	5	5	5	98.16 	121.41	146	78
XLJ	Blue	Male	TRUE	0:14:49	0:03:38	0:01:15	0:04:17	0:05:32	4	4	2	5	2	5	5	5	3	4	5	4	5	3	5	81.43 	86.81	105	77
DMZ	Blue	Male	TRUE	0:21:52	0:05:20	0:01:43	0:11:11	0:03:38	5	5	3	5	5	4	4	3	5	2	5	5	5	1	5	91.76 	99.36	114	85
DEF	Blue	Male	TRUE	0:20:10	0:05:14	0:01:58	0:07:21	0:05:37	3	3	2	3	3	5	2	2	1	4	3	3	3	1	3	89.67 	104.25	128	83
JKL	Blue	Male	TRUE	0:17:45	0:04:55	0:01:40	0:05:50	0:05:20	4	4	3	4	4	3	3	3	1	2	4	4	4	2	4	96.54 	102.68	120	79
HZY	Blue	Male	FALSE	0:05:24	0:03:54	0:01:30	#	#	4	3	4	4	4	4	3	3	2	4	3	2	3	1	4	78.32 	94.19	121	77
SWT	Red	Male	TRUE	0:19:20	0:02:50	0:02:19	0:07:23	0:06:48	4	3	1	5	5	5	2	1	1	2	3	3	4	1	4	87.21 	107.51	138	89
WHZ	Red	Male	TRUE	0:21:15	0:06:08	0:02:01	0:07:15	0:05:51	5	4	4	5	4	5	4	4	3	5	4	4	5	2	5	94.83 	108.62	132	87
LBH	Red	Male	TRUE	0:21:10	0:04:19	0:05:01	0:04:58	0:06:52	4	3	4	4	5	5	3	3	2	2	3	3	3	2	4	105.21 	109.85	138	95
ABC	Red	Male	TRUE	0:16:35	0:03:52	0:02:05	0:05:30	0:05:08	5	4	3	4	5	4	5	5	2	3	5	4	5	3	5	103.12 	114.29	134	92
GHI	Red	FeMale	TRUE	0:18:22	0:04:10	0:02:25	0:06:14	0:05:33	5	5	5	5	5	5	5	5	4	5	5	5	5	4	5	92.38 	105.92	134	88
ZZY	Red	FeMale	FALSE	0:07:04	0:05:08	0:01:56	#	#	4	1	3	3	5	4	4	2	1	2	4	4	4	1	4	99.54 	102.15	124	81
"""
data = [line.split('\t') for line in data.strip().split('\n')]
columns = data.pop(0)
df = pd.DataFrame(data, columns=columns)

# Convert columns to numeric where appropriate
numeric_columns = [
    'Overall Atmosphere', 'Monster Designs', 'Monster Colors', 'Monster Sizes', 'Sound Effects',
    'Immersion', 'Level Design', 'Puzzle Mechanics', 'Heart Rate System', 'Game Controls',
    'Enjoyment', 'Challenging', 'Recommendation', 'Future Interest', 'Expectations']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

# Calculate mean and standard deviation for fear-inducing elements
fear_columns = ['Enjoyment', 'Challenging', 'Recommendation', 'Future Interest', 'Expectations']
fear_means = df[fear_columns].mean()
fear_stds = df[fear_columns].std()

# Calculate mean and standard deviation for game immersion elements
immersion_columns = ['Immersion', 'Level Design', 'Puzzle Mechanics', 'Heart Rate System', 'Game Controls']
immersion_means = df[immersion_columns].mean()
immersion_stds = df[immersion_columns].std()

# Plot bar charts for fear-inducing elements and game immersion elements
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Fear-inducing elements bar chart
ax1.bar(fear_columns, fear_means, yerr=fear_stds, capsize=10, color='darkred', alpha=0.7)
ax1.set_xticklabels(fear_columns, rotation=45, ha='right')
ax1.set_ylabel('Ratings')
ax1.set_title('Overall Game Experience Ratings')



# Game immersion elements bar chart
ax2.bar(immersion_columns, immersion_means, yerr=immersion_stds, capsize=10, color='darkblue', alpha=0.7)
ax2.set_xticklabels(immersion_columns, rotation=45, ha='right')
ax2.set_ylabel('Ratings')
ax2.set_title('Game Immersion Elements Ratings')

# Add numeric labels inside the bars
for ax, means, stds in zip([ax1, ax2], [fear_means, immersion_means], [fear_stds, immersion_stds]):
    for i, (mean, std) in enumerate(zip(means, stds)):
        ax.annotate(f'{mean:.2f}', xy=(i, mean), ha='center', fontsize=12, fontweight='bold',
                    xytext=(0, -12), textcoords='offset points', va='top', color='white')

plt.tight_layout()
plt.show()
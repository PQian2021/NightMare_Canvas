import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Import the data
data = pd.read_excel('Survey.xlsx', sheet_name='1')

# Define the groups of monsters
groups = [('size', ['human', 'colossal']),
          ('shape', ['humanoid', 'quadruped']),
          ('color', ['black', 'white', 'red', 'blue', 'yellow']),
          ('semantic', ['ghosty', 'devil', 'evil'])]

# Calculate mean and standard deviation for each group
group_stats = []
for group in groups:
    group_name, group_values = group
    group_data = data[[f"{group_name}_{value}_rating" for value in group_values]]
    group_mean = group_data.mean()
    group_std = group_data.std()
    group_stats.append((group_name, group_values, group_mean, group_std))

# Create a figure with subplots for each group
fig, axes = plt.subplots(nrows=len(groups), ncols=1, figsize=(8, 20))

# Plot each group on a separate subplot
for i, (group_name, group_values, group_mean, group_std) in enumerate(group_stats):
    ax = axes[i]
    ax.bar(group_values, group_mean, yerr=group_std, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_title(f"Group: {group_name.capitalize()}")
    ax.set_ylabel("Rating")
    ax.set_ylim([0, 10])

plt.tight_layout()
plt.show()
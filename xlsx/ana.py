import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import kstest_normal
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import reportlab

# Import the data
data = pd.read_excel('Survey.xlsx', sheet_name='1')
# Renaming the columns
column_names = ['timestamp', 'age_18_or_older', 'comfortable_with_horror', 'purpose_understanding', 'age', 'gender', 'horror_gaming_experience']

# Add monster column names
for size in ['human', 'colossal']:
    for shape in ['humanoid', 'quadruped']:
        for color in ['black', 'white', 'red', 'blue', 'yellow']:
            for semantic in ['ghosty', 'devil', 'evil']:
                column_names.append(f"{size}_{shape}_{color}_{semantic}_rating")

column_names.append('email')

# Set the new column names
data.columns = column_names

print(data.head())

# Calculate the mean and standard deviation
mean_std_data = []
for col in data.columns[7:-1]:  # Exclude non-rating columns (the first 7 columns and the last one)
    mean_std_data.append((col, data[col].mean(), data[col].std()))

# Melt the data into long format
data_long = data.melt(id_vars=['timestamp', 'age_18_or_older', 'comfortable_with_horror',
                               'purpose_understanding', 'age', 'gender', 'horror_gaming_experience', 'email'],
                      var_name='monster', value_name='rating')

# Extract factors from the 'monster' column
split_monster = data_long['monster'].str.split('_', expand=True)

# Assign only the first four columns from the split data to the new columns
data_long[['size', 'shape', 'color', 'semantic']] = split_monster.iloc[:, :4]

# Run the Linear Mixed-Effects Model
model_formula = "rating ~ C(size) * C(shape) * C(color) * C(semantic)"
mixed_model = smf.mixedlm(model_formula, data_long, groups=data_long['timestamp'], re_formula="~C(size)")
mixed_result = mixed_model.fit()

a = mixed_result.summary()
# Print the results
print(mixed_result.summary())




# Check the assumptions
# Normality
_, pvalue_normality = kstest_normal(mixed_result.resid)
print(f"Normality p-value: {pvalue_normality}")

# Homoscedasticity
# You can use Levene's or Bartlett's test, but they require balanced data (equal group sizes)
# Alternatively, you can visualize residuals vs. fitted values using a scatter plot
plt.scatter(mixed_result.fittedvalues, mixed_result.resid)
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted Values")
plt.show()


data_long.to_csv('h.csv')

# Main effects
size_tukey = pairwise_tukeyhsd(data_long['rating'], data_long['size']).summary()
shape_tukey = pairwise_tukeyhsd(data_long['rating'], data_long['shape']).summary()
color_tukey = pairwise_tukeyhsd(data_long['rating'], data_long['color']).summary()
semantic_tukey = pairwise_tukeyhsd(data_long['rating'], data_long['semantic']).summary()

print("Size Tukey HSD results:")
print(size_tukey)
print("\nShape Tukey HSD results:")
print(shape_tukey)
print("\nColor Tukey HSD results:")
print(color_tukey)
print("\nSemantic Tukey HSD results:")
print(semantic_tukey)

# 计算每个组合的平均评级
heatmap_data = data_long.groupby(['size', 'shape', 'color', 'semantic']).rating.mean().reset_index()

# 选择两个主要因素（例如，大小和形状）作为行和列
heatmap_data_pivot = heatmap_data.pivot_table(values='rating', index=['size', 'shape'], columns=['color', 'semantic'])

# 创建热力图
plt.figure(figsize=(25, 10))  # 修改这里以调整图形的宽度和高度
heatmap = sns.heatmap(heatmap_data_pivot, annot=True, cmap='coolwarm', fmt='.2f',
                      cbar_kws={'label': 'Mean Rating',},
                      annot_kws={'fontweight': 'bold', 'fontsize': 20, 'rotation': 0})  # 修改这里以调整文本方向和字体大小
plt.title('Mean Ratings Heatmap', fontsize=32)
plt.show()

# 转换heatmap到csv
heatmap_data_pivot.to_csv('heatmap.csv')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
from scipy.stats import linregress

# 读取 Excel 文件
survey_data = pd.read_excel('survey_responses.xlsx')

# 筛选 WHZ 的数据
whz_data = survey_data[survey_data['User'] == 'WHZ']

# 提取所需信息
total_time_str = whz_data['Total time'].values[0]
room1_time_str = whz_data['ROOM1'].values[0]
hall_time_str = whz_data['Hall'].values[0]
room2_time_str = whz_data['ROOM2'].values[0]
room3_time_str = whz_data['ROOM3'].values[0]
resting_hr = whz_data['resting heart rate'].values[0]

def str_to_timedelta(time_obj):
    return timedelta(minutes=time_obj.minute, seconds=time_obj.second)

total_time = str_to_timedelta(total_time_str)
room1_time = str_to_timedelta(room1_time_str)
hall_time = str_to_timedelta(hall_time_str)
room2_time = str_to_timedelta(room2_time_str)
room3_time = str_to_timedelta(room3_time_str)


# 读取 CSV 文件
data = pd.read_csv('gaming_whz.csv')

# 将 Timestamp 列转换为 datetime 类型
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# 根据 Total time 截取数据
start_time = data['Timestamp'].iloc[0]
end_time = start_time + total_time
data = data[(data['Timestamp'] >= start_time) & (data['Timestamp'] <= end_time)]

# 设置图表大小
plt.figure(figsize=(15, 6))

# 绘制心率折线图
plt.plot(data['Timestamp'], data['Heart_rate'], label='Heart Rate', marker='o', linestyle='-', linewidth=1)

# 绘制竖线和横线
room1_end_time = start_time + room1_time
hall_end_time = room1_end_time + hall_time
room2_end_time = hall_end_time + room2_time
room3_end_time = room2_end_time + room3_time

plt.axvline(x=room1_end_time, color='r', linestyle='--', label='End of ROOM1')
plt.axvline(x=hall_end_time, color='g', linestyle='--', label='End of Hall')
plt.axvline(x=room2_end_time, color='b', linestyle='--', label='End of ROOM2')
plt.axvline(x=room3_end_time, color='y', linestyle='--', label='End of ROOM3')

plt.axhline(y=resting_hr, color='m', linestyle='--', label='Resting Heart Rate')

# 计算每段时间的平均心率
room1_hr_mean = data[(data['Timestamp'] >=start_time) & (data['Timestamp'] <= room1_end_time)]['Heart_rate'].mean()
hall_hr_mean = data[(data['Timestamp'] > room1_end_time) & (data['Timestamp'] <= hall_end_time)]['Heart_rate'].mean()
room2_hr_mean = data[(data['Timestamp'] > hall_end_time) & (data['Timestamp'] <= room2_end_time)]['Heart_rate'].mean()
room3_hr_mean = data[(data['Timestamp'] > room2_end_time) & (data['Timestamp'] <= room3_end_time)]['Heart_rate'].mean()

print("Average heart rate in ROOM1:", room1_hr_mean)
print("Average heart rate in Hall:", hall_hr_mean)
print("Average heart rate in ROOM2:", room2_hr_mean)
print("Average heart rate in ROOM3:", room3_hr_mean)

# 计算横线上的时间和横线下时间占比
above_line_time = data[data['Heart_rate'] > resting_hr]['Timestamp'].count() * (data['Timestamp'][1] - data['Timestamp'][0]).seconds
below_line_time = data[data['Heart_rate'] <= resting_hr]['Timestamp'].count() * (data['Timestamp'][1] - data['Timestamp'][0]).seconds
total_seconds = (end_time - start_time).seconds

above_line_ratio = above_line_time / total_seconds * 100
below_line_ratio = below_line_time / total_seconds * 100

print(f"Time above resting heart rate: {above_line_ratio:.2f}%")
print(f"Time below resting heart rate: {below_line_ratio:.2f}%")



# 显示最高最低心率
max_hr_idx = data['Heart_rate'].idxmax()
min_hr_idx = data['Heart_rate'].idxmin()
plt.scatter(data.loc[max_hr_idx, 'Timestamp'], data.loc[max_hr_idx, 'Heart_rate'], marker='*', color='k', s=100, label='Max Heart Rate')
plt.scatter(data.loc[min_hr_idx, 'Timestamp'], data.loc[min_hr_idx, 'Heart_rate'], marker='D', color='k', s=100, label='Min Heart Rate')


# 添加次要的y轴
ax2 = plt.gca().twinx()
ax2.plot(data['Timestamp'], (data['Heart_rate'] - resting_hr) / resting_hr * 100, linestyle='--', linewidth=0.5)
ax2.set_ylabel('Heart Rate Change from Resting HR (%)')

# 设置图表标题和轴标签
plt.title('Heart Rate Data')
plt.xlabel('Timestamp')
plt.ylabel('Heart Rate (BPM)')

# 显示图例
plt.legend()

# 自动调整 x 轴刻度标签的显示角度，避免重叠
plt.xticks(rotation=45)

# 显示图表
plt.show()


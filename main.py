from data_preprocess import pre_process
import pandas as pd
import matplotlib.pyplot as plt
df = pre_process(csv_data_file_path='./Data/Bill_Bryson_Data.csv', resample_period='H')
print(len(df) / 24)
df = df.iloc[100:-200]
df.plot()
plt.show()



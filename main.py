import pandas as pd
import pmdarima as pmd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

df = pd.read_csv("./bbtable_data.csv")
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])  # Data in 10 minute intervals
df.set_index('Datetime', inplace=True)
df.drop(columns=['Date', 'Time'], inplace=True)
df_hour = df['Count'].resample('H').mean()
rows_with_na = df_hour[df_hour.isna()]
df_hour.dropna()
# Not a long term solution to .dropna(), fill with mean? or prev weeks?

x = len(df_hour) - 800  # Getting rid of the irrelevant holiday data
df_hour = df_hour.iloc[:x]

# Auto ARIMA model fitting
"""results_auto_arima = pmd.auto_arima(df['Count'],
                                     start_p=0,
                                     start_d=0,
                                     start_q=0,
                                     max_p=2,
                                     max_d=2,
                                     max_q=2,
                                     trend='c',
                                     information_criterion='aic',
                                     trace=True,
                                     error_action='ignore')
"""
# using result from auto.arima
mod = SARIMAX(endog=df_hour,
              order=(2, 0, 2),
              trend='c')
results_manual_sarima = mod.fit()

plt.plot(df_hour[-256:], label='Actual')
pred_period = 7 * 24

predicted = results_manual_sarima.get_prediction(start=-(pred_period))  # Predictions for the last 100 time units
plt.plot(predicted.predicted_mean, label='Predicted', linestyle='dashed')

plt.legend()
plt.show()

actual_values = df_hour[-pred_period:].dropna()
predicted_mean = predicted.predicted_mean.dropna()

# Calculate Mean Squared Error (MSE)
mse = mean_squared_error(actual_values, predicted_mean)
print("Mean Squared Error (MSE):", mse)

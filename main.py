from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from sarimax import pre_process
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sarimax import find_parameters, sarimax_apply


df1 = pre_process(csv_data_file_path='Data/Data_AWS_141223', resample_period='H')
#find_parameters(df1, col='Total')

sarimax_apply(df=df1, pred_period=72, forecast_periods=72, cut_off=250, order=(1,0,1), seasonal_order=(1, 0, 2, 24))



#rmse 8.24938973897547
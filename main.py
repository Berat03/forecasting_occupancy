from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from sarimax import pre_process
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sarimax import find_parameters, sarimax_apply


df1 = pre_process(csv_data_file_path='Data/Data_AWS_141223', resample_period='H')
find_parameters(df1, col='Total')

#sarimax_apply(df=df1, pred_period=72, forecast_periods=72, cut_off=250, order=(4,0,4), seasonal_order=(1, 0, 1, 24))

def acf_plots(df, col='Total', m=24):
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))

    plot_acf(df[col], ax=axes[0, 0], title='ACF - Original')
    plot_pacf(df[col], ax=axes[0, 1], title='PACF - Original')

    df_diff = df.diff().dropna()
    plot_acf(df_diff[col], ax=axes[1, 0], title='ACF - Differenced')
    plot_pacf(df_diff[col], ax=axes[1, 1], title='PACF - Differenced')
    df_diff_season = df.diff(m).dropna()

    plot_acf(df_diff_season[col], ax=axes[2, 0], title='ACF - Seasonally Differenced')
    plot_pacf(df_diff_season[col], ax=axes[2, 1], title='PACF - Seasonal;y Differenced')
    plt.tight_layout()
    plt.show()
def seasonal_plot(df):
    fig = seasonal_decompose(df).plot()
    fig.set_size_inches((16, 9))
    fig.tight_layout()
    plt.show()

#rmse 8.24938973897547
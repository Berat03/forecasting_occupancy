from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from sarimax import pre_process
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sarimax import find_parameters, sarimax_apply
from statsmodels.tools.eval_measures import rmse


df1 = pre_process(csv_data_file_path='./Data/Bill_Bryson_Data.csv', resample_period='H')
#sarimax_apply(df=df1, pred_period=300, forecast_periods=100, cut_off=200, order=(1,0,0), seasonal_order=(1, 0, 0, 24))

find_parameters(df=df1, col='Total', cut_off=200, exog_var='Weekend')


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

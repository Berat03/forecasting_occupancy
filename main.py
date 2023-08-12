from sarimax import pre_process, sarimax_apply, find_parameters


df1 = pre_process(csv_data_file_path='./Data/Bill_Bryson_Data.csv', resample_period='H')
sarimax_apply(df=df1, pred_period=300, forecast_periods=100, cut_off=100)

#find_parameters(df=df1, col='Total', cut_off=0, exog_var='Weekend')


"""Calculate Mean Squared Error (MSE)
"""

# Forecasting Library Occupancy

This project tracks and forecasts the occupancy of Durham Unviersity Bill Bryson Library using a SARIMAX model. 

### Method
Data is webscraped and stored using AWS. Currently using a SARIMAX model, implemented with the statsmodel and pmdarima packages.

### Progress
Currently progress with prediction and forecasting...

![img](https://github.com/Berat03/SARIMAX/assets/83041608/7e5f35c3-61dd-4bc7-8b1f-99b19549e7a2)

- Need to implement term/holiday/exam exogenous variables (currently only dow).
- Need to collect more data.
- Need to begin creating back-end to connect with DynamoDB table.
- 
### Prerequistites 

### Future Plans

Not enough data to be confident in the performance of the model during term time (as most of the data is from the end of exams and holidays), so we to wait till the 2024/25 academic year begins to collect more. Also, having more data will enable the occpurtunity to other mdoels such as LTSM or Facebook Prophet, which are require more data than currently available.

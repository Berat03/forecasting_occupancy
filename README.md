# Forecasting Library Occupancy

This project tracks and forecasts the occupancy of Durham Unviersity Bill Bryson Library. 

### Progress
Currently progress with prediction and forecasting...

![img](https://github.com/Berat03/SARIMAX/assets/83041608/7e5f35c3-61dd-4bc7-8b1f-99b19549e7a2)

- Need to implement term/holiday/exam exogenous variables (currently only using day of the week).
  - Need to wait for term to start, as I almost have entirely holiday data.
- Need to collect more data.
  - Potentially use different forecasting models?
- Unsure connect with DynamoDB table to backend **cost-effectively**.
  - S3? Amplify? EB?

### Prerequistites 

### Future Plans

Not enough data to be confident in the performance of the model during term time (as most of the data is from the end of exams and holidays), so have to wait till the academic year begins to collect more. Having more data (and more varied) will enable the opportunity to try other models such as LTSM or Facebook Prophet (which are require more data than currently available).

# SekaiBorderPrediction
A Python program for predicting Project Sekai event borders with limited amount of data provided.

## For example
It's known that:
> * The 90th event is started on 30th Mar. and will end on 9th Apr..
> * At 21:18(BJS, GMT+8) 4th Apr. the 100th on the event ranking has 38274002pt. 
> * At 14:54(BJS, GMT+8) 5th Apr. the 100th on the event ranking has 41786890pt.

To predict the final border of 100th, which is the cumulative point the 100th player will get throughout the event, the code will be as follows:
```
Predictor = Predictor(datetime.date(year=2023, month=3, day=30), datetime.date(year=2023, month=4, day=9))
data = {datetime.datetime(year=2023, month=4, day=4, hour=13, minute=18): 38274002,
        datetime.datetime(year=2023, month=4, day=5, hour=6, minute=54): 41786890}
print(Predictor.predict(data, "100"))
```
And the output is:
```
78786672.6225009
```
Which means that the final 100th-border of the 90th event will be around 78.8 million(In fact the border is 80.0 million, which means a relative error of 1.5%).

Then, suppose that we want to predict the border value of 100th at 15:07(BJS, GMT+8) 7th Apr.. The code will be as follows:
```
now = datetime.datetime(year=2023, month=4, day=7, hour=7, minute=7)
print(Predictor.specifiedTimePrediction(now, data, "100"))
```
And the output is:
```
56383723.81583737
```

## Note:
The Japanese Feasts included in the code is based on relevant Japanese laws up to now(2023). If the laws change, the code will need to be changed too.
The "IsEquinox" function only has equinoxes up to 2025.

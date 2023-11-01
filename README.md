# SekaiBorderPrediction
A Python program for predicting Project Sekai event borders with limited amount of data provided.

## For example
It's known that:
> * The 90th event is started on 30th Mar. and will end on 9th Apr..
> * At 21:18(BJS, GMT+8) 4th Apr. the 100th on the event ranking has 38274002pt. 
> * At 14:54(BJS, GMT+8) 5th Apr. the 100th on the event ranking has 41786890pt.

To predict the final border of 100th, the code will be as follows:
```
print(predict(datetime.date(year=2023, month=3, day=30),
              datetime.date(year=2023, month=4, day=9),
              {
                  datetime.datetime(year=2023, month=4, day=4, hour=13, minute=18): 38274002,
                  datetime.datetime(year=2023, month=4, day=5, hour=6, minute=54): 41786890
              },
              '100'))
```
And the output is:
```
2023-04-04 21:18:00(BJS): 38274002 → 预测 = 80628397
2023-04-05 14:54:00(BJS): 41786890 → 预测 = 77674661
78786672.6225009
```
Which means the final 100th-border of the 90th event will be around 78.8 million.

## Note:
The Japanese Feasts included in the code is based on relevant Japanese laws up to now(2023). If the laws change, the code will need to be changed too.
The "IsEquinox" function only has equinoxes up to 2025.

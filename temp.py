import datetime
cashedData={"date":"2019-10-28 18:54:11.391745"}
print((datetime.datetime.now()-datetime.datetime.strptime(cashedData["date"], '%Y-%m-%d %H:%M:%S.%f')).total_seconds()<30)

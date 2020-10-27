from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360,timeout=(10,25))
kw_list = ["Blockchain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
pytrends.interest_over_time()

#from library import BuyLiquidateAlgo, SMAAlgo
from pylgo.data_loader.loader import BitfinexLoaderAPI
#algorithm = SMAAlgo(['BTCUSD', 'ETHUSD'], 'Bitfinex', '1h',
#                    '2021-12-01 06:00:00', '2022-01-01 10:00:00', 'logs', 'reports', 10_000)
#algorithm.run()
s = BitfinexLoaderAPI(symbol='tBTCUSD', start_date="2022-01-01 00:00:00", end_date="2022-07-07 00:10:00")
s.get_data()
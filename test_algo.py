from library import LSTMAlgo
# from pylgo.data_loader.loader import BitfinexLoaderAPI
algorithm = LSTMAlgo(['BTCUSD'], 'Bitfinex', 'd',
                     '2022-03-11 00:00:00', '2022-08-20 00:00:00', 'logs', 'reports', 10_000)
algorithm.run()
# s = BitfinexLoaderAPI(
#     symbol='tBTCUSD', start_date="2022-01-01 00:00:00", end_date="2022-07-07 00:10:00")
# s.get_data()

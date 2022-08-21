from library import LSTMAlgo
algorithm = LSTMAlgo(['BTCUSD'], 'Bitfinex', 'd',
                     '2022-03-11 00:00:00', '2022-08-20 00:00:00', 'logs', 'reports', 10_000)
algorithm.run()

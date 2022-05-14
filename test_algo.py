from library import HODL
algorithm = HODL('BTCUSD', 'Bitfinex', '1h',
                 '2022-01-01 06:00:00', '2022-01-01 06:00:00', 'reports', 10_000)
algorithm.run()

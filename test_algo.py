from library import BuyLiquidateAlgo, SMAAlgo
algorithm = SMAAlgo(['BTCUSD', 'ETHUSD'], 'Bitfinex', '1h',
                    '2021-12-01 06:00:00', '2022-01-01 10:00:00', 'logs', 'reports', 10_000)
algorithm.run()

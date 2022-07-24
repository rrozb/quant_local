from library import BuyLiquidateAlgo, SMAAlgo
algorithm = SMAAlgo(['BTCUSD', 'ETHUSD'], 'Bitfinex', '1h',
                    '2021-12-01 06:00:00', '2022-02-10 10:00:00', 'reports', 10_000)
algorithm.run()

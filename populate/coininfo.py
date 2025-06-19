from populate.common import load_app_env

load_app_env()

from src.cronjobs.update_binance_coins_info.update_binance_coins_info import Controller

def populate_coin_info():
    controller = Controller()

    controller.execute()
    
    print('Populated coins info')
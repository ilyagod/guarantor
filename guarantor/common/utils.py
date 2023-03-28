import json
import os

from tronpy import Tron

from guarantor.settings import settings


def populate_main_wallet_setting() -> None:
    file_path = os.path.join(os.path.dirname(__file__), "main_wallet.json")
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            main_wallet_config = json.loads(f.read())
    else:
        client = Tron(network=settings.payments_tron_network)
        main_wallet_config = client.generate_address()
        with open(file_path, "w") as f:
            json.dump(main_wallet_config, f)

    settings.payments_tron_main_wallet_config = main_wallet_config

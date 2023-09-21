import shodan
import json
import logging
import argparse

CONFIG_FILE = 'api_keys.json'

class ShodanAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api = shodan.Shodan(api_key)

    def get_account_info(self):
        try:
            account_info = self.api.info()
            usage_total = account_info.get('usage', {}).get('usage_total')
            scan_credits = account_info.get('usage', {}).get('scan_credits')
            return {
                'API Key': self.api_key,
                'Account usage': usage_total,
                'Scan credits': scan_credits
            }
        except shodan.APIError as e:
            return {
                'API Key': self.api_key,
                'Error': str(e)
            }

def read_api_keys(config_file):
    with open(config_file) as f:
        config = json.load(f)
        return config.get('api_keys', [])

def main():
    parser = argparse.ArgumentParser(description='Retrieve Shodan account information.')
    parser.add_argument('--config', default=CONFIG_FILE, help='Configuration file path')
    args = parser.parse_args()

    api_keys = read_api_keys(args.config)

    for api_key in api_keys:
        shodan_api = ShodanAPI(api_key)
        account_info = shodan_api.get_account_info()
        print(account_info)

if __name__ == '__main__':
    logging.basicConfig(filename='shodan_api.log', level=logging.INFO)
    main()

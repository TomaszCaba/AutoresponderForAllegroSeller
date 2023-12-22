import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('client_id', type=str)
parser.add_argument('client_secret', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    app_info = f'{{"CLIENT_ID": "{args.client_id}",\n"CLIENT_SECRET": "{args.client_secret}", \n"ROOT_DIR": "{os.getcwd()}"}}'
    with open('app_info.json', 'w') as f:
        f.write(app_info)

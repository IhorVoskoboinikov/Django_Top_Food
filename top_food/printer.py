import argparse
import time
import requests


parser = argparse.ArgumentParser()
parser.add_argument('-id', '--id', type=int, help='Printer operation')
args = parser.parse_args()
print(f'Принтер работает')
print(args.id)


while True:
    response = requests.get(f'http://127.0.0.1:8000/get_files_for_printer/{args.id}')
    time.sleep(5)
    print(response)
    print(response.json())


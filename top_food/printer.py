import argparse
import time
import requests


parser = argparse.ArgumentParser()
parser.add_argument('--printer_id', type=int)
args = parser.parse_args()

print(f'Printer {args.printer_id} is working!')

while True:
    response = requests.get(f'http://127.0.0.1:8000/get_files_for_printer/{args.printer_id}')
    time.sleep(5)

    print(response)

    for check in response.json().keys():

        if check == 'check':
            print('No checks to print')

        else:
            print(f'New check # {check} found. printing…')

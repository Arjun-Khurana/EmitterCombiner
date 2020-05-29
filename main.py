import pandas as pd
import numpy as np
import sys
import os
from tqdm import tqdm
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputDir', \
    help='Directory where input CSVs are located')
parser.add_argument('-a', '--appended', \
    help='Outputs intensity data as columns in MegaCSV',
    action='store_true')
parser.add_argument('-s', '--separated', \
    help='Outputs intensity data as separate CSV',
    action='store_true')
args = parser.parse_args()

def fileparse(filename):
    split = (filename.replace('.csv','').split())
    wafer = split[1]
    pulse = split[2]
    duty = split[3]
    current = split[4]
    temp = split[5]
    pos = split[6].split('X')
    pos = pos[len(pos)-1]
    pos = pos.split('Y')
    posX = pos[0]
    posY = pos[1]
    return {
        'wafer': wafer,
        'pulse': pulse,
        'duty': duty,
        'current': current,
        'temp': temp,
        'posX': posX,
        'posY': posY
    }

def stdDev(intensity):
    return {
        'count': len(intensity),
        'sum': np.sum(intensity),
        'mean': np.mean(intensity),
        'sigma': np.std(intensity)
    }

dfs = []
std = pd.DataFrame(columns=['posX', 'posY', 'count', 'sum', 'mean', 'sigma'])

for file in tqdm(os.listdir(args.inputDir)):
    if file.endswith('.csv'):
        filename = os.path.join(args.inputDir, file)
        df = pd.read_csv(filename, header=7, index_col=0)
        df['filename'] = file
        info = fileparse(file)
        for key in info:
            df[key] = info[key]

        dev = stdDev(df['Total Intensity'])

        if args.appended:
            for key in dev:
                df[key] = dev[key]
        if args.separated:
            dev.update(info)
            std = std.append(dev, ignore_index=True)
            pass

        dfs.append(df)

mega = pd.concat(dfs)

if not os.path.exists('outputs'):
    os.mkdir('outputs')

now = datetime.datetime.now()
if args.appended:
    mega.to_csv('outputs/EmitterDataStdDev-' + now.strftime('%m-%d--%H-%M-%S') + '.csv')
else:
    mega.to_csv('outputs/EmitterData-' + now.strftime('%m-%d--%H-%M-%S') + '.csv')

if args.separated:
    std.to_csv('outputs/StdDev-' + now.strftime('%m-%d--%H-%M-%S') + '.csv', index=False)
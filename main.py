import pandas as pd
import sys
import os

dfs = []

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

def rowAdd(row, file, info):
    row['filename'] = file
    row['wafer'] = info['wafer']

for file in os.listdir(sys.argv[1]):
    if file.endswith('.csv'):
        filename = os.path.join(sys.argv[1], file)
        info = fileparse(file)
        df = pd.read_csv(filename, header=7, index_col=0)
        df['filename'] = file
        for key in info:
            df[key] = info[key]
        dfs.append(df)

mega = pd.concat(dfs)

if not os.path.exists('megacsv'):
    os.mkdir('megacsv')

mega.to_csv('megacsv/output.csv')
print('done')
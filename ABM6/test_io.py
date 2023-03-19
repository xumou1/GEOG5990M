import csv
import numpy as np

# Read input data
def read_data():
    f = open('C:/Users/dell/Desktop/leeds/GEOG5990M/ABM5/in.txt', newline='')
    data = []
    for line in csv.reader(f, quoting=csv.QUOTE_NONNUMERIC):
        row = []
        for value in line:
            row.append(value)
            #print(value)
        data.append(row)
    f.close()
    n_rows, n_cols = np.shape(data)
    return data, n_rows, n_cols
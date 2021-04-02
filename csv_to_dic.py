import csv

with open('datasets/symbols.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('stock_list.py', mode='w') as outfile:
        writer = csv.writer(outfile)
        mydict = {rows[0]:rows[1] for rows in reader}
print(mydict)

import csv

data = []
with open('import/year.csv') as f:
    csv_r = csv.reader(f)
    next(csv_r)
    count = 0
    for row in csv_r:
        if count % 2 == 1:
            data.append(row[1])
        count += 1
    data = set(data)
    with open('year.txt', 'w', encoding='utf-8') as f:
        for d in data:
            f.write(d + '\n')

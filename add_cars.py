from application import db, Car
import csv

meta = db.metadata
for table in reversed(meta.sorted_tables):
    if(table.name=='car'):
        db.session.execute(table.delete())
        print("truncated Car")
db.session.commit()

with open('static/vehicles.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    columns = {}
    for row in csv_reader:
        if line_count == 0:
            col = 0
            for column in row:
                columns[column] = col
                col += 1
        else:
            if (line_count % 100 == 0):
                print(line_count)
            car = Car(
                id=row[columns['id']],
                make=row[columns['make']],
                model=row[columns['model']],
                year=row[columns['year']],
                mileage=row[columns['comb08']],
            )
            db.session.add(car)
            db.session.commit()
        line_count += 1

    print(f'Processed {line_count} lines.')

    #print (columns)

peter = Car.query.filter_by(make='Tesla', model='1', year=2017).first()
print (peter)
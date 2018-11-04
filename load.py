import csv
from application import db, Place

    with open('place.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        columns = {}
        for row in csv_reader:  # iterate each row
            if line_count == 0:  # handles the header
                col = 0
                for column in row:
                    columns[column] = col
                    col += 1
            else:
                if (line_count % 100 == 0):
                    print(line_count)  # utility, tells the progress
                is_electric = 0
                actual_mileage = row[columns['comb08']]
                if row[columns['combE']] > 0:
                    is_electric = 1
                    actual_mileage = row[columns['combE']]

            print(row[-2])

            # object to be added
            # city, state_id, state_name, county_fips, county_name, "lat","lng","zips","id"
            place = Place(
                id=row[-1],
                city=row[0],
                state_id=row[2],
                state_name=row[3],
                county_fips=row[4],
                county_name=row[5],
                lat=row[6],
                lng=row[7],
                zips=row[-2]
            )

            # commands to add the object
            db.session.add(place)
            db.session.commit()
            line_count += 1

        print(f'Processed {line_count} lines.')

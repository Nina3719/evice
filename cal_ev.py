from application import db, Car, Post

evs = Car.query.filter(Car.kwh != "0.0").all()

length = len(evs)

print(length)

kwh = 0
mileage = 0

for ev in evs:
    kwh += float(ev.kwh)
    mileage += float(ev.mileage)

kwh /= length
mileage /= length

print(kwh)
print(mileage)

our_ev = Car(id=99999, make="Average EV", model="Average EV", year=2018, mileage=70, kwh=40)

#Post.__table__.drop(db.engine)
#db.create_all()
#db.session.delete(our_ev)
#db.session.add(our_ev)
#db.session.commit()
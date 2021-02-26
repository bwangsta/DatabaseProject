import pymysql


def cheapest_flight(cur):
    # departure_code = input('Please enter airport code for the departure airport: ')
    # arrival_code = input('Please enter the airport code for the destination airport: ')
    # date = input('What is the date of the flight in yyyy-mm-dd? ')
    departure_code = 'SCK'
    arrival_code = 'IWA'
    date = '2018-02-03'

    sql = """SELECT flight_number, MIN(amount) 
            FROM fare NATURAL JOIN leg_instance 
            WHERE departure_airport_code = %s AND arrival_airport_code = %s AND leg_date = %s;"""

    cur.execute(sql, (departure_code, arrival_code, date))
    
    for flight_num, fare in cur.fetchall():
        print(f'The cheapest flight is {flight_num}, and the cost is ${fare}')


def flight_seat_info(cur):
    # name = input("Please enter the customer's name: ")
    name = 'Ryan'

    sql = """SELECT flight_number, seat_number
            FROM seat_reservation
            WHERE customer_name = %s;"""

    cur.execute(sql, (name))

    for flight_num, seat_num in cur.fetchall():
        print(f'The flight number is {flight_num}, and the seat number is {seat_num}')


def nonstop_flights(cur):
    # Find all non-stop flights for an airline.
    airline = 'Allegiant'

    sql = """SELECT flight_number
            FROM flight NATURAL JOIN leg_instance
            WHERE leg_number = 1 AND airline = %s"""
    
    cur.execute(sql, (airline))

    for flight_num in cur.fetchall():
        print(f'The non-stop flights are: {flight_num[0]}')


def add_airplane(db, cur):
    # Add a new airplane.
    total_seats = 400
    airplane_type = 'B317'

    sql1 = """INSERT INTO airplane
            VALUES(DEFAULT, %s, %s)"""
    
    cur.execute(sql1, (total_seats, airplane_type))
    db.commit()

    sql2 = """SELECT airplane_id
            FROM airplane
            WHERE total_number_of_seats = %s AND airplane_type = %s;"""

    cur.execute(sql2, (total_seats, airplane_type))

    for id in cur.fetchall():
        print(f'The new airplane has been added with id: {id}')


if __name__ == "__main__":
    db = pymysql.connect(host='localhost', user='mp2',
                         passwd='Eeecs116', db='flights')

    cur = db.cursor()
    cheapest_flight(cur)
    flight_seat_info(cur)
    nonstop_flights(cur)
    add_airplane(db, cur)

    db.close()

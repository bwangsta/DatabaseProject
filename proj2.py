import pymysql

def cheapest_flight(cur):
    departure_code = input('Please enter airport code for the departure airport: ')
    arrival_code = input('Please enter the airport code for the destination airport: ')
    date = input('What is the date of the flight in yyyy-mm-dd? ')

    sql = """SELECT flight_number, MIN(amount) 
            FROM fare NATURAL JOIN leg_instance 
            WHERE departure_airport_code = %s AND arrival_airport_code = %s AND leg_date = %s
            GROUP BY flight_number
            LIMIT 1;"""

    cur.execute(sql, (departure_code, arrival_code, date))
    
    for flight_num, fare in cur.fetchall():
        print(f'The cheapest flight is {flight_num}, and the cost is ${fare}')


def flight_seat_info(cur):
    name = input("Please enter the customer's name: ")

    sql = """SELECT flight_number, seat_number
            FROM seat_reservation
            WHERE customer_name = %s;"""

    cur.execute(sql, (name))

    for flight_num, seat_num in cur.fetchall():
        print(f'The flight number is {flight_num}, and the seat number is {seat_num}')


def nonstop_flights(cur):
    # Find all non-stop flights for an airline.
    airline = input('What is the name of the airline? ')

    sql = """SELECT flight_number, COUNT(leg_number) AS total_legs
            FROM flight NATURAL JOIN leg_instance
            WHERE airline = %s
            GROUP BY flight_number, leg_date
            HAVING total_legs = 1;"""
    
    cur.execute(sql, (airline))

    flightlist = []
    print('The non-stop flights are: ', end='')
    for flightnum, _ in cur.fetchall():
        flightlist.append(flightnum)
    print(', '.join(flightlist))


def add_airplane(db, cur):
    # Add a new airplane.
    # total_seats = input('Please enter the total number of seats: ')
    # airplane_type = input('Please enter the airplane type: ')
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

    print(f'The new airplane has been added with id: {cur.fetchone()[0]}')


def increase_fares(cur):
    factor = input('Please enter a factor (e.g. 0.2 will increase all fares by 20%): ')
    factor = str(float(0.2) + 1)

    sql1 = """SELECT flight_number
            FROM fare
            WHERE amount <= 200;"""

    cur.execute(sql1)
    num_updated = len(cur.fetchall())

    sql2 = """UPDATE fare
            SET amount = amount * %s
            WHERE amount <= 200"""

    cur.execute(sql2, (factor))
    db.commit()

    print(f'{num_updated} fares are affected.')


def remove_reservation(cur):
    flightnum = input('Please enter the flight number: ')
    name = input('Please enter the customer name: ')

    sql1 = """SELECT seat_number
            FROM seat_reservation
            WHERE flight_number = %s AND customer_name = %s"""

    cur.execute(sql1, (flightnum, name))
    seatnum = cur.fetchone()[0]

    sql2 = """DELETE seat_reservation
            WHERE flight_number = %s AND customer_name = %s"""

    cur.execute(sql2, (flightnum, name))
    db.commit()

    print(f'Seat {seatnum} is released.')

# def main():
#     while True:
#         query_choice = input('Pick a query')

#         if query_choice = 'quit':


if __name__ == "__main__":
    db = pymysql.connect(host='localhost', user='mp2',
                         passwd='Eeecs116', db='flights')

    cur = db.cursor()
    # cheapest_flight(cur)
    # flight_seat_info(cur)
    # nonstop_flights(cur)
    # add_airplane(db, cur)
    # increase_fares(cur)

    db.close()
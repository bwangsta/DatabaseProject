import pymysql

# Query: Find the cheapest flight given airports and a date.
def cheapest_flight(cur):
    departure_code = input('Please enter airport code for the departure airport: ')
    arrival_code = input('Please enter the airport code for the destination airport: ')
    date = input('What is the date of the flight in yyyy-mm-dd? ')

    sql = """SELECT flight_number, MIN(amount) 
            FROM fare NATURAL JOIN leg_instance 
            WHERE departure_airport_code = %s AND arrival_airport_code = %s AND leg_date = %s"""

    cur.execute(sql, (departure_code, arrival_code, date))
    
    for flight_num, fare in cur.fetchall():
        print(f'The cheapest flight is {flight_num}, and the cost is ${fare}')


# Query: Find the flight and seat information for a customer.
def flight_seat_info(cur):
    name = input("Please enter the customer's name: ")

    sql = """SELECT flight_number, seat_number
            FROM seat_reservation
            WHERE customer_name = %s;"""

    cur.execute(sql, (name))

    for flight_num, seat_num in cur.fetchall():
        print(f'The flight number is {flight_num}, and the seat number is {seat_num}')


# Query: Find all non-stop flights for an airline.
def nonstop_flights(cur):
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


# Task: Add a new airplane.
def add_airplane(db, cur):
    # Asks user for number of seats and airplane type
    total_seats = input('Please enter the total number of seats: ')
    airplane_type = input('Please enter the airplane type: ')

    sql1 = """SELECT MAX(airplane_id)
             FROM airplane;"""

    cur.execute(sql1)
    plane_id = cur.fetchone()[0] + 1

    sql2 = """INSERT INTO airplane
            VALUES(%s, %s, %s)"""
    
    cur.execute(sql2, (plane_id, total_seats, airplane_type))
    db.commit()

    sql3 = """SELECT airplane_id
            FROM airplane
            WHERE total_number_of_seats = %s AND airplane_type = %s;"""

    cur.execute(sql3, (total_seats, airplane_type))

    print(f'The new airplane has been added with id: {cur.fetchone()[0]}')


# Increase low-cost fares(≤ 200) by a factor.
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


# Remove a seat reservation.
def remove_reservation(cur):
    flightnum = input('Please enter the flight number: ')
    name = input('Please enter the customer name: ')

    sql1 = """SELECT seat_number
            FROM seat_reservation
            WHERE flight_number = %s AND customer_name = %s"""

    cur.execute(sql1, (flightnum, name))
    seatnum = cur.fetchone()[0]

    sql2 = """DELETE FROM seat_reservation
            WHERE flight_number = %s AND customer_name = %s"""

    cur.execute(sql2, (flightnum, name))
    db.commit()

    print(f'Seat {seatnum} is released.')


def main():
    print('1.) Find the cheapest flight given airports and a date.')
    print('2.) Find the flight and seat information for a customer.')
    print('3.) Find all non-stop flights for an airline.')
    print('4.) Add a new airplane.')
    print('5.) Increase low-cost fares(≤ 200) by a factor.')
    print('6.) Remove a seat reservation.')

    while True:
        choice = input('CHOOSE A QUERY NUMBER (1-6): ').lower()

        if choice == 'quit':
            break
        if choice == '1':
            cheapest_flight(cur)
        elif choice == '2':
            flight_seat_info(cur)
        elif choice == '3':
            nonstop_flights(cur)
        elif choice == '4':
            add_airplane(db, cur)
        elif choice == '5':
            increase_fares(cur)
        elif choice == '6':
            remove_reservation(cur)
        else:
            print('Invalid Input. Please enter a number between 1-6')


if __name__ == "__main__":
    db = pymysql.connect(host='localhost', user='mp2',
                         passwd='eecs116', db='flights')

    cur = db.cursor()

    main()

    db.close()
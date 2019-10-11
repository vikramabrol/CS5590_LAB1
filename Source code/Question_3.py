import numpy as np
import random

# for First Class or Business Class, reserve 1 to 5 rows, economy class for the rest
# for first class or business class, put the price range between 1000 and 2000
# for employees, put price as 0 for economy
# create dictionary with all values, price, seat number, ticket type etc

# Create flight class to enter flight details
class flight:
    def __init__(self, airline_number, origin, destination, date_of_flying):
        self.airline_number = airline_number
        self.origin = origin
        self.destination = destination
        self.date_of_flying = date_of_flying
        self.flight_details = {'airline_number': self.airline_number,
                               'origin': self.origin,
                               'destination': self.destination,
                               'date_of_flying': self.date_of_flying}

# Define a class on ticket where you enter ticket details and calculate price based on ticket type and class
# ask user input on number of seats on the plane
# assign seat based on ticket class and type
class ticket:
    num_seats = int(input("Enter number of seats (multiple of 5) >> "))
    passenger_count = 0
    def __init__(self, ticket_class='Economy', ticket_type='Non_Employee'):
        self.ticket_class = ticket_class
        self.ticket_type = ticket_type
        self.__class__.num_seats -= 1
        self.__class__.passenger_count += 1
    def calculate_price(self):
        ticket_price = 0
        if self.ticket_type != 'Employee':
            if self.ticket_class == 'First_Class':
                ticket_price = 1500
            elif self.ticket_class == 'Business_Class':
                ticket_price = 2000
            elif self.ticket_class == 'Economy':
                ticket_price = 500
        else:
            if self.ticket_class == 'First_Class':
                ticket_price = 1200
            elif self.ticket_class == 'Business_Class':
                ticket_price = 1500
            elif self.ticket_class == 'Economy':
                ticket_price = 0
        return ticket_price

    def assign_seat(self):
        col = np.array(range(int(self.num_seats) // 5))
        # col = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        row = np.array(['A', 'B', 'C', 'D', 'E'])
        all_seats = np.transpose([np.tile(col, len(row)), np.repeat(row, len(col))])
        bc_seats = np.transpose([np.tile(col[:3], len(row)), np.repeat(row, len(col[:3]))])
        fc_seats = np.transpose([np.tile(col[3:6], len(row)), np.repeat(row, len(col[3:6]))])
        economy_seats = np.transpose([np.tile(col[6:], len(row)), np.repeat(row, len(col[6:]))])
        if self.ticket_class == 'First_Class':
            assigned_seat = random.choice(fc_seats)
        elif self.ticket_class == 'Business_Class':
            assigned_seat = random.choice(bc_seats)
        else:
            assigned_seat = random.choice(all_seats)
        new_seats = np.delete(all_seats, np.where(all_seats == assigned_seat))
        remaining_seats = int(self.num_seats) - 1
        seats = {'assigned_seat': assigned_seat,
                      'rem_seats': remaining_seats}
        return seats

    def ticket_details(self):
        tickets = {'ticket_class': self.ticket_class,
                  'ticket_type': self.ticket_type,
                  'ticket_price': self.calculate_price()
                   }
        return tickets
# Implement parent class to inherit from flight and ticket classes
# this class will be used to make the reservation
class passenger(flight, ticket):
    def __init__(self, airline_number, origin, destination, date_of_flying, ticket_class, ticket_type, last_name, first_name):
        flight.__init__(self, airline_number, origin, destination, date_of_flying)
        ticket.__init__(self, ticket_class, ticket_type)
        self.last_name = last_name
        self.first_name = first_name
        self.passenger_details = {'last_name': self.last_name,
                                  'first_name': self.first_name,
                                  'airline_number': self.airline_number,
                                  'origin': self.origin,
                                  'destination': self.destination,
                                  'date': self.date_of_flying,
                                  'assigned_seat': self.assign_seat().get('assigned_seat'),
                                  'ticket_price': self.ticket_details().get('ticket_price')}
        passenger_record = {}
        if self.num_seats != 0:
            passenger_record.update(self.passenger_details)
            print(passenger_record)

    def check_for_tickets(self):
        if self.num_seats != 0:
            self.num_seats -= 1
            return self.num_seats
    def pass_count(self):
        self.passenger_count += 1

#print(ticket.assign_seat(ticket))
pass1 = passenger('A4634', 'STL', 'KC', '2019/11/02', 'Economy', 'Non_Employee', 'Smith', 'John')
pass2 = passenger('A4634', 'ORD', 'KC', '2019/11/02', 'Economy', 'Employee', 'Smith', 'Steve')
pass2 = passenger('A4634', 'ORD', 'KC', '2019/11/02', 'First_Class', 'Non_Employee', 'Smith', 'Sam')
print("Number of passengers booked: " + str(passenger.passenger_count))

print("Number of seats remaining: " + str(passenger.num_seats))
class MenuItem:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


class Menu:
    def __init__(self):
        self.menu_items = []

    def add_item(self, name, description, price):
        item = MenuItem(name, description, price)
        self.menu_items.append(item)

    def remove_item(self, name):
        for item in self.menu_items:
            if item.name == name:
                self.menu_items.remove(item)

    def update_item(self, name, description, price):
        for item in self.menu_items:
            if item.name == name:
                item.description = description
                item.price = price

    def display_menu(self):
        print("Menu:")
        for item in self.menu_items:
            print(f"{item.name}: ${item.price:.2f} - {item.description}")
        print()


class Table:
    def __init__(self, number, seats):
        self.number = number
        self.seats = seats


class Reservation:
    def __init__(self, customer_name, date, time, num_guests, table):
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.num_guests = num_guests
        self.table = table
        self.order = []

    def add_to_order(self, item):
        self.order.append(item)

    def update_order(self, old_item, new_item):
        if old_item in self.order:
            index = self.order.index(old_item)
            self.order[index] = new_item

    def delete_from_order(self, item):
        if item in self.order:
            self.order.remove(item)

    def calculate_total_price(self, menu):
        total_price = sum(item.price for item in self.order)
        return total_price

    def display_order(self, menu):
        print("Order:")
        for item in self.order:
            menu_item = next((menu_item for menu_item in menu.menu_items if menu_item.name == item), None)
            if menu_item:
                print(f"{menu_item.name}: ${menu_item.price:.2f} - {menu_item.description}")
        print(f"Total Price: ${self.calculate_total_price(menu):.2f}")
        print()


class ReservationManager:
    def __init__(self):
        self.reservations = []

    def create_reservation(self, customer_name, date, time, num_guests, table):
        reservation = Reservation(customer_name, date, time, num_guests, table)
        self.reservations.append(reservation)
        return reservation

    def find_reservation(self, table_number, date, time):
        for reservation in self.reservations:
            if (
                reservation.table.number == table_number
                and reservation.date == date
                and reservation.time == time
            ):
                return reservation
        return None

    def update_reservation(self, reservation, new_date, new_time, new_num_guests):
        reservation.date = new_date
        reservation.time = new_time
        reservation.num_guests = new_num_guests

    def delete_reservation(self, reservation):
        self.reservations.remove(reservation)

    def view_all_reservations(self):
        for reservation in self.reservations:
            print(reservation.customer_name, reservation.date, reservation.time, reservation.num_guests)


class Staff:
    def __init__(self, reservation_manager, menu):
        self.reservation_manager = reservation_manager
        self.menu = menu

    def view_menu(self):
        self.menu.display_menu()

    def view_all_reservations(self):
        self.reservation_manager.view_all_reservations()

    def view_reservation_details(self, table_number, date, time):
        reservation = self.reservation_manager.find_reservation(table_number, date, time)
        if reservation:
            reservation.display_order(self.menu)
        else:
            print("No reservation found for the entered details.")

    def update_reservation_details(self, table_number, date, time, new_date, new_time, new_num_guests):
        reservation = self.reservation_manager.find_reservation(table_number, date, time)
        if reservation:
            self.reservation_manager.update_reservation(reservation, new_date, new_time, new_num_guests)
            print("Reservation details updated.")
        else:
            print("No reservation found for the entered details.")

    def cancel_reservation(self, table_number, date, time):
        reservation = self.reservation_manager.find_reservation(table_number, date, time)
        if reservation:
            self.reservation_manager.delete_reservation(reservation)
            print("Reservation canceled.")
        else:
            print("No reservation found for the entered details.")

    def add_new_menu_item(self, name, description, price):
        self.menu.add_item(name, description, price)
        print("Menu item added.")

    def update_menu_item(self, name, description, price):
        self.menu.update_item(name, description, price)
        print("Menu item updated.")

    def delete_menu_item(self, name):
        self.menu.remove_item(name)
        print("Menu item deleted.")


# Initialize Menu
menu = Menu()
# Add 10 default menu items
menu.add_item("Osh", "Samarqand oshi", 10.00)
menu.add_item("Sho'rva", "Tovuq sho'rva", 15.00)
menu.add_item("Kabob", "Namangancha kabob", 8.00)
# Add 7 more meals...

# Initialize ReservationManager
reservation_manager = ReservationManager()

# Initialize Staff
staff = Staff(reservation_manager, menu)

while True:
    print("\n1. Customer")
    print("2. Staff")
    print("3. Exit")

    user_type = input("Enter user type (1/2/3): ")

    if user_type == "1":
        # Customer Section
        while True:
            print("\n1. View menu")
            print("2. Make a reservation")
            print("3. View the restaurant details")
            print("4. Cancel the reservation")
            print("5. View the reservation details")
            print("6. Update the reservation details")
            print("7. Back to main menu")

            customer_choice = input("Enter your choice (1-7): ")

            if customer_choice == "1":
                # View menu
                menu.display_menu()
            elif customer_choice == "2":
                # Make a reservation
                menu.display_menu()
                customer_name = input("Enter your name: ")
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")
                num_guests = int(input("Enter the number of guests: "))

                # Check if the place is available
                table_number = 1  # Placeholder, you may want to implement a logic to assign table numbers
                table = Table(table_number, 4)  # Placeholder for the number of seats
                reservation = reservation_manager.find_reservation(table_number, date, time)

                if reservation:
                    print("This seat is booked.")
                else:
                    print(f"Reserved! Your table number is {table_number}.")

                    # Order food
                    menu.display_menu()
                    order = []

                    # Allow selecting up to 10 meals
                    for _ in range(10):
                        item = input("Enter the item you want to order (type 'done' to finish): ")
                        if item.lower() == 'done':
                            break

                        # Check if the entered item is in the menu
                        if any(menu_item.name.lower() == item.lower() for menu_item in menu.menu_items):
                            order.append(item)
                        else:
                            print("Invalid item. Please enter a valid menu item.")

                    reservation_manager.create_reservation(customer_name, date, time, num_guests,
                                                            table).order = order

                    print("Reservation and order updated:")
                    reservation_manager.find_reservation(table_number, date, time).display_order(menu)
                    break
            elif customer_choice == "3":
                # View the restaurant details
                # Add code to display restaurant details (name, address, phone number, etc.)
                print("Restaurant details: [Add details here]")
            elif customer_choice == "4":
                # Cancel the reservation
                table_number = int(input("Enter your table number: "))
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")

                reservation = reservation_manager.find_reservation(table_number, date, time)

                if reservation:
                    reservation_manager.delete_reservation(reservation)
                    print("Reservation canceled.")
                else:
                    print("No reservation found for the entered details.")
            elif customer_choice == "5":
                # View the reservation details
                table_number = int(input("Enter your table number: "))
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")

                reservation = reservation_manager.find_reservation(table_number, date, time)

                if reservation:
                    reservation.display_order(menu)
                else:
                    print("No reservation found for the entered details.")
            elif customer_choice == "6":
                # Update the reservation details
                table_number = int(input("Enter your table number: "))
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")
                new_date = input("Enter new date (YYYY-MM-DD): ")
                new_time = input("Enter new time: ")
                new_num_guests = int(input("Enter new number of guests: "))

                reservation = reservation_manager.find_reservation(table_number, date, time)

                if reservation:
                    reservation_manager.update_reservation(reservation, new_date, new_time, new_num_guests)
                    print("Reservation details updated.")
                else:
                    print("No reservation found for the entered details.")
            elif customer_choice == "7":
                # Back to main menu
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    elif user_type == "2":
        # Staff Section
        while True:
            print("\n1. View Menu")
            print("2. View All Reservations")
            print("3. View Reservation Details")
            print("4. Update Reservation Details")
            print("5. Cancel Reservation")
            print("6. Add New Menu Item")
            print("7. Update Menu Item")
            print("8. Delete Menu Item")
            print("9. Exit")

            staff_choice = input("Enter your choice (1-9): ")

            if staff_choice == "1":
                staff.view_menu()
            elif staff_choice == "2":
                staff.view_all_reservations()
            elif staff_choice == "3":
                table_number = int(input("Enter table number: "))
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")
                staff.view_reservation_details(table_number, date, time)
            elif staff_choice == "4":
                table_number = int(input("Enter table number: "))
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")
                new_date = input("Enter new date (YYYY-MM-DD): ")
                new_time = input("Enter new time: ")
                new_num_guests = int(input("Enter new number of guests: "))
                staff.update_reservation_details(table_number, date, time, new_date, new_time, new_num_guests)
            elif staff_choice == "5":
                table_number = int(input("Enter table number: "))
                date = input("Enter the date (YYYY-MM-DD): ")
                time = input("Enter the time: ")
                staff.cancel_reservation(table_number, date, time)
            elif staff_choice == "6":
                name = input("Enter the name of the new menu item: ")
                description = input("Enter the description of the new menu item: ")
                price = float(input("Enter the price of the new menu item: "))
                staff.add_new_menu_item(name, description, price)
            elif staff_choice == "7":
                name = input("Enter the name of the menu item to update: ")
                description = input("Enter the new description of the menu item: ")
                price = float(input("Enter the new price of the menu item: "))
                staff.update_menu_item(name, description, price)
            elif staff_choice == "8":
                name = input("Enter the name of the menu item to delete: ")
                staff.delete_menu_item(name)
            elif staff_choice == "9":
                print("Exiting the program.")
                exit()
            else:
                print("Invalid choice. Please enter a valid option.")

    elif user_type == "3":
        # Exit
        print("Exiting the program.")
        exit()

    else:
        print("Invalid choice. Please enter a valid option.")

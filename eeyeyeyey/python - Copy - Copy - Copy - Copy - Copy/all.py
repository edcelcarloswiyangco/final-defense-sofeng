
#admin.py

import log_in_and_sign_up as log

admin_password = 'superadmin'

def manage_barbers():
    while True:
        print("\n--- Manage Barbers ---")
        print("1. Add Barber Account")
        print("2. Delete Barber Account")
        print("3. Show All Barbers")
        print("4. Set Barber Availability")  
        print("5. Back to Admin Menu")

        choice = input("Choose option: ")

        if choice == '1':
            log.signup(log.barbers)

        elif choice == '2':
            email = input("Enter barber email to delete: ").strip()
            if email in log.barbers:
                del log.barbers[email]
                if email in log.barber_schedules:
                    del log.barber_schedules[email]
                print("Barber deleted successfully!")
            else:
                print("Barber not found!")

        elif choice == '3':
            print("List of Barbers:")
            if log.barbers:
                for email in log.barbers:
                    print("-", email)
            else:
                print("No barber accounts found.")

        elif choice == '4':
            email = input("Enter barber email to set availability: ").strip()
            if email in log.barbers:
                timeslot = input("Enter available slot (e.g., 2025-04-10 10:00 AM): ").strip()
                if email not in log.barber_schedules:
                    log.barber_schedules[email] = []
                log.barber_schedules[email].append(timeslot)
                print("Timeslot added to barber schedule.")
            else:
                print("Barber not found.")

        elif choice == '5':
            break

        else:
            print("Invalid choice! Please try again.")


def set_barber_schedule():
    email = input("Enter barber email to set availability: ").strip()
    if email not in log.barbers:
        print("Barber not found.")
        return

    print("1. Enter custom slots")
    print("2. Use preset daily schedule (9 AM to 5 PM)")
    choice = input("Choose option: ")

    if choice == '1':
        while True:
            slot = input("Enter slot (or 'done' to finish): ").strip()
            if slot.lower() == 'done':
                break
            log.barber_schedules.setdefault(email, []).append(slot)
    elif choice == '2':
        date = input("Enter date (e.g., 2025-04-10): ").strip()
        for hour in range(9, 18):
            slot = f"{date} {hour}:00"
            log.barber_schedules.setdefault(email, []).append(slot)
        print("Preset schedule added.")

def show_reviews():
    print("\n--- Barber Ratings & Reviews ---")
    for barber, feedbacks in log.reviews.items():
        print(f"\nBarber: {barber}")
        for fb in feedbacks:
            print(f"- {fb['customer']} rated {fb['rating']}/5: {fb['comment']}")

def show_barber_calendar():
    print("\n--- Barber Calendar View ---")
    for barber, slots in log.barber_schedules.items():
        print(f"\nBarber: {barber}")
        for slot in sorted(slots):
            print(f" - {slot}")

def admin_menu():
    print("\nWelcome, Admin!")
    while True:
        print("\n--- Admin Menu ---")
        print("1. Manage Barbers")
        print("2. Confirm Cancellation Requests")
        print("3. Confirm Payment After Service")
        print("4. View Ratings & Reviews")
        print("5. View Barber Calendar")
        print("6. Exit Admin Menu")

        choice = input("Choose option: ")

        if choice == '1':
            manage_barbers()
        elif choice == '2':
            confirm_cancellation()
        elif choice == '3':
            confirm_payment()
        elif choice == '4':
            show_reviews()
        elif choice == '5':
            show_barber_calendar()
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please try again.")

def confirm_cancellation():
    print("\n--- Cancel Booking Requests ---")
    for customer_email, requests in log.cancellation_requests.items():
        for appointment in requests[:]:
            print(f"Customer: {customer_email} | Appointment: {appointment['barber']} | Slot: {appointment['slot']}")
            confirm = input("Confirm cancellation (y/n)? ").strip().lower()
            if confirm == 'y':
                log.appointments[customer_email] = [a for a in log.appointments[customer_email] if a != appointment]
                log.barber_schedules.setdefault(appointment['barber'], []).append(appointment['slot'])
                requests.remove(appointment)
                log.send_email(customer_email, "Appointment Cancelled", f"Your appointment with {appointment['barber']} at {appointment['slot']} has been cancelled.")
                print("Appointment cancelled.")
            else:
                print("Cancellation not confirmed.")

def confirm_payment():
    print("\n--- Confirm Payment After Service ---")
    for customer_email, appointments in log.appointments.items():
        if customer_email in log.payment_status:
            continue
        for appointment in appointments:
            confirm = input(f"Has {appointment['barber']}'s service for {customer_email} been completed and paid? (y/n): ").strip().lower()
            if confirm == 'y':
                log.payment_status[customer_email] = True
                log.send_email(customer_email, "Payment Confirmed", f"Payment for service by {appointment['barber']} is confirmed. Thank you!")
                print("Payment confirmed.")
            else:
                print("Payment not confirmed.")



#barber.py
import calendar
from datetime import datetime
import log_in_and_sign_up as log


def view_calendar(barber_email):
    print("\n--- Barber's Monthly Calendar ---")
    current_month = datetime.now().month
    current_year = datetime.now().year

    month_days = calendar.monthcalendar(current_year, current_month)

    print(f"--- {calendar.month_name[current_month]} {current_year} ---")
    for week in month_days:
        for day in week:
            if day != 0:  
                date = datetime(current_year, current_month, day)
                formatted_date = date.strftime('%Y-%m-%d')

                if formatted_date in log.barber_schedules.get(barber_email, []):
                    print(f"{day}: Available")
                else:
                    booked = False
                    for customer_email, appointments in log.appointments.items():
                        for app in appointments:
                            if app['barber'] == barber_email and app['slot'] == formatted_date:
                                print(f"{day}: Booked by {customer_email}")
                                booked = True
                                break
                    if not booked:
                        print(f"{day}: No available slots")
    print("\n")



    month_days = calendar.monthcalendar(current_year, current_month)

    print(f"--- {calendar.month_name[current_month]} {current_year} ---")
    for week in month_days:
        for day in week:
            if day != 0: 
                date = datetime(current_year, current_month, day)
                formatted_date = date.strftime('%Y-%m-%d')
                if formatted_date in log.barber_schedules.get(barber_email, []):
                    print(f"{day}: Available")
                else:
                    print(f"{day}: No available slots")
    print("\n")


def view_my_schedule(barber_email):
    print("\n--- My Schedule ---")
    schedule = log.barber_schedules.get(barber_email, [])
    if schedule:
        for idx, slot in enumerate(schedule, 1):
            print(f"{idx}. {slot}")
    else:
        print("You have no available schedule set.")




def view_my_appointments(barber_email):
    print("\n--- Appointments Booked ---")
    found = False
    for customer_email, appointments in log.appointments.items():
        for app in appointments:
            if app['barber'] == barber_email:
                print(f"Customer: {customer_email} | Slot: {app['slot']}")
                found = True
    if not found:
        print("No appointments booked yet.")


def view_reviews(barber_email):
    print("\n--- My Ratings & Reviews ---")
    reviews = log.reviews.get(barber_email, [])
    if reviews:
        for review in reviews:
            print(f"Rating: {review['rating']} | Review: {review['comment']}")
    else:
        print("No reviews yet.")


def barber_dashboard(barber_email):
    while True:
        print(f"\n--- Barber Dashboard ({barber_email}) ---")
        print("1. View My Schedule")
        print("2. View Appointments")
        print("3. View Ratings & Reviews")
        print("4. View My Calendar")
        print("5. Logout")

        choice = input("Choose option: ").strip()

        if choice == '1':
            view_my_schedule(barber_email)
        elif choice == '2':
            view_my_appointments(barber_email)
        elif choice == '3':
            view_reviews(barber_email)
        elif choice == '4':
            view_calendar(barber_email) 
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

#customer.py

import log_in_and_sign_up as log

def view_barbers():
    print("\n--- List of Barbers ---")
    if log.barbers:
        for idx, email in enumerate(log.barbers, 1):
            print(f"{idx}. {email}")
    else:
        print("No barbers available at the moment.")

def book_appointment(customer_email):
    if not log.barbers:
        print("Sorry, no barbers available for booking.")
        return

    print("\n--- Book an Appointment ---")
    print("Choose a barber from the list below:")

    barber_list = list(log.barbers.keys())
    for idx, barber_email in enumerate(barber_list, 1):
        print(f"{idx}. {barber_email}")

    try:
        choice = int(input("Enter number of the barber you want to book: "))
        selected_barber = barber_list[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    available_slots = log.barber_schedules.get(selected_barber, [])
    if not available_slots:
        print("This barber has no available slots.")
        return

    print("\nAvailable Slots:")
    for idx, slot in enumerate(available_slots, 1):
        print(f"{idx}. {slot}")

    try:
        slot_choice = int(input("Choose a slot number to book: "))
        selected_slot = available_slots[slot_choice - 1]
    except (ValueError, IndexError):
        print("Invalid slot choice.")
        return

    appointment = {
        'barber': selected_barber,
        'slot': selected_slot
    }

    log.appointments.setdefault(customer_email, []).append(appointment)
    
    log.barber_schedules[selected_barber].remove(selected_slot)

    print("Appointment booked successfully!")


def cancel_appointment(customer_email):
    print("\n--- Cancel My Appointment ---")
    appointments = log.appointments.get(customer_email, [])
    if not appointments:
        print("You have no appointments to cancel.")
        return

    for idx, appointment in enumerate(appointments, 1):
        print(f"{idx}. Barber: {appointment['barber']} | Slot: {appointment['slot']}")

    try:
        choice = int(input("Choose appointment to cancel: "))
        selected_appointment = appointments[choice - 1]
        # Add to cancellation request
        if customer_email not in log.cancellation_requests:
            log.cancellation_requests[customer_email] = []
        log.cancellation_requests[customer_email].append(selected_appointment)
        print("Cancellation request has been sent to the admin.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def view_my_appointments(customer_email):
    print("\n--- My Appointments ---")
    user_appointments = log.appointments.get(customer_email, [])
    if not user_appointments:
        print("You have no appointments yet.")
    else:
        for idx, app in enumerate(user_appointments, 1):
            print(f"{idx}. Barber: {app['barber']} | Slot: {app['slot']}")

def customer_menu(customer_email):
    while True:
        print("\n--- Customer Menu ---")
        print("1. View Barbers")
        print("2. Book Appointment")
        print("3. View My Appointments")
        print("4. Cancel Appointment")
        print("5. Logout")

        choice = input("Choose option: ")

        if choice == '1':
            view_barbers()
        elif choice == '2':
            book_appointment(customer_email)
        elif choice == '3':
            view_my_appointments(customer_email)
        elif choice == '4':
            cancel_appointment(customer_email)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")


#log_in_and_sign_up.py

users = {}
barbers = {}
appointments = {}
barber_schedules = {}
cancellation_requests = {}
payment_status = {}
reviews = {}

def send_email(to, subject, message):
    print(f"\n[EMAIL SENT to {to}]")
    print(f"Subject: {subject}")
    print(f"Message: {message}")

def login(accounts):
    email = input("Enter your email here: ").strip()
    password = input("Enter your password here: ").strip()
    if email in accounts and accounts[email]['password'] == password:
        print("Login successful!")
        return email
    else:
        print("Invalid email or password.")
        return None

def signup(accounts):
    email = input("Enter your desired email: ").strip()
    if email in accounts:
        print("Email already exists!")
    else:
        password = input("Enter your password: ").strip()
        accounts[email] = {'password': password}
        print("Account created successfully!")


#customer.py

import log_in_and_sign_up as log

def view_barbers():
    print("\n--- List of Barbers ---")
    if log.barbers:
        for idx, email in enumerate(log.barbers, 1):
            print(f"{idx}. {email}")
    else:
        print("No barbers available at the moment.")

def book_appointment(customer_email):
    if not log.barbers:
        print("Sorry, no barbers available for booking.")
        return

    print("\n--- Book an Appointment ---")
    print("Choose a barber from the list below:")

    barber_list = list(log.barbers.keys())
    for idx, barber_email in enumerate(barber_list, 1):
        print(f"{idx}. {barber_email}")

    try:
        choice = int(input("Enter number of the barber you want to book: "))
        selected_barber = barber_list[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    available_slots = log.barber_schedules.get(selected_barber, [])
    if not available_slots:
        print("This barber has no available slots.")
        return

    print("\nAvailable Slots (only unbooked shown):")
    for idx, slot in enumerate(available_slots, 1):
        print(f"{idx}. {slot}")

    try:
        slot_choice = int(input("Choose a slot number to book: "))
        selected_slot = available_slots[slot_choice - 1]
    except (ValueError, IndexError):
        print("Invalid slot choice.")
        return

    appointment = {
        'barber': selected_barber,
        'slot': selected_slot
    }

    log.appointments.setdefault(customer_email, []).append(appointment)
    log.barber_schedules[selected_barber].remove(selected_slot)
    log.send_email(customer_email, "Appointment Booked", f"Barber: {selected_barber}, Slot: {selected_slot}")
    print("Appointment booked successfully!")

def cancel_appointment(customer_email):
    print("\n--- Cancel My Appointment ---")
    appointments = log.appointments.get(customer_email, [])
    if not appointments:
        print("You have no appointments to cancel.")
        return

    for idx, appointment in enumerate(appointments, 1):
        print(f"{idx}. Barber: {appointment['barber']} | Slot: {appointment['slot']}")

    try:
        choice = int(input("Choose appointment to cancel: "))
        selected_appointment = appointments[choice - 1]
        log.cancellation_requests.setdefault(customer_email, []).append(selected_appointment)
        print("Cancellation request has been sent to the admin.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def view_my_appointments(customer_email):
    print("\n--- My Appointments ---")
    user_appointments = log.appointments.get(customer_email, [])
    if not user_appointments:
        print("You have no appointments yet.")
    else:
        for idx, app in enumerate(user_appointments, 1):
            print(f"{idx}. Barber: {app['barber']} | Slot: {app['slot']}")

def rate_barber(customer_email):
    print("\n--- Rate Your Barber ---")
    appointments = log.appointments.get(customer_email, [])
    if not appointments:
        print("You have no past appointments to rate.")
        return

    for idx, appointment in enumerate(appointments, 1):
        print(f"{idx}. Barber: {appointment['barber']} | Slot: {appointment['slot']}")

    try:
        choice = int(input("Choose which appointment to rate: "))
        selected_appointment = appointments[choice - 1]
        barber_email = selected_appointment['barber']
        rating = int(input("Enter rating (1-5): "))
        comment = input("Enter your comment: ").strip()
        log.reviews.setdefault(barber_email, []).append({
            'customer': customer_email,
            'rating': rating,
            'comment': comment
        })
        print("Thank you for your feedback!")
    except (ValueError, IndexError):
        print("Invalid input.")

def customer_menu(customer_email):
    while True:
        print("\n--- Customer Menu ---")
        print("1. View Barbers")
        print("2. Book Appointment")
        print("3. View My Appointments")
        print("4. Cancel Appointment")
        print("5. Rate Barber")
        print("6. Logout")

        choice = input("Choose option: ")

        if choice == '1':
            view_barbers()
        elif choice == '2':
            book_appointment(customer_email)
        elif choice == '3':
            view_my_appointments(customer_email)
        elif choice == '4':
            cancel_appointment(customer_email)
        elif choice == '5':
            rate_barber(customer_email)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")


# main.py
import barber 
import log_in_and_sign_up as log
import admin as ad

import customer

while True:
    print("\n=== Online Barber Booking System ===")
    print("1. User Login")
    print("2. User Sign Up")
    print("3. Exit")

    choice = input("Choose option (or type 'barber' or 'admin'): ").strip().lower()

    if choice == '1':
        customer_email = log.login(log.users)
        if customer_email:
            customer.customer_menu(customer_email)

    elif choice == '2':
        log.signup(log.users)

    elif choice == 'barber':
        barber_email = log.login(log.barbers)
        if barber_email:
            barber.barber_dashboard(barber_email)  


    elif choice == 'admin':
        for attempt in range(3):
            password = input("Enter Admin Password: ")
            if password == ad.admin_password:
                ad.admin_menu()
                break
            else:
                print("Wrong password.")
        else:
            print("Too many failed attempts.")

    elif choice == '3':
        print("Thank you for using our system!")
        break

    else:
        print("Invalid choice! Please try again.")

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
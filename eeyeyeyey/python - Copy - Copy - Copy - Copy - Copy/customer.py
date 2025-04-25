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
            paid = "PAID" if app in log.payment_status.get(customer_email, []) else "PENDING"
            print(f"{idx}. Barber: {app['barber']} | Slot: {app['slot']} | Payment: {paid}")


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

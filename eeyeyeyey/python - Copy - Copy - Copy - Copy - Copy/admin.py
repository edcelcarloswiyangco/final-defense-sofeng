
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
    # Make a copy of the cancellation_requests items so that we can modify the dictionary safely while iterating.
    for customer_email, requests in list(log.cancellation_requests.items()):
        # Iterate over a shallow copy of the requests list to allow removals in-place.
        for appointment in requests[:]:
            print(f"Customer: {customer_email} | Appointment: {appointment['barber']} | Slot: {appointment['slot']}")
            confirm = input("Confirm cancellation (y/n)? ").strip().lower()
            if confirm == 'y':
                # Remove the appointment from the customer's appointments list, if it exists.
                if customer_email in log.appointments and appointment in log.appointments[customer_email]:
                    log.appointments[customer_email].remove(appointment)
                else:
                    print("Warning: Appointment not found in customer's list.")

                # Return the canceled slot back to the barber's schedule.
                log.barber_schedules.setdefault(appointment['barber'], []).append(appointment['slot'])

                # Remove the appointment from the cancellation request list.
                requests.remove(appointment)

                # Notify the customer via email.
                log.send_email(customer_email, "Appointment Cancelled", 
                               f"Your appointment with {appointment['barber']} at {appointment['slot']} has been cancelled.")
                print("Appointment cancelled.")
            else:
                print("Cancellation not confirmed.")

        # If no cancellation requests remain for a customer, remove their key entirely.
        if not requests:
            del log.cancellation_requests[customer_email]


def confirm_payment():
    print("\n--- Confirm Payment After Service ---")
    all_unpaid = []

    # Gather all unpaid appointments
    for customer_email, appointments in log.appointments.items():
        for appointment in appointments:
            paid_appointments = log.payment_status.get(customer_email, [])
            if appointment not in paid_appointments:
                all_unpaid.append((customer_email, appointment))

    if not all_unpaid:
        print("No unpaid appointments found.")
        return

    # Display unpaid appointments
    for idx, (customer_email, appointment) in enumerate(all_unpaid, 1):
        print(f"{idx}. Customer: {customer_email} | Barber: {appointment['barber']} | Slot: {appointment['slot']}")

    try:
        choice = int(input("Enter the number of the appointment to confirm payment (or 0 to cancel): "))
        if choice == 0:
            print("Cancelled payment confirmation.")
            return

        selected = all_unpaid[choice - 1]
        customer_email, appointment = selected

        # Mark as paid
        log.payment_status.setdefault(customer_email, []).append(appointment)
        log.send_email(
            customer_email,
            "Payment Confirmed",
            f"Payment for service by {appointment['barber']} at {appointment['slot']} is confirmed. Thank you!"
        )
        print("Payment confirmed successfully.")

    except (ValueError, IndexError):
        print("Invalid selection.")


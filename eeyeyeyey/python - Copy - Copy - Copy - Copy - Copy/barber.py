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
        #///print("4. View My Calendar")///
        print("4. Logout")

        choice = input("Choose option: ").strip()

        if choice == '1':
            view_my_schedule(barber_email)
        elif choice == '2':
            view_my_appointments(barber_email)
        elif choice == '3':
            view_reviews(barber_email)
        elif choice == '5':
            view_calendar(barber_email) 
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

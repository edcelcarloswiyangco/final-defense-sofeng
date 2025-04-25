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

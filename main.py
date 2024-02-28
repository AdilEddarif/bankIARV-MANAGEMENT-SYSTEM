from users import user
def main():
    user_test = user.User()

    def display_menu():
        """Display the main menu."""
        menu = """ 
               ************************************************************************
               #|#                 -- WELCOME TO BANK IARV --                       #|#
               #|#                                                                  #|#
               #|#                                                                  #|#
               #|#       1) Create Account : 1                                      #|#
               #|#       2) Login : 2                                               #|#
               #|#       3) Exit : 'o'                                              #|#
               #|#                                                                  #|#
               ************************************************************************
              """
        print(menu.center(100))

    def user_interface(username,password):
        while True:
            print("YOU ARE IN USER DASHBOARD --- '/h' to display help table ---")
            choice = input("Choose an option : ")
            if choice =="/h":
                user_test.check_credentials(username,password)


            elif choice == "1":
                user_info = user_test.get_user_info(username)
                if user_info:
                    print("Personal Information:")
                    print(f"Your Unique ID  : {user_info[0]}")
                    print(f"First Name      : {user_info[1]}")
                    print(f"Last Name       : {user_info[2]}")
                    print(f"National ID     : {user_info[3]}")
                    print(f"Email           : {user_info[4]}")
                    print(f"Phone           : {user_info[5]}")
                else:
                    print("User not found.")


            elif choice == "2":
                user_info = user_test.get_user_info(username)
                if user_info:
                    print(f"Your Balance is Currently :  {user_info[6]} DH.")


            elif choice == "3":
                while True:
                    try:
                        amount = float(input("Enter the amount you want to deposit: "))
                        break
                    except ValueError:
                        print("Error: Amount should be a float!")

                user_test.deposit_balance(username,amount)
                print(f"{amount} DH has been successfully added to your account.")


            elif choice == "4":
                while True:
                    try:
                        amount = float(input("Enter the amount you want to withdraw : "))
                        break
                    except ValueError:
                        print("Error: Amount should be a float!")

                user_test.withdraw_balance(username,amount)


            elif choice=="5":
                while True:
                    try:
                        receiver_id = input("Enter the recepient ID : ")
                        amount = float((input("Enter the amount to Transfer : ")))

                        break
                    except ValueError:
                        print("Error: Amount should be a float!")
                user_test.transfer_money(username, receiver_id, amount)


            elif choice=="6":
                user_test.show_transactions(username)


            elif choice=="7":
                check=user_test.check_admin(username)
                if check:
                    while True:
                        print("YOU ARE IN ADMIN DASHBOARD --- '/h' to display help table ---")
                        admn_opt=input("Choose an admin option : ")
                        if admn_opt == "1":
                            user_id = input("Enter user ID to update username : ")
                            new_name= input("Enter new Username : ")
                            user_test.update_username(user_id,new_name)
                        elif admn_opt == "/h":
                            user_test.check_admin(username)
                        elif admn_opt == "2":
                            user_id = input("Enter user ID to update password : ")
                            new_password=input("Enter new Password : ")
                            user_test.update_password(user_id,new_password)
                        elif admn_opt == "3":
                            user_id = input("Enter user ID to update email : ")
                            new_email = input("Enter new Email : ")
                            user_test.update_email(user_id,new_email)
                        elif admn_opt == "4":
                            user_id = input("Enter user ID to delete : ")
                            user_test.delete_user(user_id)
                        elif admn_opt == "5":
                            user_test.show_all_users()
                        elif admn_opt == "e":
                            exit()
                        elif admn_opt == "o":
                            break





            elif choice == "o":
                break
            elif choice == "e":
                exit()
            else:
                print("Invalid Command!")

    def login_interface():
        while True:
            display_menu()
            welcome = input("Choose an option : ")

            if welcome == "2":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                if user_test.check_credentials(username, password):
                    user_interface(username,password)

                else:
                    print("Error: Incorrect username or password, please try again.")
            elif welcome == "1":
                firstname = input("Enter your firstname: ")
                lastname = input("Enter your lastname: ")
                nationalid = input("Enter your national id number: ")
                email = input("Enter your email: ")
                phone = input("Enter your phone number: ")
                username = input("Create username: ")
                while (user_test.check_username(username)==True):
                    username = input("Create username: ")

                password = input("Create password: ")
                user_test.insert_credentials(firstname, lastname, nationalid, email, phone, username, password)
            elif welcome == "o":
                exit()

            else:
                print("Invalid Command!")
                login_interface()

    login_interface()

if __name__ == "__main__":
    main()

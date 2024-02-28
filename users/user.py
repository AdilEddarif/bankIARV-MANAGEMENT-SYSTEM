from datetime import datetime
class User:
    def check_username(self, username):
        try:
            with open("database/usersdatabase.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[7] == username:
                        print("Username already exists.")
                        return True
            print("Username is available.")
            return False
        except Exception as e:
            print("Error while checking username:", e)
            return True


    def check_credentials(self, username, password):
        try:
            with open("database/usersdatabase.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    name = data[1].upper()
                    if data[7] == username and data[8] == password:
                        user_menu = f""" 
                                                ********************************************************************
                                                             -- HELLO {name}! WELCOME TO YOUR ACCOUNT --           
                                                *                                                                  *
                                                *                                                                  *
                                                *       1) Show Account :                   1                      *
                                                *       2) Show Balance :                   2                      *
                                                *       3) deposit balance :                3                      *
                                                *       4) Withdrawal Balance :             4                      *
                                                *       5) Transfer Money :                 5                      *
                                                *       6) Show Transactions History :      6                      *
                                                *       7) Dashboard Admin :                7                      *
                                                *       8) Logout :                        'o'                     *
                                                *       9) Exit :                          'e'                     *
                                                *                                                                  *
                                                ********************************************************************                   
                                            """
                        print(user_menu)
                        return True

                return False
        except Exception as e:
            print("Error while checking credentials:", e)
            return False



    def withdraw_balance(self, username, amount):
        try:
            # Update user's balance
            with open("database/usersdatabase.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for i, line in enumerate(lines):
                    data = line.strip().split(",")
                    if data[7] == username:
                        current_balance = float(data[6])
                        if amount <= current_balance:
                            new_balance = current_balance - amount
                            data[6] = str(new_balance)
                            line = ','.join(data) + '\n'
                            lines[i] = line
                            file.seek(0)
                            file.writelines(lines)
                            file.truncate()
                            print("Withdrawal successful.")
                        else:
                            print("Error : Amount is bigger than balance.")

                        break
                else:
                    print("User not found in database.")
            with open("database/transactions.txt", "a") as transaction_file:
                transaction_file.write(f"Sender: {username}, Receiver: {username}, Amount: -{amount} DH, Date: {datetime.now()}\n")
        except Exception as e:
            print("Error:", e)




    def deposit_balance(self, username,amount):
        try:
            # Update receiver's balance
            with open("database/usersdatabase.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    data = line.strip().split(",")
                    if data[7] == username:
                        current_balance = float(data[6])
                        new_balance = current_balance + amount
                        data[6] = str(new_balance)
                        line = ','.join(data) + '\n'
                    file.write(line)
                file.truncate()

            # Record transaction in transactions.txt
            with open("database/transactions.txt", "a") as transaction_file:
                transaction_file.write(f"Sender: {username}, Receiver: {username}, Amount: +{amount} DH, Date: {datetime.now()}\n")


        except Exception as e:
            print("Error while depositing balance:", e)




    def get_last_id(self):
        try:
            with open("database/usersdatabase.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1]
                    last_id = last_line.split(",")[0]
                    return int(last_id)
                else:
                    return 0
        except FileNotFoundError:
            return 0
        except Exception as e:
            print("Error while getting last ID:", e)
            return None





    def get_user_info(self, username):
        try:
            with open("database/usersdatabase.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[7] == username:
                        return data[:7]
            return None
        except Exception as e:
            print("Error while getting user info:", e)
            return None





    def insert_credentials(self, firstname, lastname, nationalid, email, phone, username, password):
        try:
            last_id = self.get_last_id()
            new_id = last_id + 1
            with open("database/usersdatabase.txt", "a") as file:
                file.write(
                    f"{new_id},{firstname},{lastname},{nationalid},{email},{phone},0,{username},{password},0\n")
            print("User created successfully")
        except Exception as e:
            print("Error while inserting credentials:", e)

    def transfer_money(self, username, receiver_id, amount):
        try:
            sender_found = False
            receiver_found = False
            receiver_name = None

            # Update receiver's balance
            with open("database/usersdatabase.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for i, line in enumerate(lines):
                    data = line.strip().split(",")
                    if  data[0] == receiver_id:
                        receiver_id=data[0]
                        receiver_name = data[7]
                        receiver_found = True
                        receiver_balance = float(data[6])

                        data[6] = str(receiver_balance)
                        lines[i] = ','.join(data) + '\n'
                        file.seek(0)
                        file.writelines(lines)
                        file.truncate()

            # If receiver is found, update sender's balance
            if receiver_found:
                with open("database/usersdatabase.txt", "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    for i, line in enumerate(lines):
                        data = line.strip().split(",")
                        if data[7] == username:
                            user_id=data[0]
                            if(user_id != receiver_id):
                                sender_found = True
                                receiver_balance += amount
                                sender_balance = float(data[6])
                                if amount <= sender_balance:
                                    sender_balance -= amount
                                    data[6] = str(sender_balance)
                                    lines[i] = ','.join(data) + '\n'
                                    file.seek(0)
                                    file.writelines(lines)
                                    file.truncate()
                                    print("Transfer successful.")
                                else:
                                    print("Error: Insufficient balance for transfer.")
                                break
                            else:
                                print("Error : You cant transfer money to yourself! ")
                                break


            if not receiver_found:
                print("Error: Receiver not found.")

            if sender_found and receiver_found:
                with open("database/transactions.txt", "a") as transaction_file:
                    transaction_file.write(
                        f"Sender: {username}, Receiver: {receiver_name}, Amount: {amount} DH, Date: {datetime.now()}\n")

        except Exception as e:
            print("Error during money transfer:", e)

    def show_transactions(self, username):
        try:
            print("+----------------------+----------------------+------------+-----------------------------+")
            print("|       Sender         |       Receiver       |   Amount   |        Date                 |")
            print("+----------------------+----------------------+------------+-----------------------------+")

            with open("database/transactions.txt", "r") as transaction_file:
                for line in transaction_file:
                    data = line.strip().split(", ")
                    sender = data[0].split(": ")[1]
                    receiver = data[1].split(": ")[1]
                    amount = data[2].split(": ")[1]
                    transaction_date = data[3].split(": ")[1]

                    if (sender == username and receiver!=username):
                        print("| {:<20} | {:<20} | {:<10} | {:<19} |".format(sender, receiver, "-" + amount,
                                                                             transaction_date))
                    elif (receiver == username and sender!=username):
                        print("| {:<20} | {:<20} | {:<10} | {:<19} |".format(sender, receiver, "+" + amount,
                                                                             transaction_date))
                    elif (sender==username and receiver==username):
                        print("| {:<20} | {:<20} | {:<10} | {:<19} |".format(sender, receiver,amount,
                                                                             transaction_date))


            print("+----------------------+----------------------+------------+-----------------------------+")

        except FileNotFoundError:
            print("Transaction database not found.")
        except Exception as e:
            print("Error while retrieving transaction history:", e)
    def check_admin(self,username):
        try:
            with open("database/usersdatabase.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    name = data[1].upper()
                    if data[7] == username and data[9] =="1":
                        """Display the admin menu."""
                        user_menu = f""" 
                                        ********************************************************************
                                                    -- WELCOME {name} TO ADMIN DASHBOARD --            
                                        *                                                                  *
                                        *                                                                  *
                                        *       1) update name :             1                             *
                                        *       2) update password :         2                             *
                                        *       3) update email :            3                             *
                                        *       4) Delete Account :          4                             *
                                        *       5) Show Users     :          5                             *
                                        *       6) Quit Admin Dashboard :   'o'                            *
                                        *       7) Exit :                   'e'                            *
                                        *                                                                  *
                                        ********************************************************************                   
                                    """
                        print(user_menu)
                        return True
                    else:
                        print("You are not an Admin !")
                        break

                return False
        except Exception as e:
            print("Error while checking for admin:", e)
            return False

    def update_username(self,user_id, new_name):
        try:
            # Read the contents of the file
            with open("database/usersdatabase.txt", "r") as file:
                lines = file.readlines()

            # Iterate through each line to find the user by user_id
            for i, line in enumerate(lines):
                data = line.strip().split(",")
                if data[0] == user_id:
                    user_id = data[0]
                    old_name= data[7]
                    # Update the name with the new_name
                    data[7] = new_name
                    # Join the modified data into a line
                    lines[i] = ",".join(data) + "\n"
                    break  # Stop searching once the user is found

            else:
                # If the user_id is not found, return without updating
                print("User ID not found.")
                return

            # Write the modified contents back to the file
            with open("database/usersdatabase.txt", "w") as file:
                file.writelines(lines)

            print(f"SUCCESS : Username updated successfully from '{old_name}' to : '{new_name}' for user ID : '{user_id}'")

        except Exception as e:
            print("Error while updating username:", e)

    def update_password(self,user_id, new_password):
        try:
            # Read the contents of the file
            with open("database/usersdatabase.txt", "r") as file:
                lines = file.readlines()

            # Iterate through each line to find the user by user_id
            for i, line in enumerate(lines):
                data = line.strip().split(",")
                if data[0] == user_id:
                    user_id=data[0]
                    old_password = data[8]
                    # Update the name with the new_name
                    data[8] = new_password
                    # Join the modified data into a line
                    lines[i] = ",".join(data) + "\n"
                    break  # Stop searching once the user is found

            else:
                # If the user_id is not found, return without updating
                print("User ID not found.")
                return

            # Write the modified contents back to the file
            with open("database/usersdatabase.txt", "w") as file:
                file.writelines(lines)

            print(f"SUCCESS : Password updated successfully from '{old_password}' to : '{new_password}' for user ID : '{user_id}'")

        except Exception as e:
            print("Error while updating password:", e)

    def update_email(self, user_id, new_email):
        try:
            # Read the contents of the file
            with open("database/usersdatabase.txt", "r") as file:
                lines = file.readlines()

            # Iterate through each line to find the user by user_id
            for i, line in enumerate(lines):
                data = line.strip().split(",")
                if data[0] == user_id:
                    user_id = data[0]
                    old_email = data[4]
                    # Update the name with the new_name
                    data[4] = new_email
                    # Join the modified data into a line
                    lines[i] = ",".join(data) + "\n"
                    break  # Stop searching once the user is found

            else:
                # If the user_id is not found, return without updating
                print("User ID not found.")
                return

            # Write the modified contents back to the file
            with open("database/usersdatabase.txt", "w") as file:
                file.writelines(lines)

            print(
                f"SUCCESS : Email updated successfully from '{old_email}' to : '{new_email}' for user ID : '{user_id}'")

        except Exception as e:
            print("Error while updating password:", e)

    def delete_user(self,user_id):
        try:
            # Read the contents of the file
            with open("database/usersdatabase.txt", "r") as file:
                lines = file.readlines()

            user_found = False
            # Iterate through each line to find the user by username
            for line in lines:
                data = line.strip().split(",")
                if data[0] == user_id:
                    user_id = data[0]
                    if (data [9] != "1"):
                        lines.remove(line)
                        user_found = True
                        break
                    else:
                        print("Error: Cannot delete an ADMIN !")

            if not user_found:
                print("User not found.")
                return

            # Write the modified contents back to the file
            with open("database/usersdatabase.txt", "w") as file:
                file.writelines(lines)

            print(f"SUCCESS : User ID {user_id} deleted successfully.")

        except Exception as e:
            print("Error while deleting user:", e)

    def show_all_users(self):
        try:
            # Read the contents of the file
            with open("database/usersdatabase.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    def isadmin(data):
                        if data == "1":
                            return True
                        else:
                            return False
                    user_details = f"User ID: '{data[0]}', First Name: '{data[1]}', Last Name: '{data[2]}', National ID: '{data[3]}', Email: '{data[4]}', Phone: '{data[5]}', Balance: '{data[6]}', Username: '{data[7]}', Password: '{data[8]}', IS_ADMIN: '{isadmin(data[9])}'"
                    print(user_details)

        except FileNotFoundError:
            print("User database not found.")
        except Exception as e:
            print("Error while showing users:", e)


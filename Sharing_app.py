class ExpenseSharing:
    def __init__(self, friends):
        self.balances = {friend: 0 for friend in friends}
        print(f"Initialized balances for: {', '.join(friends)}")

    def add_expense(self, payer, amount, participants):
        
        if payer not in self.balances:
            print(f"Error: Payer '{payer}' is not in the list of friends.")
            return
        for p in participants:
            if p not in self.balances:
                print(f"Error: Participant '{p}' is not in the list of friends.")
                return

        self.balances[payer] += amount
        split_amount = amount / len(participants)
        for participant in participants:
            self.balances[participant] -= split_amount
        print(f"Expense added: {payer} paid Rs.{amount:.2f} for {', '.join(participants)}.\n Current balances: {self.balances}")

    def calculate_settlement(self):
        print("\n--- Calculating Settlements ---")
        
        owed = {name: balance for name, balance in self.balances.items() if balance > 0}
        owing = {name: abs(balance) for name, balance in self.balances.items() if balance < 0}

        settlements = []

        
        owed_list = sorted(list(owed.items()), key=lambda item: item[1], reverse=True)
        owing_list = sorted(list(owing.items()), key=lambda item: item[1], reverse=True)

        i, j = 0, 0
        while i < len(owed_list) and j < len(owing_list):
            payer_name, payer_amount = owing_list[j]
            receiver_name, receiver_amount = owed_list[i]

            settle_amount = min(payer_amount, receiver_amount)

            settlements.append(f"{payer_name} owes {receiver_name} Rs.{settle_amount:.2f}")

            
            owing_list[j] = (payer_name, payer_amount - settle_amount)
            owed_list[i] = (receiver_name, receiver_amount - settle_amount)

            
            if owing_list[j][1] == 0:
                j += 1
            if owed_list[i][1] == 0:
                i += 1
        
        if not settlements:
            print("Everyone's balances are settled!")
        else:
            for settlement in settlements:
                print(settlement)

        print("\n--- Final Balances ---")
        for friend, balance in self.balances.items():
            print(f"{friend}: Rs.{balance:.2f}")


if __name__ == "__main__":
    print("Welcome to the Expense Sharing App!")

    
    friends_input = input("Enter the names of friends separated by commas (e.g., Alice, Bob, Carol): ")
    friends = [friend.strip() for friend in friends_input.split(',') if friend.strip()]

    if not friends:
        print("No friends entered. Exiting.")
    else:
        expense_sharing = ExpenseSharing(friends)

        print("\n--- Add Expenses ---")
        print("Enter expense details. Type 'done' for the payer's name to finish.")
        while True:
            payer = input("Enter payer's name (or 'done' to finish): ").strip()
            if payer.lower() == 'done':
                break

            try:
                amount = float(input(f"Enter amount paid by {payer}: "))
                if amount <= 0:
                    print("Amount must be positive. Please try again.")
                    continue
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue

            participants_input = input(f"Enter participants for this expense (comma-separated, e.g., Alice, Bob, Carol): ")
            participants = [p.strip() for p in participants_input.split(',') if p.strip()]

            if not participants:
                print("No participants entered for this expense. Please try again.")
                continue
            
            
            invalid_participants = [p for p in participants if p not in friends]
            if invalid_participants:
                print(f"Error: The following participants are not in your friends list: {', '.join(invalid_participants)}. Please try again.")
                continue

            expense_sharing.add_expense(payer, amount, participants)

        expense_sharing.calculate_settlement()

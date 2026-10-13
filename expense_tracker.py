# Step 4: Error protection (try / except)

total = 0  # initialized OUTSIDE the loop

while True:
    user_input = input("Enter an expense amount (or 'quit' to stop): ")

    if user_input.lower() == "quit":
        break

    try:
        expense = int(user_input)
        total = total + expense
    except ValueError:
        print("Invalid Data. Please enter a number or 'quit'.")

print("Total Spent:", total)
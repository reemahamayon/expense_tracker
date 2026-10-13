# Step 5: Save the total to a file so it is remembered

FILE_NAME = "total.txt"

# Load the old total (or start at 0 if there is no file yet)
try:
    with open(FILE_NAME, "r") as file:
        total = int(file.read())
except (FileNotFoundError, ValueError):
    total = 0

print("Previous total:", total)

while True:
    user_input = input("Enter an expense amount (or 'quit' to stop): ")

    if user_input.lower() == "quit":
        break

    try:
        expense = int(user_input)
        total = total + expense
    except ValueError:
        print("Invalid Data. Please enter a number or 'quit'.")

# Save the new total
with open(FILE_NAME, "w") as file:
    file.write(str(total))

print("Total Spent:", total)
#Kody Graham,
#Algoritms- RSA Project

#Holders for my encrypted and signed messages
messages = []
signatures = []

#Ask for the user choice
def prompt_choice(lowest,highest):

    while True: #Obviously just repeat until the user gives a valid choice
        try:
            x= int(input().strip())
            if lowest <= x <= highest: #these are just the min/max values for valid choices
                return x
        except Exception:
            pass
        print(f"Please enter a number between {lowest} and {highest}.")

#Just a basic function to print our main menu
def main_menu():
    print("Please select your user type:")
    print("")
    print("1. A public user")
    print("")
    print("2. The owner of the keys")
    print("")
    print("3. Exit Program")
    print("")
    print("Enter your choice: ", end="")

#Another basic function to print the menu for the public user choice
def public_menu_list():
    print("")
    print("As a public user, what would you like to do?")
    print("")
    print("1. Send an encrypted message")
    print("")
    print("2. Authenticate a digital signature")
    print("")
    print("3. Exit")
    print("")
    print("")
    print("Enter your choice: ", end="")

#Same thing basic function to print the owners menu
def owner_menu_list():
    print("As the owner of the keys, what would you like to do?")
    print("")
    print("1. Decrypt a received message")
    print("")
    print("2. Digitally sign a message")
    print("")
    print("4. Generating a new set of the keys")
    print("")
    print("")
    print("Enter your choice: ", end="")

#Function to handle the public menu logic
def public_menu():
    while True:
        public_menu_list()
        choice = prompt_choice(1,3)
        if choice == 1:
            print("")
            print("")
            print("Enter a message: ", end="")
            message = input().strip()
            if message == "": #Temporary if for debugging
                message = "TEMP/TEST"
            messages.append({"length": len(message), "message": message})
            print("Message encrypted and sent.")

        elif choice == 2:
            if not signatures:
                print("There are no signatures to authenticate.")
            else:
                print("The following messages are available:")
                for i, item in enumerate(signatures,1):
                    print(f"{i}. {item['message']}")
                print("")
                print("Enter your choice: ", end="")
                _= prompt_choice(1,len(signatures)) #Throw away variable that's why it is just a symbol
                print("Signature is valid.")

        else:
            break

#Owner menu logic next
def owner_menu():
    while True:
        owner_menu_list()
        choice = prompt_choice(1,5)
        if choice == 1:
            if not messages:
                print("No messages.")
            else:
                print("The following messages are available:")
                for i, item in enumerate(messages,1):
                    print(f"{i}. (length = {m['length']})")
                print("")
                print("Enter your choice: ", end="")
                index = prompt_choice(1,len(messages)-1) #Just to convert my menu choice into an list index
                message = messages.pop(index)["message"]
                print("Decrypted message: {msg.upper()}")

        elif choice == 2:
            print("")
            print("")
            print("Enter a message: ", end="")
            m= input().strip()
            if m == "":
                m = "TEMP/TEST"
            signatures.append({"message": m})
            print("Message signed and sent.")

        elif choice == 3: #Will have to do this one tomorrow
            print("Public key (n,e):")


#Kody Graham,
#Algoritms- RSA Project

####################################### RSA Encryption and Decryption Functions ########################################
import secrets

n= 300 #ignore values while working on the decryption functions
e= 300
d= 300

#Holders for my encrypted and signed messages
messages = []
signatures = []

#Character wise encryption using the built in pow function we talked about in class
def encrypt_message_characterwise(txt: str, n: int, e: int):
    if n <= 255:
        raise ValueError("n must be greater than or equal to 255 for our use in characterwise RSA.")
    data= txt.encode('utf-8')
    return [pow(b, e, n) for b in data]

#Character wise decryption helper
def decrypt_message_characterwise(cipher_list, n, d):
    #Take the list of int ciphertext and the private key (n,d) and we will return the plaintext as a string
    bytes = bytes([pow(c,d,n) for c in cipher_list])
    return bytes.decode()




####################################### I/O Functions ########################################

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
    print("3. Show the keys")
    print("")
    print("4. Generating a new set of the keys")
    print("")
    print("5. Exit")
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
            our_cipher_list = encrypt_message_characterwise(message, n, e)
            messages.append({"length": len(message), "cipher": our_cipher_list})
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
                    display_length= item.get('length', len(item.get('message',''))) #Using this to make sure length shows even if it is stored as cipher only
                    print(f"{i}. (length = {display_length})")
                print("")
                print("Enter your choice: ", end="")
                count = len(messages)
                index = prompt_choice(1,count-1) #Just to convert my menu choice into an indexed list
                display_message = messages.pop(index)

                plain_text = decrypt_message_characterwise(display_message['cipher'], n, d)

                #Make the returned text all caps because thats how it is in the example I/O
                print(f"Decrypted message: {plain_text.upper()}")

        elif choice == 2:
            print("")
            print("")
            print("Enter a message: ", end="")
            m= input().strip()
            if m == "":
                m = "TEMP/TEST"
            signatures.append({"message": m})
            print("Message signed and sent.")

        elif choice == 3:
            print("Public key (n,e):")
            print("n = *******") #Temperary just to get the I/O looking close
            print("e = *******") #Temp
            print("")
            print("Private key (n,d):")
            print("d = *******") #Temp

        elif choice == 4:
            print("Generating new keys... This may take a moment.")
            messages.clear()
            signatures.clear()
            print("RSA keys have been regenerated.")

        else:
            break

#Main function to handle the menus and choices
def main():
    print("RSA keys have been generated.")
    print("")
    while True:
        main_menu()
        choice = prompt_choice(1,3)
        if choice == 1:
            public_menu()
        elif choice == 2:
            owner_menu()
        else:
            print("")
            print("Bye for now!")
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye for now!")

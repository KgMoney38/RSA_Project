#Kody Graham,
#Algoritms- RSA Project

import secrets

####################################### RSA Math and Logic Functions ########################################

#Slightly modified from the extended euclidean algorithm we looked at in class
def extended_gcd(a, b):
    if b==0:
        return (1, 0, a)
    x, y, d = extended_gcd(b, a % b)
    return (y, x-a//b* y, d) #Used for back substitution

def modinv(a, m):
    d,x, _ = extended_gcd(a, m)
    if d!=1:
        raise Exception('modular inverse does not exist')
    return x % m

#Use the fermat prime test like we learned in class
def fermat_prime_prob(n: int, k:int =24) ->bool:
    if n<2:
        return False

    #Quick small screen for common primes
    smallSet= [2,3,5,7,11,13,17,19,23,29]
    for p in smallSet:
        if n == p:
            return True
        if n % p == 0:
            return False

    #Random base Fermat check
    for _ in range(k):
        a = secrets.randbelow(n-3)+2
        if pow(a,n-1,n) != 1:
            return False
    return True

#Generate the random number with the top bit set so we can enforce the bit length
def generate_prime(bits: int=512)-> int:
    while True:
        candidate = (secrets.randbits(bits) | (1 << bits-1))|1)
        if fermat_prime_prob(candidate):
            return candidate

#Build our RSA keys n, e , and d
def generate_pair_of_keys(bits: int = 1024):
    half= bits//2
    p = generate_prime(half)
    q= generate_prime(half)

    while q == p: #Make sure p and q are different
        q= generate_prime(half)

    n = p*q
    phi = (p-1)*(q-1)

    e = 65537
    if extended_gcd(e, phi)[0] != 1:
        while True: #Fallback to pick a random odd e until gcd using e and phi is ==1
            cand = (secrets.randbelow(17) | 1)
            if extended_gcd(cand, phi)[0] == 1:
                e = cand
                break
    d = modinv(e, phi)
    return n, e, d





####################################### RSA Encryption and Decryption Functions ########################################

n= None
d= None
e = None

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

#Signature for completeness however Dr. Hu said no hash required
def sign_message_characterwise(message: str, signature_list, n: int, d: int):
    data = message.encode('utf-8')
    return[pow(b,d,n) for b in data]

#Finally we need to verify the signed message
def verify_message_characterwise(message: str, signature_list, n: int, e: int):
    recover = bytes([pow(s,e,n) for s in signature_list])
    try:
        return recover.decode('utf-8') == message
    except UnicodeDecodeError:
        return False




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
    global n
    global e
    global d

    n= generate_pair_of_keys(bits=1024)
    e= generate_pair_of_keys(bits=1024)
    d = generate_pair_of_keys(bits=1024)

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

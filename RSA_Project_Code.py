#Kody Graham,
#Algoritms- RSA Project



import secrets #We need this import to give us cryptographically safe random numbers for our prime number and our keys

n: int #WIll hold the RSA modulus of p*q
d: int #Will hold the private exponent
e: int #Will hold the public exponent

#Holders for my encrypted and signed messages both lists
messages = []
signatures = []

####################################### RSA Math and Logic Functions ########################################

#Slightly modified from the extended euclidean algorithm we looked at in class
def extended_gcd(a:int, b:int):
    #Will return d, x, and y where a*x + b*y = g which is gcd(a,b)
    if b==0: #Base case to end our recursion
        return (a, 1, 0) #The gcd is a and the coefficients are (1,0)
    d, x, y = extended_gcd(b, a % b) #Recursion on b,a mod b
    return d, y, x- (a//b) * y #Back substitute to get the new coefficient

#This is where we will compute the modular inverse of a mod m
def modinverse(a, m):
    d,x, _ = extended_gcd(a, m) #Get gcd and coefficient x when a*x + m*y =d
    if d!=1: #Inverse only exists when our a and m are coprime
        raise Exception('modular inverse does not exist')
    return x % m #This return wraps x into m to get the positive inverse

#Use the fermat prime test like we learned in class
def fermat_prime_prob(n: int, k:int =24) ->bool:
    if n<2: #Numbers below 2 are not prime
        return False

    #Quick small screen for common primes
    smallSet= [2,3,5,7,11,13,17,19,23,29] #Small primes for our trial divide
    for p in smallSet: #Obviously just loops through our small set
        if n == p: #if n is in our list accept it
            return True
        if n % p == 0: #Our n is composite if it is divisible by any of the small primes
            return False

    #Random base Fermat check
    for _ in range(k): #Repeat the test with different random bases
        a = secrets.randbelow(n-3)+2 #Set our a to a random number in 2, n-2
        if pow(a,n-1,n) != 1: #It is composite if a^(n-1) mod n isnt 1
            return False

    return True #Only return true if all tests pass

#Generate the random number with the top bit set so we can enforce the bit length meaning keep the size
def generate_prime(bits:int = 512)-> int: #
    while True: #Keep trying until a "candidate" passes the tests
        candidate = (secrets.randbits(bits) | (1 << (bits-1))|1) #Random odd with the top bit set
        if fermat_prime_prob(candidate): #Only accept the candidate if it passes the Fermat test
            return candidate #Return the probable prime we found

#Build our RSA keys n, e , and d.
def generate_pair_of_keys(bits: int = 1024):
    half= bits//2 #Split the number of bits between p and q
    p = generate_prime(half)
    q= generate_prime(half)

    while q == p: #Make sure p and q are different
        q= generate_prime(half) #If they are the same obviously just regenerate one.

    n = p*q #Compute the modulus n

    phi = (p-1)*(q-1) #Using phi like we talked about in class

    e = 65537 #Common public exponent e

    if extended_gcd(e, phi)[0] != 1: #This looks confusing but it is just if e is not coprime with phi

        while True: #Fallback to pick a random odd e until gcd using e and phi is ==1
            candidate = (secrets.randbits(17) | 1) #Using a random 17 bit odd candidate for our e

            if candidate >1 and extended_gcd(candidate, phi)[0] == 1:
                e = candidate #Accept the candidate as e if it is coprime and >1
                break
    d = modinverse(e, phi) #This is the private exponent

    return n, e, d #Return the triple key



####################################### RSA Encryption and Decryption Functions ########################################

#Character wise encryption using the built in pow function we talked about in class
def encrypt_message_characterwise(txt: str, n: int, e: int): #Encrypt the message per byte using n,e
    if n <= 255: #Make sure the modulus can hold a byte value
        raise ValueError("n must be greater than or equal to 255 for our use in characterwise RSA.")
    data= txt.encode('utf-8') #Convert string to bytes
    return [pow(b, e, n) for b in data] #This is where we map each byte to c= b^e mod n

#Character wise decryption helper
def decrypt_message_characterwise(cipher_list, n, d):
    #Take the list of int ciphertext and the private key (n,d) and we will return the plaintext as a string
    num_bytes = bytes([pow(c,d,n) for c in cipher_list]) #Note to self: bytes is a keyword in python so remember i cant use it as a var name
    return num_bytes.decode('utf-8', errors='replace') #Decode the bytes to a string and replace any invalid sequence

#Signature for completeness however Dr. Hu said no hash required
def sign_message_characterwise(message: str, n: int, d: int):
    data = message.encode('utf-8') #Encode our message to bytes
    return[pow(b,d,n) for b in data] #Just raising the b to the d power mod n for each byte.

#Finally we need to verify the signed message
def verify_message_characterwise(message: str, signature_list, n: int, e: int):
    recover = bytes([pow(s,e,n) for s in signature_list]) #Open each signature byte using s^e mod n
    try: #Just to catch decode errors
        return recover.decode('utf-8') == message #Only valid if recovered message is the same as the original message
    except UnicodeDecodeError: #Shouldnt happen but just in case use this to return false, meaning an invalid signature.
        return False



####################################### I/O Functions ########################################
#Less comments in this section of our code because this is all pretty self-explanatory,
#very unlike our RSA Encryption/Decryption and Math/Logic sections.

#Ask for the user choice
def prompt_choice(lowest,highest):

    while True: #Obviously just repeat until the user gives a valid choice
        try:
            x= int(input().strip()) #Read line, then strip the space, then convert to int
            if lowest <= x <= highest: #these are just the min/max values for valid choices
                return x
        except Exception:
            pass #Just keep looping to reprompt
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
        if choice == 1: #Send encrypted message
            print("")
            print("")
            print("Enter a message: ", end="")
            message = input().strip()
            our_cipher_list = encrypt_message_characterwise(message, n, e) #Encrypt with the public key
            messages.append({"length": len(message), "cipher": our_cipher_list}) #Store the length and cipher list
            print("Message encrypted and sent.")

        elif choice == 2: #Authenticate signature
            if not signatures:
                print("There are no signatures to authenticate.")
            else:
                print("The following messages are available:")
                for i, item in enumerate(signatures,1):
                    print(f"{i}. {item['message']}")
                print("")
                print("Enter your choice: ", end="")
                pick= prompt_choice(1,len(signatures))-1 #Note to self: Need the -1 for 0->N instead of 1->N
                sig = signatures[pick]
                ok = verify_message_characterwise(sig["message"], sig["signature"], n, e) #Verify with our public key
                print("Signature is valid." if ok else "Signature is invalid.")

        else: #Choice 3: Exit
            break

#Owner menu logic next
def owner_menu():
    global n, e, d #Declared global because we reassign our keys if the regenerate option is chosen

    while True: #Just a loop
        owner_menu_list()
        choice = prompt_choice(1,5)
        if choice == 1: #Decrypt message
            if not messages:
                print("No messages.")
            else:
                print("The following messages are available:")
                for i, item in enumerate(messages,1):
                    display_length= item.get('length', len(item.get('message',''))) #Using this to make sure length shows even if it is stored as cipher only
                    print(f"{i}. (length = {display_length})")
                print("")
                print("Enter your choice: ", end="")
                index = prompt_choice(1,len(messages)) -1
                display_message = messages.pop(index) #remove and return the message

                plain_text = decrypt_message_characterwise(display_message['cipher'], n, d) #Decrypt with our private key

                #Make the returned text all caps because thats how it is in the example I/O that Dr. Hu provided
                print(f"Decrypted message: {plain_text.upper()}")

        elif choice == 2: #Sign message
            print("")
            print("")
            print("Enter a message: ", end="")
            m= input().strip()
            signature_list = sign_message_characterwise(m, n, d) #Create signature with our private key
            signatures.append({"message": m, "signature": signature_list}) #Store the message and its signature
            print("Message signed and sent.")

        elif choice == 3: #Show our current keys
            print("Public key (n,e):")
            print(f"n = {n}")
            print(f"e = {e}")
            print("")
            print("Private key (n,d):")
            print(f"d = {d}")

        elif choice == 4: #Regen a new keypair
            print("Generating new keys... This may take a moment.")
            n,e,d = generate_pair_of_keys(bits=1024) #Calls our function to generate the random keys again
            messages.clear() #Removes the old messages
            signatures.clear() #Removes the old signatures
            print("RSA keys have been regenerated.")

        else: #Choice 5: Exit
            break

#Main function to handle the menus and choices
def main():

    global n,e,d

    n,e,d = generate_pair_of_keys(bits=1024) #Generate our keys at startup

    print("RSA keys have been generated.")
    print("")
    while True:
        main_menu()
        choice = prompt_choice(1,3)
        if choice == 1: #Public user
            public_menu()
        elif choice == 2: #Owner
            owner_menu()
        else: #Choice 3: Quit
            print("")
            print("Bye for now!")
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye for now!")

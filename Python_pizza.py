# 🚨 Don't change the code below 👇
print("Welcome to Python Pizza Deliveries!")
size = input("What size pizza do you want? S, M, or L ")
add_pepperoni = input("Do you want pepperoni? Y or N ")
extra_cheese = input("Do you want extra cheese? Y or N ")
# 🚨 Don't change the code above 👆
small = 15
medium = 20
large = 25
pepsmall = 2
pepmedL = 3
extra = 1
#Write your code below this line 👇
if size == "S" and add_pepperoni == "Y" and extra_cheese =="Y":
    print(f"Your final bill is: ${small+pepsmall+extra}.")
if size == "S" and add_pepperoni == "Y" and extra_cheese =="N":
    print(f"Your final bill is: ${small+pepsmall}.")
if size == "S" and add_pepperoni == "N" and extra_cheese =="Y":
    print(f"Your final bill is: ${small+extra}.")
if size == "S" and add_pepperoni == "N" and extra_cheese =="N":
    print(f"Your final bill is: ${small}.")
if size == "M" and add_pepperoni == "Y" and extra_cheese =="Y":
    print(f"Your final bill is: ${medium+pepmedL+extra}.")
if size == "M" and add_pepperoni == "Y" and extra_cheese =="N":
    print(f"Your final bill is: ${medium+pepmedL}.")
if size == "M" and add_pepperoni == "N" and extra_cheese =="Y":
    print(f"Your final bill is: ${medium+extra}.")
if size == "M" and add_pepperoni == "N" and extra_cheese =="N":
    print(f"Your final bill is: ${medium}.")
if size == "L" and add_pepperoni == "Y" and extra_cheese =="Y":
    print(f"Your final bill is: ${large+pepmedL+extra}.")
if size == "L" and add_pepperoni == "Y" and extra_cheese =="N":
    print(f"Your final bill is: ${large+pepmedL}.")
if size == "L" and add_pepperoni == "N" and extra_cheese =="Y":
    print(f"Your final bill is: ${large+extra}.")
if size == "L" and add_pepperoni == "N" and extra_cheese =="N":
    print(f"Your final bill is: ${large}.")
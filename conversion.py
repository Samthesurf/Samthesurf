CAD_to_Naira = 450
Naira_to_CAD = 1 / 450


def conversion(naira):
    if naira > 0:
        return f"{naira} naira is {naira * Naira_to_CAD} dollars\nWhat a life!"
    elif naira == 0:
        return f"stop right there, 0 is obviously 0, input a positive value"
    else:
        return f"so you are owing the bank money? go and pay them back!"
def naira_conf():
    if naira_value.isdigit():
        naira_v = int(naira_value)

def convert(cad):
    if cad >= 0:
        return f"{cad} dollars is {cad * CAD_to_Naira} Naira\nWhat can we do?"
    elif cad == 0:
        return f'pfft, you poor person, go and do some work'
    else:
        return f"stop right there, go and pay the bank their money or it will increase monthly"


user_input = input("Put the dollar value you want to convert\n")
if user_input.isdigit():
    num_ber = int(user_input)
    ans_wer = convert(num_ber)
    print(ans_wer)
elif user_input.isdecimal():
    print("my function is for whole numbers")
else:
    print("stop this nonsense!")

user_inputs = input("Put the naira value you want to convert\n")
num_bers = int(user_inputs)
ans_wers = conversion(num_bers)
print(ans_wers)

naira_value = input()
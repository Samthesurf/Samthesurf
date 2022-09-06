import random
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇
gesture = int(input('What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.'))
if gesture == 0:
  print(rock)
elif gesture == 1:
  print(paper)
else:
  print(scissors)
choice1 = [rock, paper, scissors]
compchoice = random.choice(choice1)
print(compchoice)

if gesture == 0 and compchoice == choice1[0]:
  print("It's a draw")
elif gesture == 0 and compchoice == choice1[1]:
  print("You lose")
elif gesture == 0 and compchoice == choice1[2]:
  print('I win')
  
if gesture == 1 and compchoice == choice1[0]:
  print("I win")
elif gesture == 1 and compchoice == choice1[1]:
  print("It's a draw")
elif gesture == 1 and compchoice == choice1[2]:
  print("You lose")
  
if gesture == 2 and compchoice == choice1[0]:
  print("You lose")
elif gesture == 2 and compchoice == choice1[1]:
  print("I win")
elif gesture == 2 and compchoice == choice1[2]:
  print("It's a draw")
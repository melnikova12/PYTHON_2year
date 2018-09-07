import random

letters = 'abcdefghijklmnopqrstuvwxyz'

#выбирает рандомную букву и приписывает ей сразу же номер 
letter = letters[random.randint(0,25)]

#игровой цикл 
while True:
    #предлагает угадать (вписать) букву 
    guess = input("Type a lower-case letter: ")
    
    #проверяет, что пользователь ввел именно букву (не заглавную)
    #проверяет то, что то, что ввел пользователь есть в letters
    if guess not in letters:
        print("That is not a lower-case letter.")
        continue
    #если все правильно: 
    if guess == letter:
        print("That’s right!")
        break
    #подсказка, если не угадали
    if guess > letter:
        print("It’s earlier in the alphabet.")
    else:
        print("It’s later in the alphabet.")

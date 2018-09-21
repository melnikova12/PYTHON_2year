#ВАЖНЫЙ КОММЕНТАРИЙ:частично этот код писался с Дианой Горган (группа 1) 

import random
Number_of_tries = 5

print ('Привет! Давай поиграем в "Виселицу"!')

def beginning():
    rules = input ('Если вы хотите узнать правила, введите "да": ')
    if rules == "да":
        print ('Вы должны угадать слово из выбранной темы за 5 попыток')
    else:
        print ('Ну правила все-таки надо узнать - вы должны угадать слово из выбранной вами темы за 5 попыток')

    
    theme_choosing = input('Чтобы перейти к ознакомлению с темами, введи "темы": ')
    if theme_choosing == "темы":
        print("тема №1 - животные; тема №2 - города России;тема №3 - страны")
    else:
        print("Все равно познакомлю с темами: тема №1 - животные; тема №2 - города России;тема №3 - страны")


    rules2 = input ("ОЧЕНЬ ВАЖНЫЕ НЮАНСЫ - чтобы узнать о них, введи 'нюансы': ")
    if rules2 == "нюансы":
        print('все слова загаданы в единственном числе + вводить можно только строчные буквы')
    else:
        print('все равно вот нюансы - все слова загаданы в единственном числе + вводить можно только строчные буквы')
            
 
def theme():   
    theme_asking = input ('Введите номер выбранной темы ("1","2" или "3"): ')
    if theme_asking == '1':
        file = '1.txt' #если пользователь ввел 1, то программа берет файл 1
    elif theme_asking == '2':
        file = '2.txt'
    else:
        file = '3.txt'
    return file


def open_file():
    file = theme()
    with open (file, encoding = 'utf-8') as f:
        words = f.read().lower()
    words = words.split('\n') #текст - отдельные слова
    word = random.choice(words)
    return word


def working_with_word(word): #обрабатываю слово
    unknown_word = ['_' for i in range(len(word))]
    print (' '.join(unknown_word)) #на выходе теперь строка, а не список (убрались кавычки)
    return unknown_word


def letters (unknown_word, word):
    human = human_file()
    while '_' in unknown_word: #цикл для того, чтобы игра не остановливалась после одной попытки
        letter = input('Введите букву: ').lower()
        if letter in word:
            for i in range (len(word)):       #сравниваем букву с каждым элементом
                if letter == word[i]:
                    unknown_word[i] = letter        
            print('Поздравляем, вы угадали букву!')
            print (' '.join(unknown_word))
        else:
            print ('Вы не угадали букву :(')
            global Number_of_tries
            Number_of_tries = Number_of_tries - 1
            print ('Количество оставшихся попыток: {} '.format(Number_of_tries))
            print (human[5-Number_of_tries])
        if Number_of_tries == 0:
            print ('К сожалению, вы проиграли!')
            break


def human_file(): #работаю с файлом с картинками, создаю массив 
    with open ("human.txt", encoding = 'utf-8') as f:
        human = f.read()
        human = human.split('\n\n')
        return human


#итоговая функция,в которой по кускам собираем игру             
def main():
    beginning()
    word = open_file()
    unknown_word = working_with_word(word)
    letters(unknown_word, word)

main()
    



    
    
            


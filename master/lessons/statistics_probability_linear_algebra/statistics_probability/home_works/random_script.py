from random import randint

number_of_questions = 7
number_of_members = 3
counter_members = number_of_members * [0]
divide_questions_array = number_of_questions * [None]
while (counter_members[0] != number_of_questions // 3) and \
       (counter_members[1] != number_of_questions // 3) and \
       (counter_members[2] != (number_of_questions // 3)+1):
    counter_members = number_of_members * [0]
    for i in range(number_of_questions):
        solver = randint(0, number_of_members-1)
        counter_members[solver] += 1
        divide_questions_array[i] = solver

print(divide_questions_array)

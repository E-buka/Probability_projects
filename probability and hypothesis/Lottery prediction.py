
#### 6/49 Lottery Ticket Probability 

import pandas as pd

def factorial(n):
    total = 1
    for i in range(n, 0, -1):
        total *= i 
    return total

def combinations(n, k): 
    n_factorial = factorial(n)
    k_factorial = factorial(k)
    n_less_k_factorial = factorial(n-k)
    return n_factorial/(k_factorial * n_less_k_factorial)


# Probability of winning with one ticket. 

def one_ticket_probability(): 
    """
    A ticket has six numbers between 1-49 taken without replacement
    To win a big prize, a playing ticket must match the six numbers drawn
    """
    total_combinations = combinations(49, 6) 
    successful_outcome = 1 # every ticket will match only one possible combination
    percent_probability = (successful_outcome / total_combinations)*100
    message = "Hi there! \nYou have %.7f%% chance of winning the big price with one ticket" % percent_probability
    return message
    

print(one_ticket_probability())


# Exploring historical winning numbers 


# Users can explore historical data to determine whether they would have ever won
# The csv data below contains all historical big prize winning number sets from 1982 to 
# 2018 in Canada https://www.kaggle.com/datasets/datascienceai/lottery-dataset.

df = pd.read_csv("649.csv")
print(df.head())


#generating the set of all winning numbers from historical 

winning_numbers = df.apply(lambda row: set(row.iloc[4:10]), axis=1)

def check_historical_occurence(ticket_numbers, winning_numbers):
    """The function checks the users winning set against historical 
    winning set and prints how many times that has occurred"""
    
    user_set = set(ticket_numbers)
    times_won = winning_numbers == user_set
    total_times_won = sum(times_won)
    message = f"Hi there!!! Your winning number combination has occurred as a winning set {total_times_won} times"  
    return message



set1 = [1,6,23,24,27,39,]
set2 = [23, 17, 3, 49, 30, 10]
set3 = [5, 14, 21, 31, 34, 47]

print(check_historical_occurence(set3, winning_numbers))



def multi_ticket_probability(total_tickets):
    """
    This checks the probability of winning with multiple tickets
    """
    total_outcome = combinations(49, 6)
    successful_outcome = total_tickets
    probability = (successful_outcome/total_outcome)*100
    message = "Hi there! \nYou have %.7f%% chance of winning the big price with your ticket" % probability
    return message


number_of_tickets = [1, 10, 100, 10000, 1000000, 6991908, 13983816]

for number in number_of_tickets:
    print(multi_ticket_probability(number))


def probability_less_6(no_of_winning):
    """This function calculates the probability of having 2 to 5
    winning numbers in a player's ticket"""
    
    total_combinations = combinations(6, no_of_winning) # total combinations of correct winning number
    no_remaining_combinations = combinations(43, 6-no_of_winning) #remaining combinations of remaining 43 & 6 ticket no
    total_successful_outcome = total_combinations * no_remaining_combinations 
    probability = total_successful_outcome/combinations(49, 6)
    message = f"Hi there! \nWith {no_of_winning} numbers, you have {probability*100:.5f}% chance of winning"
    return message


winning_set = [2, 3, 4, 5]

for number in winning_set:
    print(probability_less_6(number))
    print('------------------\n')


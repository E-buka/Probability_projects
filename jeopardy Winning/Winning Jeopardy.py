import pandas as pd 
import re
from scipy.stats import chisquare
import numpy as np

jeopardy = pd.read_csv('jeopardy.csv')

print(jeopardy.shape)
jeopardy.head()

print(jeopardy.columns)

jeopardy.rename({'Show Number' : 'Show_number', ' Air Date' : 'Air_date', ' Round' :'Round', 
                ' Category': 'Category', ' Value': 'Value', ' Question': 'Question', ' Answer': 'Answer'}, axis=1, inplace=True)

print(jeopardy.columns)


def normalize(message):
    message = message.lower()
    message = re.sub(r'[^A-Za-z0-9\s]', '', message)
    message = re.sub(r'\s+' , ' ', message)
    return message


jeopardy['clean_question'] = jeopardy['Question'].apply(normalize)
jeopardy['clean_answer']  = jeopardy['Answer'].apply(normalize)


def clean_convert(message):
    message = str(message)
    message = re.sub(r'[^A-Za-z0-9\s]', '', message)
    try:
        value = int(message)
    except Exception:
        value = 0 
    return value

jeopardy['clean_value'] = jeopardy['Value'].apply(clean_convert)

jeopardy['Air_date'] = pd.to_datetime(jeopardy['Air_date'], errors='coerce') 

print(jeopardy.dtypes)

## How often the answer can be used for a question 

def answer_in_question(row):
    split_answer = row['clean_answer'].split()
    split_question = row['clean_question'].split()
    match_count = 0 
    if 'the' in split_answer:
        split_answer.remove('the') 
    if len(split_answer)==0:
        return 0        
    for txt in split_answer:
        if txt in split_question:
            match_count += 1 

    return match_count/len(split_answer)


#applying the function above to find out how many times answers are used in question
# and their fraction in the total words of the answer

jeopardy['answer_in_question'] = jeopardy.apply(answer_in_question, axis=1)

## finding the mean of the answer_in_question column
## this will give indication of how likely an answer is to be in question

mean_answer_in_question = jeopardy['answer_in_question'].mean()
print(mean_answer_in_question)

## Investigating recycled questions. 
## sorting the dataframe by the air_date column in order to investigate recycled questions

question_overlap = []
terms_used = set()

jeopardy = jeopardy.sort_values(by=['Air_date'], axis=0)

for row in jeopardy.iterrows():
    row = row[1]
    split_question = row['clean_question'].split(' ')
    split_question = [word for word in split_question if len(word) >=6]
    match_count = 0 
    for word in split_question:
        if word in terms_used:
            match_count +=1
        terms_used.add(word)
    if len(split_question) > 0:
        match_count = match_count/len(split_question)
    question_overlap.append(match_count)    
 
jeopardy['question_overlap'] = question_overlap

jeopardy['question_overlap'].mean()

## Low versus high value  questions 

def low_vs_high(row):
    if row['clean_value'] > 800:
        value = 1
    else:
        value = 0 
    return value

jeopardy['high_value'] = jeopardy.apply(low_vs_high, axis = 1)


def word_count(word):
    low_count = 0 
    high_count = 0 
    for row in jeopardy.iterrows():
        row = row[1]
        split_question = row['clean_question'].split(' ')
        if word in split_question:
            if row['high_value'] == 1:
                high_count += 1
            else:
                low_count += 1
    return high_count, low_count 


comparison_terms = iter(terms_used)
observed_expected = []

for _ in range(10):
    observed_expected.append(word_count(next(comparison_terms)))
    
print(observed_expected)


##  Applying Chi-square test

high_value = jeopardy['high_value']==1
high_value_count = high_value.sum()

low_value = jeopardy['high_value']==0
low_value_count = low_value.sum()

chi_squared = []

for item in observed_expected:
    total = sum(item)
    total_prop = total / jeopardy.shape[0]
    expected_high = total_prop * high_value_count
    expected_low = total_prop * low_value_count

    observed = np.array([item[0], item[1]])
    expected = np.array([expected_high, expected_low])
    chi_squared.append(chisquare(observed, expected))

print(chi_squared)


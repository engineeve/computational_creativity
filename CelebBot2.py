import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pandas as pd
import numpy as np
import string
import math

data = pd.read_excel("Veale.xlsx",  encoding='utf8')


data = data.replace({'"':''}, regex=True)
df = np.array(data)

# ============ Functions to convert data to JSON format ===========

# adds inverted commas to strings in list
def format_to_string(column):
    attributes = []
    for j in column:
        j = str(' "%s" '%(j))
        attributes.append(j)
    return attributes

# Removes brackets and adds commas between elements
def format_list(list,list_name):
    #rule_name = "%s" % (list_name)
    rule_values = '[%s]' % ', '.join(map(str, list) )
    #rule = ' "%s" : %s ,' %(rule_name,rule_values)
    return rule_values

# Removes punctuation from raw data
def remove_punctuation(data_col):
    for i, word in zip(range(len(data_col)), data_col):
        allowed = {",", " ", "-"}.union(string.ascii_lowercase).union(string.ascii_uppercase).union(string.digits)
        filtered_word = "".join([letter for letter in word if letter in allowed])
        data_col[i] = filtered_word
    return data_col


# New Film
non_fictional_actor =[]
fictional = []
pretty_char=[]
ugly_char=[]
intelectual_char =[]
stupid_char = []
sadistic_char =[]
sensitive_char=[]
opponent_rule = []
date_rule =[]
fight_rule = []
villan=[]
hero=[]
fictional_female=[]
fictional_male=[]
non_fictional_male_actor=[]
non_fictional_female_actor=[]
non_fictional=[]
non_fictional_male=[]
non_fictional_female=[]
ugly_char_male=[]
ugly_char_female=[]
pretty_char_male=[]
pretty_char_female=[]


for i in df:

    if pd.isnull(i[23]) == False:
        # Convert ascii to list
        as_list = [x.strip() for x in i[23].split(',')]
        if list(set(['pretty','elegant','sultry' ,'beautiful', 'sexy','attractive', 'slim','handsome','strong','muscular']).intersection(as_list))!=[]:
            pretty_char.append(i[0])
            if 'female' == i[2]:
                pretty_char_female.append(i[0])
            if 'male' == i[2]:
                pretty_char_male.append(i[0])
        if list(set(['intelligent', 'smart','clever' ,'well-educated','super-intelligent','scientific','educated','logical']).intersection(as_list)) != []:
            intelectual_char.append(i[0])
        if list(set(['sensitive', 'romantic', 'sweet', 'loveable', 'heartwarming', 'adorable', 'angelic','creative,']).intersection(as_list)) != []:
            if i[15] != 'fictional':
                sensitive_char.append(i[0])

    if pd.isnull(i[22]) == False:
        as_list = [x.strip() for x in i[22].split(',')]
        if list(set(['disgusting', 'gelatinous', 'ugly', 'flabby']).intersection(as_list)) != []:
            if 'female' == i[2]:
                ugly_char_female.append(i[0])
            if 'male' == i[2]:
                ugly_char_male.append(i[0])
        if list(set(['dumb', 'inarticulate',  'unthinking', 'stupid','unintelligent', 'dim-witted','air-headed']).intersection(as_list)) != []:
            stupid_char.append(i[0])
        if list(set(['evil', 'malicious', 'cruel', 'power-hungry' ]).intersection(as_list)) != []:
            sadistic_char.append(i[0])
            if pd.isnull(i[9]) == False:
                activity_list = [x.strip() for x in i[9].split(',')]
                statement = str('"Are you lonely, looking for love, do you like %s, I hear %s is single" ' % (activity_list[0], i[0]))
                date_rule.append(statement)

    if pd.isnull(i[21]) == False:
        as_list = [x.strip() for x in i[21].split(',')]
        if list(set(['Crime Fighter', 'Superhero','Hero','Heroine']).intersection(as_list)) != []:
            hero.append(i[0])
        if list(set(['Crimeboss','Henchman','Serial Killer','Killer','Terrorist','Tyrant,','Villain','Traitor','Thug']).intersection(as_list)) != []:
            villan.append(i[0])

    if pd.isnull(i[8]) == False:
        as_list = [x.strip() for x in i[8].split(',')]
        statement = str(' "From the wise words of %s, keep your friends close, but %s even closer" '%(i[0],as_list[0] ))
        opponent_rule.append(statement)
        statement = str('"News from %s, fight breaks out between %s and %s, a %s seen fleeing the scene" ' % (i[4],i[0], as_list[0],i[10]))
        fight_rule.append(statement)
        print statement

    if 'fictional' == i[15]:
        fictional.append(i[0])
        if 'female' == i[2]:
            fictional_female.append(i[0])
        if 'male' == i[2]:
            fictional_male.append(i[0])

    if i[15] != 'fictional':
        non_fictional.append(i[0])
        if 'Acting' in i[13]:
            if 'female' == i[2]:
                non_fictional_female_actor.append(i[0])
            if 'male' == i[2]:
                non_fictional_male_actor.append(i[0])
            non_fictional_actor.append(i[0])

        if 'male' == i[2]:
            non_fictional_male.append(i[0])
        if 'female' == i[2]:
            non_fictional_female.append(i[0])


# Format to tracery rules
def tracery_format(rule,expansion):
    expansion = remove_punctuation(expansion)
    expansion = format_to_string(expansion)
    expansion = format_list(expansion, rule)
    new_rule = str(' "%s" : %s ,     ' %(rule,expansion))
    text_file.write(new_rule + '\n')


print date_rule

text_file = open("Output.txt", "w")
tracery_format('non_fictional_character_actor', non_fictional_actor)
tracery_format('fictional_character', fictional)
tracery_format('pretty_character', pretty_char)
tracery_format('ugly_character', ugly_char)
tracery_format('stupid_character', stupid_char)
tracery_format('villans', villan)
tracery_format('heros', hero)
tracery_format('intellectual_character', intelectual_char)
tracery_format('sadistic_character', sadistic_char)
tracery_format('sensitive_character', sensitive_char)
tracery_format('date_rule',date_rule)
tracery_format('fight_rule',fight_rule)
tracery_format('opponent_rule',opponent_rule)
tracery_format('non_fictional_character', non_fictional)
tracery_format('fictional_female',fictional_female)
tracery_format('fictional_male',fictional_male)
tracery_format('non_fictional_female_actor',non_fictional_female_actor)
tracery_format('non_fictional_male_actor',non_fictional_male_actor)
tracery_format('ugly_char_female',ugly_char_female)
tracery_format('ugly_char_male',ugly_char_male)
tracery_format('pretty_char_female',pretty_char_female)
tracery_format('pretty_char_male',pretty_char_male)
tracery_format('non_fictional_female',non_fictional_female)
tracery_format('non_fictional_male',non_fictional_male)
text_file.close()









import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pandas as pd
import numpy as np
import string

data = pd.read_excel("NOC_list_Niamh_Version.xlsx",  encoding='utf8')


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
    rule_name = "%s" % (list_name)
    rule_values = '[%s]' % ', '.join(map(str, list) )
    rule = ' "%s" : %s ,' %(rule_name,rule_values)
    return rule

# Removes punctuation from raw data
def remove_punctuation(data_col):
    for i, word in zip(range(len(data_col)), data_col):
        allowed = {",", " ", "-"}.union(string.ascii_lowercase).union(string.ascii_uppercase).union(string.digits)
        filtered_word = "".join([letter for letter in word if letter in allowed])
        data_col[i] = filtered_word
    return data_col



# ======================= CHaracter Bot =============================
# Columns to use
talking_points_col = remove_punctuation(df[:,23])
typical_activity_col = remove_punctuation(df[:,9])
character_col = remove_punctuation(df[:,0])

important_cols = [talking_points_col,typical_activity_col,character_col]
cols_names = ["Talking Points","Typical Activity","Character Name"]



# Initialize lists to hold names
rule_names=[]
# Holds rules that only contain non terminals
total_rule = []
# Holds the rule that combines "Talking Points"and"Typical Activity" of character
total_character_rules = []



# Create Rules
for i in range(len(df)):
    character_rule_temp = []
    for k in range(0, 2):
        attribute_col = important_cols[k]
        column = attribute_col[i].split(",")
        attributes = format_to_string(column)
        rule_name = str('%s %s'% ( df[i,0] , cols_names[k]))
        rules = format_list(attributes,rule_name)
        rule_names.append(rule_name)
        total_rule.append(rules)
        character_rule_temp.append(rule_name)
    character_rule = str(' "Someone tell #%s# %s #%s#" '%(character_rule_temp[0],character_col[i],character_rule_temp[1] ))
    total_character_rules.append(character_rule)



sub_list_lenght = len(total_character_rules)/2
# Split characters randomly into two groups
characterA = total_character_rules[0:sub_list_lenght]
characterB = total_character_rules[sub_list_lenght:]

# Convert to JSON
characterA_rule = format_list(characterA,list_name = "CharacterA")
characterB_rule = format_list(characterB,list_name = "CharacterB")

# Character Names - don't need
character_col = format_to_string(character_col)
characters = format_list(character_col,list_name = "Characters Names")

# ========================= Responses ========================



# Repsonses
df_response = data

df_response = df_response[['Character','Opponent','Weapon of Choice','Category']].copy()
df_response = np.asarray(df_response,dtype="str")

for j in range(len(df_response[0])):
    df_response[:, j] = remove_punctuation(df_response[:, j])


opponent_array = np.chararray((1, 3))
category_array = np.chararray((1, 2))

# Any values that are missing for the Opponent, then use CAtegory instead
for i in range(len(df_response)):

    if df_response[i,1] == 'nan':
        row = np.column_stack((df_response[i,0],df_response[i,3]))
        category_array = np.vstack((category_array,row))
    else:
        row = df_response[i, 0:3]
        opponent_array = np.vstack((opponent_array,row))

category_array = np.delete(category_array, (0), axis=0)
opponent_array = np.delete(opponent_array, (0), axis=0)



def create_rule(arr, name = ["Category"], terminal_rule_type = False):

    rule_name_total = []
    rules_total = []
    total_terminal_rules = []
    for i in range(len(arr)):
        terminal_rule_temp = []
        for k in range(1,len(arr[0])):
            attribute_col = arr[:,k]
            column = attribute_col[i].split(",")
            attributes = format_to_string(column)
            rule_name = str('%s %s'% ( arr[i,0] , name[k-1]))
            rules = format_list(attributes,rule_name)
            rule_name_total.append(rule_name)
            rules_total.append(rules)
            terminal_rule_temp.append(rule_name)
        if terminal_rule_type == "opponent":
            terminal_rule = str('"%s": "I would choose %s , because I would get the chance to battle against #%s# with my #%s#", '%(arr[i,0] ,arr[i,0] ,terminal_rule_temp[0],terminal_rule_temp[1] ))
            total_terminal_rules.append(terminal_rule)
        if terminal_rule_type == "category":
            terminal_rule = str('"%s": "I would choose %s , because I have always wanted to be a #%s# ", ' % (arr[i, 0], arr[i, 0], terminal_rule_temp[0]))
            total_terminal_rules.append(terminal_rule)
    return rules_total , total_terminal_rules



category_rule , category_terminal_rule = create_rule(category_array,name = ["Category"], terminal_rule_type = "category")
opponent_rule , opponent_terminal_rule = create_rule(opponent_array,name = ["Opponent","Weapon"] ,terminal_rule_type = "opponent" )

total_response_rules = np.concatenate((category_rule,opponent_rule))
total_terminal_rule =  np.concatenate((opponent_terminal_rule,category_terminal_rule))


text_file = open("Output.txt", "w")
text_file.write(characterA_rule +'\n')
text_file.write(characterB_rule +'\n')
for i in total_rule:
    text_file.write(i+ '\n')
text_file.close()


text_file = open("bot2.txt", "w")
for i in total_response_rules:
    text_file.write(i+ '\n')
text_file.close()

text_file = open("Response.txt", "w")
for i in total_terminal_rule:
    text_file.write(i+ '\n')
text_file.close()
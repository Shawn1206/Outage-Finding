# This script is for evaluating how effective the NLP algorithm is when tagging the location name by checking the
# precision and recall of a randomly generated sample. I wrote this program to make manually checking data easier on
# the terminal and you can manipulate it at will to fulfill your need.
import random
import csv
import sys
import en_core_web_sm
from geolocation_extracting import token_ex

num_t = 100  # the size of sample
text = []  # used for holding the input data
file_name = sys.argv[1]  # terminal input of dataset's filename

# the input is set to be .tsv file and you can change this part at will
with open(file_name, newline='') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        text.append(row[-1])
text = text[1:]

num = len(text)
list_sample = random.sample(range(num), num_t)
# The following five lists are used to hold the indexes of corresponding entries in the dataset
total_num = []
reco_num = []
unreco = []
misreco = []
weird = []

c_num = num_t
with open('log_for_' + file_name[-10::-4] + '.txt', 'a') as file:  # you can custom the output file name
    for i in list_sample:
        print('====================================' + '\n' + '====================================')
        print(str(c_num) + ' / ' + str(num_t))
        c_num -= 1
        flag = 0
        # This part basically depends on your NLP algorithm's API
        nlp = en_core_web_sm.load()
        doc = nlp(text[i])
        for X in doc.ents:
            if X.label_ == 'GPE':
                reco_num.append(i)
                flag = 1
                break

        # printing the data entry on the terminal and collecting feedback
        print(text[i] + '\n')
        feedback = input("Contains location words ([Y]/N)?")
        feedback2 = input("Is this tweet weird ([Y]/N)?")
        while feedback.lower() not in 'yn' or feedback2.lower() not in 'yn' or not feedback2 or not feedback:
            feedback = input("Contains location words ([Y]/N)?")
            feedback2 = input("Is this tweet weird ([Y]/N)?")
        assert (feedback.lower() in 'yn')
        assert (feedback2.lower() in 'yn')
        if feedback.lower() == 'y':
            total_num.append(i)
            if flag == 0:
                unreco.append(i)
        else:
            if flag == 1:
                misreco.append(i)

        if feedback2.lower() == 'y':
            weird.append(i)

    a = set(total_num)
    b = set(reco_num)
    c = set(unreco)
    d = set(misreco)
    e = set(weird)
    a -= e  # get rid of entries which are mistakenly put into our dataset
    b -= e
    c -= e
    d -= e
    count = 0
    # sometimes certain entries need to be reexamined because some unknown reason makes the NLP algorithm failed to 
    # process them in the first run 
    f = []
    for i in c:
        output = token_ex(text[i])
        if output:
            count += 1
            f.append(i)
            
    recall = (len(a) - len(c) + count) / len(a)  # calculate the results
    precision = (len(b) - len(d) + count) / (len(b) + count)
    b |= set(f)
    c -= set(f)
    file.write("The number of total tweets contains locations by human: " + str(len(total_num)) + '\n')
    file.write("The number of total tweets contains locations by machine: " + str(len(b)) + '\n')
    file.write("The number of total tweets contains locations not tagged by machine: " + str(len(c)) + '\n')
    file.write(
        "The number of total tweets contains locations mistakenly tagged by machine: " + str(len(misreco)) + '\n')
    file.write("The number of weird tweets in the sample: " + str(len(weird)) + '\n')
    file.write("The list of total tweets contains locations by human: " + str(total_num) + '\n')
    file.write("The list of total tweets contains locations by machine: " + str(b) + '\n')
    file.write("The list of total tweets contains locations not tagged by machine: " + str(c) + '\n')
    file.write("The list of total tweets contains locations mistakenly tagged by machine: " + str(misreco) + '\n')
    file.write("The list of weird tweets in the sample: " + str(weird) + '\n')
    file.write("Precision is: " + str(precision))
    file.write("Recall is " + str(recall))

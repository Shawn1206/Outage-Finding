import random
import sys
import en_core_web_sm

file_name = sys.argv[1]
tmp = open(file_name, 'r')
text = tmp.read()
text = text.split('\n')[:-1]
num = len(text)
list_sample = random.sample(range(num), 500)
total_num = []
reco_num = []
unreco = []
misreco = []
weird = []
with open('log_for_' + file_name, 'a') as file:
    for i in list_sample:
        print('====================================' + '\n' + '====================================')
        flag = 0
        nlp = en_core_web_sm.load()
        doc = nlp(text[i])
        for X in doc.ents:
            if X.label_ == 'GPE':
                reco_num.append(i)
                flag = 1
                break
        print(text[i] + '\n')
        feedback = input("Contains location words ([Y]/N)?")
        feedback2 = input("Is this tweet weird ([Y]/N)?")
        while feedback.lower() not in 'yn' or feedback2.lower() not in 'yn':
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
    file.write("The number of total tweets contains locations by human: " + str(len(total_num)) + '\n')
    file.write("The number of total tweets contains locations by machine: " + str(len(reco_num)) + '\n')
    file.write("The number of total tweets contains locations not tagged by machine: " + str(len(unreco)) + '\n')
    file.write("The number of total tweets contains locations mistakenly tagged by machine: " + str(len(misreco)) + '\n')
    file.write("The number of weird tweets in the sample: " + str(weird) + '\n')
    file.write("The list of total tweets contains locations by human: " + str(total_num) + '\n')
    file.write("The list of total tweets contains locations by machine: " + str(reco_num) + '\n')
    file.write("The list of total tweets contains locations not tagged by machine: " + str(unreco) + '\n')
    file.write("The list of total tweets contains locations mistakenly tagged by machine: " + str(misreco) + '\n')
    file.write("The list of weird tweets in the sample: " + str(weird) + '\n')

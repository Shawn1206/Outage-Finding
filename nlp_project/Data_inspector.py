import random
import sys
import en_core_web_sm
def token_ex(clean_text):
    nlp = en_core_web_sm.load()
    doc = nlp(clean_text)
    output = []
    for X in doc.ents:
        if X.label_ == 'GPE':
            output.append((X.text, X.label_))
    return output
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
c_num = 500
with open('log_for_' + file_name, 'a') as file:
    for i in list_sample:
        print('====================================' + '\n' + '====================================')
        print(str(c_num) + ' / ' + '500')
        c_num -= 1
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
    a -= e
    b -= e
    c -= e
    d -= e
    count = 0
    f = []
    for i in c:
        output = token_ex()
        if output:
            count += 1
            f.append(i)
    recall = (len(a) - len(c) + count) / len(a)
    precision = (len(b) - len(d) + count) / (len(b) + count)
    b += set(f)
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
    file.write("Precision is: "+str(precision))
    file.write("Recall is "+str(recall))

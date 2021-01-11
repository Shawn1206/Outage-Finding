# this file's function is to synthesize the twitter data scrapped using different keyword sets targeting the same ISP
# Since the keyword set is in the file name of the output data, we can combine them together easily
# However, since the format of scrapped data changed from .txt to .csv/.tsv, the following function may need some change

a = ['no', 'knocked', 'down', 'out']
b = ['internet', 'service', 'network']
isp = ['"AT&T"', 'DIRECTV', 'ATT']
id_set = []  # this set hold the tweets' ids and use them to get rid of the repetitive ones while synthesizing
for i in a:
    for j in b:
        for k in isp:
            key = i + ' ' + j + ' ' + k  # generate the keyword set
            file_name = '/Users/xiaoan/Desktop/network/nlp_project/data/' + key + ' 2019-01-01 00:00:00.txt'
            isp_name = 'Re_AT&T.txt'
            try:
                tmp = open(file_name, 'r')
                text = tmp.read()
                text = text.split('\n')[:-1]

                res = open('New_data_' + isp_name, 'a')  # store the output
                for tweet in text:
                    t_id = tweet[:19]
                    if t_id in id_set:
                        continue
                    else:
                        id_set.append(t_id)
                        res.write(tweet + '\n')
            except:
                continue


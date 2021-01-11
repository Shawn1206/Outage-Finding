# This file contains lists/dictionaries that will be used in data extracting, like US state name as well as their
# abbreviations and their capital names. You can add more stuff in this file which would be helpful to your cases.
capital_dic = {
    'Alabama': 'Montgomery',
    'Alaska': 'Juneau',
    'Arizona': 'Phoenix',
    'Arkansas': 'Little Rock',
    'California': 'Sacramento',
    'Colorado': 'Denver',
    'Connecticut': 'Hartford',
    'Delaware': 'Dover',
    'Florida': 'Tallahassee',
    'Georgia': 'Atlanta',
    'Hawaii': 'Honolulu',
    'Idaho': 'Boise',
    'Illinois': 'Springfield',
    'Indiana': 'Indianapolis',
    'Iowa': 'Des Monies',
    'Kansas': 'Topeka',
    'Kentucky': 'Frankfort',
    'Louisiana': 'Baton Rouge',
    'Maine': 'Augusta',
    'Maryland': 'Annapolis',
    'Massachusetts': 'Boston',
    'Michigan': 'Lansing',
    'Minnesota': 'St. Paul',
    'Mississippi': 'Jackson',
    'Missouri': 'Jefferson City',
    'Montana': 'Helena',
    'Nebraska': 'Lincoln',
    'Neveda': 'Carson City',
    'New Hampshire': 'Concord',
    'New Jersey': 'Trenton',
    'New Mexico': 'Santa Fe',
    'New York': 'Albany',
    'North Carolina': 'Raleigh',
    'North Dakota': 'Bismarck',
    'Ohio': 'Columbus',
    'Oklahoma': 'Oklahoma City',
    'Oregon': 'Salem',
    'Pennsylvania': 'Harrisburg',
    'Rhoda Island': 'Providence',
    'South Carolina': 'Columbia',
    'South Dakoda': 'Pierre',
    'Tennessee': 'Nashville',
    'Texas': 'Austin',
    'Utah': 'Salt Lake City',
    'Vermont': 'Montpelier',
    'Virginia': 'Richmond',
    'Washington': 'Olympia',
    'West Virginia': 'Charleston',
    'Wisconsin': 'Madison',
    'Wyoming': 'Cheyenne',
    'District of Columbia': 'DC'
}
state_list = ['American Samoa', 'AS', 'Guam', 'Guam', 'GU', 'Marshall Islands', 'MH', 'Micronesia', 'FM',
              'Northern Marianas', 'MP', 'Palau', 'PW', 'Puerto Rico', 'P.R.', 'PR', 'Virgin Islands', 'VI', 'Alabama',
              'Ala.', 'AL', 'Alaska', 'Alaska', 'AK', 'Arizona', 'Ariz.', 'AZ', 'Arkansas', 'Ark.', 'AR', 'California',
              'Calif.', 'CA', 'Colorado', 'Colo.', 'CO', 'Connecticut', 'Conn.', 'CT', 'Delaware', 'Del.', 'DE',
              'District of Columbia', 'D.C.', 'DC', 'Florida', 'Fla.', 'FL', 'Georgia', 'Ga.', 'GA', 'Hawaii', 'Hawaii',
              'HI', 'Idaho', 'Idaho', 'ID', 'Illinois', 'Ill.', 'IL', 'Indiana', 'Ind.', 'IN', 'Iowa', 'Iowa', 'IA',
              'Kansas', 'Kans.', 'KS', 'Kentucky', 'Ky.', 'KY', 'Louisiana', 'La.', 'LA', 'Maine', 'Maine', 'ME',
              'Maryland', 'Md.', 'MD', 'Massachusetts', 'Mass.', 'MA', 'Michigan', 'Mich.', 'MI', 'Minnesota', 'Minn.',
              'MN', 'Mississippi', 'Miss.', 'MS', 'Missouri', 'Mo.', 'MO', 'Montana', 'Mont.', 'MT', 'Nebraska',
              'Nebr.', 'NE', 'Nevada', 'Nev.', 'NV', 'New Hampshire', 'N.H.', 'NH', 'New Jersey', 'N.J.', 'NJ',
              'New Mexico', 'N.M.', 'NM', 'New York', 'N.Y.', 'NY', 'North Carolina', 'N.C.', 'NC', 'North Dakota',
              'N.D.', 'ND', 'Ohio', 'Ohio', 'OH', 'Oklahoma', 'Okla.', 'OK', 'Oregon', 'Ore.', 'OR', 'Pennsylvania',
              'Pa.', 'PA', 'Rhode Island', 'R.I.', 'RI', 'South Carolina', 'S.C.', 'SC', 'South Dakota', 'S.D.', 'SD',
              'Tennessee', 'Tenn.', 'TN', 'Texas', 'Tex.', 'TX', 'Utah', 'Utah', 'UT', 'Vermont', 'Vt.', 'VT',
              'Virginia', 'Va.', 'VA', 'Washington', 'Wash.', 'WA', 'West Virginia', 'W.Va.', 'WV', 'Wisconsin', 'Wis.',
              'WI', 'Wyoming', 'Wyo.', 'WY']
state_dict = {'American Samoa': 'AS', 'Alabama': 'AL', 'Ala.': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Ariz.': 'AZ',
              'Arkansas': 'AR', 'Ark.': 'AR', 'California': 'CA', 'Calif.': 'CA', 'Colorado': 'CO', 'Colo.': 'CO',
              'Connecticut': 'CT', 'Conn.': 'CT', 'Delaware': 'DE', 'Del.': 'DE', 'District of Columbia': 'DC',
              'D.C.': 'DC', 'Florida': 'FL', 'Fla.': 'FL', 'Georgia': 'GA', 'Ga.': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
              'Illinois': 'IL', 'Ill.': 'IL', 'Indiana': 'IN', 'Ind.': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
              'Kans.': 'KS', 'Kentucky': 'KY', 'Ky.': 'KY', 'Louisiana': 'LA', 'La.': 'LA', 'Maine': 'ME',
              'Maryland': 'MD', 'Md.': 'MD', 'Massachusetts': 'MA', 'Mass.': 'MA', 'Michigan': 'MI', 'Mich.': 'MI',
              'Minnesota': 'MN', 'Minn.': 'MN', 'Mississippi': 'MS', 'Miss.': 'MS', 'Missouri': 'MO', 'Mo.': 'MO',
              'Montana': 'MT', 'Mont.': 'MT', 'Nebraska': 'NE', 'Nebr.': 'NE', 'Nevada': 'NV', 'Nev.': 'NV',
              'New Hampshire': 'NH', 'N.H.': 'NH', 'New Jersey': 'NJ', 'N.J.': 'NJ', 'New Mexico': 'NM', 'N.M.': 'NM',
              'New York': 'NY', 'N.Y.': 'NY', 'North Carolina': 'NC', 'N.C.': 'NC', 'North Dakota': 'ND', 'N.D.': 'ND',
              'Ohio': 'OH', 'Oklahoma': 'OK', 'Okla.': 'OK', 'Oregon': 'OR', 'Ore.': 'OR', 'Pennsylvania': 'PA',
              'Pa.': 'PA', 'Rhode Island': 'RI', 'R.I.': 'RI', 'South Carolina': 'SC', 'S.C.': 'SC',
              'South Dakota': 'SD', 'S.D.': 'SD', 'Tennessee': 'TN', 'Tenn.': 'TN', 'Texas': 'TX', 'Tex.': 'TX',
              'Utah': 'UT', 'Vermont': 'VT', 'Vt.': 'VT', 'Virginia': 'VA', 'Va.': 'VA', 'Washington': 'WA',
              'Wash.': 'WA', 'West Virginia': 'WV', 'W.Va.': 'WV', 'Wisconsin': 'WI', 'Wis.': 'WI', 'Wyoming': 'WY',
              'Wyo.': 'WY', 'Guam': 'GU', 'Marshall Islands': 'MH', 'Micronesia': 'FM', "Northern Marianas": "MP",
              "Palau": 'PW', 'Puerto Rico': 'PR', "P.R.": 'PR', 'Virgin Islands': 'VI'}

stop_words = ['i', 'im', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
              "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
              'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
              'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
              'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
              'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
              'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
              'up', 'in', 'on', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
              'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'nor', 'only',
              'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
              "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
              'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn',
              "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
              "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", '']
directions = ['North', 'South', 'East', 'West', 'Northwest', 'Northeast', 'Southwest', 'Southeast', 'N', 'S', 'W', 'E',
              'NE', 'NW', 'SW', 'SE']

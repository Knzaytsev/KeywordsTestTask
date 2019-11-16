import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer

dataset = pd.read_csv(r'data\keywords_.csv', sep=';')

df = pd.DataFrame(dataset)

df['\'Keyword\''] = list(map(lambda x: re.sub(r'\s-[a-zA-Zа-яА-Я!0-9]+', '', x), df['\'Keyword\'']))

df_result = pd.DataFrame({'Keyword_x' : [], 'AdGroupId_x' : [], 'Keyword_y' : [], 'AdGroupId_y' : [], 'crossed' : []})

frame = list()
tokenizer = RegexpTokenizer(r'[a-zA-Zа-яА-Я+!0-9]+')
for i in df.index:
    agi = df['\'AdGroupId\''][i]
    series = df.where(df['\'AdGroupId\''] != agi)
    series.dropna(inplace=True)
    for s in series.index:
        word_x = df['\'Keyword\''][i]
        word_y = df['\'Keyword\''][s]
        kws_x = tokenizer.tokenize(word_x.lower())
        kws_y = tokenizer.tokenize(word_y.lower())
        agiy = df['\'AdGroupId\''][s]
        subset = [word for word in kws_x if word.lower() in kws_y]
        if len(subset) > 1:
            subset = ', '.join(map(str, subset))
            frame.append(pd.DataFrame({'Keyword_x' : [word_x], 'AdGroupId_x' : [agi], 'Keyword_y' : [word_y], 
                                       'AdGroupId_y' : [agiy], 'crossed' : [subset]}))

df_result = pd.concat(frame)

df_result.to_csv(r'data/keywords_ext.csv', index=None)
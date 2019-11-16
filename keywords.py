import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer

dataset = pd.read_csv(r'data\keywords_.csv', sep=';')

df = pd.DataFrame(dataset)

<<<<<<< HEAD
df['\'Keyword\''] = list(map(lambda x: re.sub(r'\s-[a-zA-Zа-яА-Я!+0-9]+', '', x), df['\'Keyword\'']))

df_result = pd.DataFrame({'Keyword_x' : [], 'AdGroupId_x' : [], 'Keyword_y' : [], 'AdGroupId_y' : [], 'crossed' : []})

tokenizer = RegexpTokenizer(r'[a-zA-Zа-яА-Я+!0-9]+')
tokens = list(map(lambda x: tokenizer.tokenize(x.lower()), df['\'Keyword\'']))
=======
df['\'Keyword\''] = list(map(lambda x: re.sub(r'\s-[a-zA-Zа-яА-Я!0-9]+', '', x), df['\'Keyword\'']))

df_result = pd.DataFrame({'Keyword_x' : [], 'AdGroupId_x' : [], 'Keyword_y' : [], 'AdGroupId_y' : [], 'crossed' : []})

frame = list()
tokenizer = RegexpTokenizer(r'[a-zA-Zа-яА-Я+!0-9]+')
>>>>>>> 73250abab764c53978dbd61def70bbad8231b3e8
for i in df.index:
    agi = df['\'AdGroupId\''][i]
    series = df.where(df['\'AdGroupId\''] != agi)
    series.dropna(inplace=True)
<<<<<<< HEAD
    inds = [s for s in series.index if len([word for word in tokens[i] if word in tokens[s]]) > 1]
    if len(inds) > 0:
        kws_x = [df['\'Keyword\''][i]] * len(inds)
        agi_x = [df['\'AdGroupId\''][i]] * len(inds)
        df_search = df.loc[df.index.isin(inds)]
        kws_y = df_search['\'Keyword\''].tolist()
        agi_y = df_search['\'AdGroupId\''].tolist()
        subsets = list(list())
        for s in inds:
            subsets.append([w for w in tokens[i] if w in tokens[s]])
        subsets = [', '.join(map(str, w)) for w in subsets]
        df_add = pd.DataFrame({'Keyword_x' : [], 'AdGroupId_x' : [], 'Keyword_y' : [], 'AdGroupId_y' : [], 'crossed' : []})
        df_add['Keyword_x'] = kws_x
        df_add['AdGroupId_x'] = agi_x 
        df_add['Keyword_y'] = kws_y
        df_add['AdGroupId_y'] = agi_y
        df_add['crossed'] =  subsets
        df_result = pd.concat([df_result, df_add])

df_result[['AdGroupId_x', 'AdGroupId_y']] = df_result[['AdGroupId_x', 'AdGroupId_y']].astype('int64')

df_result.to_csv(r'data\keywords_ext.csv', index=None)

print('Done!')
=======
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
>>>>>>> 73250abab764c53978dbd61def70bbad8231b3e8

import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer

dataset = pd.read_csv(r'C:\Users\Tuccc\Desktop\Работка\data\keywords_.csv', sep=';')

df = pd.DataFrame(dataset)

df['\'Keyword\''] = list(map(lambda x: re.sub(r'\s-[a-zA-Zа-яА-Я!+0-9]+', '', x), df['\'Keyword\'']))

df_result = pd.DataFrame({'Keyword_x' : [], 'AdGroupId_x' : [], 'Keyword_y' : [], 'AdGroupId_y' : [], 'crossed' : []})

tokenizer = RegexpTokenizer(r'[a-zA-Zа-яА-Я+!0-9]+')
tokens = list(map(lambda x: tokenizer.tokenize(x.lower()), df['\'Keyword\'']))

for i in df.index:
    agi = df['\'AdGroupId\''][i]
    series = df.where(df['\'AdGroupId\''] != agi)
    series.dropna(inplace=True)
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

df_result.to_csv(r'C:\Users\Tuccc\Desktop\Работка\data\keywords_ext.csv', index=None)

print('Done!')

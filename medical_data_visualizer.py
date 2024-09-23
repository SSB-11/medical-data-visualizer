import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
def calculate_bmi(cm_height, kg_weight):
    bmi = kg_weight/pow(cm_height/100, 2) # Height in centimeters to meters
    return bmi

df['overweight'] = np.where(calculate_bmi(df['height'], df['weight']) > 25, 1, 0)

# 3
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6
    df_cat = df_cat.groupby('cardio').value_counts()
    df_cat.name = 'total'
    
    # 7
    df_cat = df_cat.reset_index()
    chart = sns.catplot(data=df_cat, x='variable', y='total', col='cardio', hue='value', kind='bar', order=sorted(df_cat['variable']))


    # 8
    fig = chart.fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi'])
        & (df['height'] >= df['height'].quantile(0.025)) 
        & (df['height'] <= df['height'].quantile(0.975))
        & (df['weight'] >= df['weight'].quantile(0.025)) 
        & (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # 14
    fig, ax = plt.subplots()

    # 15
    sns.heatmap(corr, ax=ax, annot=True, cmap='YlGnBu', fmt='.1f', mask=mask)


    # 16
    fig.savefig('heatmap.png')
    return fig

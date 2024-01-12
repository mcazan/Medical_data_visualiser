import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = None
df=pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = None

bmi= (df['weight'])/(df['height']/100)**2

overweight=[]
for v in bmi:
  if v>25:
    overweight.append(1)
  else:
    overweight.append(0)

df['overweight'] = overweight

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.loc[df['cholesterol']==1,'cholesterol'] = 0
df.loc[df['cholesterol']>1,'cholesterol'] = 1
df.loc[df['gluc']==1,'gluc'] = 0
df.loc[df['gluc']>1,'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = None
    df_cat=pd.melt(df,
                  id_vars=['cardio'],
                  value_vars=['cholesterol', 'gluc','alco','active', 'smoke', 'overweight']
                  )

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat=df_cat.groupby(['cardio','variable']).value_counts()
    df_cat=df_cat.reset_index()
    df_cat.columns=['cardio','variable','value','total']

    # Draw the catplot with 'sns.catplot()'
    f = sns.catplot(data=df_cat,
               x='variable',
               y='total',
               hue='value',
               col='cardio', 
               kind='bar')


    # Get the figure for the output
    fig = None
    fig=f.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = None
    df_heat = df.loc[(df["ap_lo"] <= df["ap_hi"]) & 
                    (df["height"] >= df["height"].quantile(0.025)) & 
                    (df["height"] <= df["height"].quantile(0.975)) & 
                    (df["weight"] >= df["weight"].quantile(0.025)) & 
                    (df["weight"] <= df["weight"].quantile(0.975))]

    # Calculate the correlation matrix
    corr = None
    corr=df_heat.corr()

    # Generate a mask for the upper triangle
    mask = None
    mask=np.triu(np.ones_like(corr,dtype=bool))


    # Set up the matplotlib figure
    fig, ax=plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,
              vmax=.3,  
              center=0,
              annot=True,
              fmt='.1f',
              annot_kws={'fontsize':6},
              cbar_kws={'shrink':.7},
              linewidth=.5,
              mask=mask  
    )


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

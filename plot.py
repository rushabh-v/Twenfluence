import pandas as pd
import seaborn as sns

def plot_data(data):
    df = pd.DataFrame.from_dict(data)
    sns.set_style('ticks')
    plt = sns.boxplot(data=df)
    plt.set_xticklabels(labels=plt.get_xticklabels(), rotation=45)
    sns.despine()
    figure = plt.get_figure()
    figure.savefig("output.png", bbox_inches = "tight")
    return figure

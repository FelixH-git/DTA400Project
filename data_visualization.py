from Simulation import Person, Virus_Simulation
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calc_histogram(csv_file):
    df = pd.read_csv(f'{csv_file}.csv', encoding='latin-1')
    df = df.sort_values(by='hour')
    print(df)
    sns.displot(data=df['hour']).figure.get_figure().savefig(f'{csv_file}.png')

def calc_line_plot(csv_file, sort_after=None, use_matplotlib=False):
    df = pd.read_csv(f'{csv_file}.csv', encoding='latin-1')
    
    if not use_matplotlib:
        df = pd.read_csv(f'{csv_file}.csv', encoding='latin-1')
        if sort_after:
            df = df.sort_values(by=sort_after)
        sns.lineplot(df[f'{sort_after}']).figure.get_figure().savefig(f'{csv_file}.png')
        
if __name__ == "__main__":
    calc_line_plot('Que_length', sort_after='que_length')
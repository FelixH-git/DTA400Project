from Simulation import Person, Virus_Simulation
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    df = pd.read_csv('people.csv', encoding='latin-1')
    df = df.sort_values(by='age')
    print(df)
    sns.displot(data=df['age']).figure.get_figure().savefig('test.png')
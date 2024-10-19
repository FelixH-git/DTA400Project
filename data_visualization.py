from Simulation import Person, Virus_Simulation
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    df = pd.read_csv('stay_in_hospital.csv', encoding='latin-1')
    df = df.sort_values(by='days')
    print(df)
    sns.displot(data=df['days']).figure.get_figure().savefig('test.png')
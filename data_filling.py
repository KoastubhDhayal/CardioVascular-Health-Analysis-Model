import pandas as pd

df = pd.read_csv(r'C:\Users\Vaishnavi\OneDrive\Desktop\sem 5\de\DE_MiniProject\merged_data.csv')

df.fillna(0, inplace=True)  

df.to_csv('data_filled.csv', index=False)
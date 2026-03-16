
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
data = pd.read_csv(r'C:\Users\Vaishnavi\OneDrive\Desktop\sem 5\de\DE_MiniProject\data_updated.csv')
# Set the figure size
plt.figure(figsize=(10, 6))

# Create a bar plot of sleep efficiency by age category and gender
sns.barplot(x='age_category', y='Sleep efficiency', hue='Gender', data= data, ci=None)

# Set the title and labels
plt.title('Average Sleep Efficiency by Age Group and Gender')
plt.xlabel('Age Group')
plt.ylabel('Sleep Efficiency')

# Show the plot
plt.show()

plt.figure(figsize=(10, 6))

# Plot a histogram of sleep duration
sns.histplot(data['Sleep duration'], bins=20, kde=True, color='skyblue')

# Set the title and labels
plt.title('Distribution of Sleep Duration')
plt.xlabel('Sleep Duration (hours)')
plt.ylabel('Frequency')

# Show the plot
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Filter numeric columns only for correlation calculation
numeric_data = data.select_dtypes(include='number')

# Compute the correlation matrix
corr_matrix = numeric_data.corr()

# Set the figure size
plt.figure(figsize=(12, 10))

# Create a heatmap of the correlation matrix
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)

# Set the title
plt.title('Correlation Matrix Heatmap')

# Show the plot
plt.show()
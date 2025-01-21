import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('cot-few-claude.csv')

# Strip any extra spaces from the labels
df['TRUE'] = df['TRUE'].str.strip()
df['pre'] = df['pre'].str.strip()

# Ensure the columns are of the correct type (use 'category' type if the values are labels)
df['TRUE'] = df['TRUE'].astype('category')
df['pre'] = df['pre'].astype('category')

# Optionally handle missing values (if necessary)
df = df.dropna(subset=['TRUE', 'pre'])

# Check unique values in TRUE and pre columns
print("Unique values in 'TRUE':", df['TRUE'].unique())
print("Unique values in 'pre':", df['pre'].unique())

# Check value counts for class distribution
print("Class distribution in TRUE:\n", df['TRUE'].value_counts())
print("Class distribution in pre:\n", df['pre'].value_counts())

# Define categories
categories = ['Good', 'Moderate', 'Poor']

# Compute precision, recall, and F1 for each class
precision = precision_score(df['TRUE'], df['pre'], labels=categories, average=None, zero_division=0)
recall = recall_score(df['TRUE'], df['pre'], labels=categories, average=None, zero_division=0)
f1 = f1_score(df['TRUE'], df['pre'], labels=categories, average=None, zero_division=0)

# Output per-class results
for i, category in enumerate(categories):
    print(f"Class: {category}")
    print(f"Precision: {precision[i]}")
    print(f"Recall: {recall[i]}")
    print(f"F1 Score: {f1[i]}")
    print()

# Compute macro averages
precision_macro = precision_score(df['TRUE'], df['pre'], labels=categories, average='macro', zero_division=0)
recall_macro = recall_score(df['TRUE'], df['pre'], labels=categories, average='macro', zero_division=0)
f1_macro = f1_score(df['TRUE'], df['pre'], labels=categories, average='macro', zero_division=0)

print(f"Macro Precision: {precision_macro}")
print(f"Macro Recall: {recall_macro}")
print(f"Macro F1 Score: {f1_macro}")

# Compute weighted averages
precision_weighted = precision_score(df['TRUE'], df['pre'], labels=categories, average='weighted', zero_division=0)
recall_weighted = recall_score(df['TRUE'], df['pre'], labels=categories, average='weighted', zero_division=0)
f1_weighted = f1_score(df['TRUE'], df['pre'], labels=categories, average='weighted', zero_division=0)

print(f"Weighted Precision: {precision_weighted}")
print(f"Weighted Recall: {recall_weighted}")
print(f"Weighted F1 Score: {f1_weighted}")

# Confusion matrix
conf_matrix = confusion_matrix(df['TRUE'], df['pre'], labels=categories)

# Plot confusion matrix
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=categories, yticklabels=categories)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Print confusion matrix
print("Confusion Matrix:\n", conf_matrix)

import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import StackingClassifier, VotingClassifier
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load dataset
col_names = ['sender', 'receiver', 'date', 'subject', 'body', 'url', 'label']
#dataset1 = pd.read_csv('Nazario_5.csv', header=None, names=col_names)
dataset1 = pd.read_csv('/content/Nazario_7_3 - Nazario_5.csv', header=None, names=col_names)
#dataset1 = pd.read_csv('Nazario_7_3.csv', header=None, names=col_names)

# Shuffle dataset
#dataset1 = dataset1.sample(frac=1)

# Apply OneHotEncoder to categorical columns
onehot = OneHotEncoder(handle_unknown='ignore')
onehot_transformed = pd.DataFrame(onehot.fit_transform(dataset1[['sender', 'receiver', 'date', 'subject', 'body', 'url']]).toarray())
dataset1 = pd.concat([dataset1, onehot_transformed], axis=1)
dataset1.drop(['sender', 'receiver', 'date', 'subject', 'body', 'url'], axis=1, inplace=True)

# Initialize LabelEncoder
#le = LabelEncoder()

# List of columns to encode
#columns_to_encode = ['sender', 'receiver', 'date', 'subject', 'body', 'url']

# Apply LabelEncoder to each column in the list
#for column in columns_to_encode:
#    dataset1[column] = le.fit_transform(dataset1[column])

X = dataset1.iloc[:, 1:]
y = dataset1.iloc[:, :1]

# Check the distribution of your classes
print(y['label'].value_counts())

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a StratifiedKFold object
strat_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Use the StratifiedKFold object to split the training data into different folds
for train_index, val_index in strat_kfold.split(X_train, y_train):
    X_train_fold, X_val_fold = X_train.iloc[train_index], X_train.iloc[val_index]
    y_train_fold, y_val_fold = y_train.iloc[train_index], y_train.iloc[val_index]


# Decision Tree
decision_tree = DecisionTreeClassifier(random_state=42)

# KNN
knn = KNeighborsClassifier(n_neighbors=13)

# Define base models
base_models = [('Decision Tree', DecisionTreeClassifier()),
               ('K-Nearest Neighbors', KNeighborsClassifier())]

# Define meta model
meta_model = LogisticRegression()

# Stacking Classifier
stacking_model = StackingClassifier(estimators=base_models, final_estimator=meta_model)

# List of models
models = [decision_tree, knn, stacking_model]
model_names = ['Decision Tree', 'K-Nearest Neighbors', 'Stacking Classifier']

# Train and evaluate each model
for model, name in zip(models, model_names):
    model.fit(X_train, y_train.values.ravel())
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro', zero_division=1)  # or 'weighted'
    recall = recall_score(y_test, y_pred, average='macro', zero_division=1)  # or 'weighted'
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=1)  # or 'weighted'

    print(f"Model: {name}")
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("\n")

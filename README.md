# Phishing Email Detection with Machine Learning

Compares machine-learning classifiers for telling phishing emails from legitimate ones.

## Approach

1. Load a labeled email dataset (Nazario phishing corpus). Columns: sender, receiver, date, subject, body, URL, label.
2. Encode the text and categorical fields.
3. Split 80/20 into training and evaluation sets, with 5-fold stratified cross-validation.
4. Train and compare:
   - Decision tree
   - k-nearest neighbors (k = 13)
   - Stacking ensemble (decision tree + k-NN, logistic regression as the meta-model)
   - Voting ensemble
5. Report accuracy, precision, recall and F1 for each model.

## Built with

Python · scikit-learn · pandas · NumPy

## Run it

Written for Google Colab. Set the CSV path near the top of `3Methods_ML_PhishEmails.py` to your copy of the dataset, then run:

```bash
pip install scikit-learn pandas numpy
python 3Methods_ML_PhishEmails.py
```

import pandas as pd
from sklearn.metrics import confusion_matrix
from prettytable import PrettyTable

def load_dataframes(date, to_load=["courses", "participants"]):
    # TODO
    dfs = []

# Print the confusion matrix for a binary classification task with prettytable
def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    x = PrettyTable()

    x.field_names = ["", "Predicted Loser", "Predicted Winner"]

    x.add_row(["True Loser", cm[0,0], cm[0,1]])
    x.add_row(["True Winner", cm[1,0], cm[1,1]])
    print(x)
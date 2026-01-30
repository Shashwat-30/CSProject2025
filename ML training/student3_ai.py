# For predicting student exam scores in multiple subjects using multi-output regression.
# The model is trained on a dataset containing student attendance % and previous exam scores.
# The final model is saved as 'best_exam4_predictor.pkl'.

# Import Libraries
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Lasso

# Load Dataset
df = pd.read_csv(r"realistic_students_dataset_5subjects.csv")                                       

# Features (X) & Targets (y)
X = df.drop(['Student_ID','Exam4_Math','Exam4_Science','Exam4_English','Exam4_History','Exam4_Computer'], axis=1)
y = df[['Exam4_Math','Exam4_Science','Exam4_English','Exam4_History','Exam4_Computer']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = MultiOutputRegressor(Lasso(alpha=10))
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Save Model
joblib.dump(model, "best_exam4_predictor.pkl")
print("\nModel saved as best_exam4_predictor.pkl")

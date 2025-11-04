import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder


class AdaptiveMLEngine:

    def __init__(self):
        
        self.level_map = {"easy": 1, "medium": 2, "hard": 3}

        data = pd.read_csv("mcq_training_data.csv")

        self.le_subject = LabelEncoder()
        data["subject_enc"] = self.le_subject.fit_transform(data["subject"])

        X = data[["subject_enc", "accuracy", "avg_time", "streak", "current_level"]].values
        y = data["next_level"].values
        

        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model = LogisticRegression(max_iter=300)
        self.model.fit(X_scaled, y)

    def predict_next_level(self, subject, accuracy, avg_time, streak, current_level):

        # Prepare input features
        
        subj_enc = self.le_subject.transform([subject])[0]
        if isinstance(current_level, str):
            current_level = self.level_map.get(current_level.lower(), 1)
        subject_map = {"Math": 1, "Biology": 2, "Indian Law": 3, "Geography": 4, "English": 5}
        subj_enc = subject_map.get(subject, 0)
        X_new = self.scaler.transform([[subj_enc, accuracy, avg_time, streak, current_level]])
        pred_level = self.model.predict(X_new)[0]
        return pred_level


import pickle
import pandas as pd
from schema.user_input import UserInput 
from schema.prediction_response import PredictionResponse

MODEL_VERSION = "1.0.0"

class Model:

    def __init__(self):

        model_path =  'model/model.pkl'
        # import the ml model
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
    def predict(self, data : UserInput) -> PredictionResponse:
        input_df = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'smoker': data.smoker,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }])

        predicted_class = self.model.predict(input_df)[0]
        class_labels = self.model.classes_.tolist()
        probabilities = self.model.predict_proba(input_df)[0]
        confidence = max(probabilities)
        class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))
        prediction_response = PredictionResponse(
            predicted_category=predicted_class,
            confidence=round(confidence, 4),
            class_probabilities=class_probs
        )
        return prediction_response.model_dump_json()

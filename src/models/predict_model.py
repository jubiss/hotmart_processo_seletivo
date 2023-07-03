import joblib
import pandas as pd
import src.features.build_features as build_features
# Load the best_model
model = joblib.load('models\XGBoost.joblib')

def single_prediction(producer_id, repurchase, product_category, product_niche, product_creation_date,product_id=-1 , model=model):
    # Make predictions using the loaded model
    data = pd.DataFrame(data = [[product_id, producer_id, repurchase, product_category, product_niche, product_creation_date]],
                        columns = ['product_id', 'producer_id', 'repurchase', 'product_category', 'product_niche', 
                                   'product_creation_date'])
    
    data = build_features.product_creation_date_eng(data)
    data = build_features.product_creation_date_eng(data)
    predictions = model.predict(data)
    return predictions

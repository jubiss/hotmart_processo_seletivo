import sys
import os
sys.path.append(os.getcwd())
import joblib
import pandas as pd
import src.features.build_features as build_features
# Load the best_model
model = joblib.load('models\XGBoost.joblib')

def single_prediction(product_id , producer_id, repurchase, product_category, product_niche, product_creation_date, model=model):
    # Make predictions using the loaded model
    data = pd.DataFrame(data = [[product_id, producer_id, repurchase, product_category, product_niche, product_creation_date]],
                        columns = ['product_id', 'producer_id', 'repurchase', 'product_category', 'product_niche', 
                                   'product_creation_date'])
    
    data = data.set_index('product_id')
    data = build_features.static_features(data, predict=True)
    predictions = model.predict(data)
    return predictions

pred = single_prediction(product_id=-1 , producer_id=534, repurchase=True, 
                         product_category='Podcast', product_niche='Child psychology', 
                         product_creation_date='2011-03-19')
print(pred)
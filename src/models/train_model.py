import pandas as pd
import sys
import os
sys.path.append(os.getcwd())
import src.features.build_features as build_features
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from xgboost.sklearn import XGBRegressor
from sklearn.model_selection import train_test_split
from joblib import dump
#from boruta import BorutaPy

df = pd.read_csv(r'data/sales_data.csv', index_col=0)

transform_target = MinMaxScaler()
df['purchase_value'] = transform_target.fit_transform(df[['purchase_value']])

param_grid = {
    'model__learning_rate': [0.1, 0.01, 0.001],
    'model__n_estimators': [100, 200, 300],
    'model__max_depth': [3, 4, 5],
    'model__subsample': [0.8, 0.9, 1.0]
}



df = df.set_index('product_id')
df = build_features.product_creation_date_eng(df)
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['purchase_value']), df[['purchase_value']])

y_train = y_train.reset_index().groupby('product_id').agg(target = ('purchase_value', 'sum'))['target']
y_test = y_test.reset_index().groupby('product_id').agg(target = ('purchase_value', 'sum'))['target']


pipeline = Pipeline([
    ('feature_engineering', build_features.build_features(filter_with_few_products=True)),
    #('feature_selection', BorutaPy(XGBRegressor(), n_estimators='auto', verbose=1, random_state=1)),
    ('model', XGBRegressor())
])

pipeline.fit(X_train, y_train)

feat_eng_pipe = pipeline.steps[0][1]
X_train_pipe = feat_eng_pipe.transform(X_train)
X_test_pipe = feat_eng_pipe.transform(X_test)
train_pred = pipeline.predict(X_train)
test_pred = pipeline.predict(X_test)

X_train_pipe['target'] = y_train
X_test_pipe['target'] = y_test
X_train_pipe['pred'] = train_pred
X_test_pipe['pred'] = test_pred

X_train_pipe.to_csv(r'data\processed\pred_train_data.csv') 
X_test_pipe.to_csv(r'data\processed\pred_test_data.csv')

#eval_dict = eval.evaluate_model(pipeline, X_train, X_test, y_train, y_test)
# Save the parameters as a DataFrame


#results_df = pd.DataFrame.from_dict(eval_dict, orient='index', columns=['XGBoost'])
#results_df.to_csv('model_parameters.csv', index=True)

# Save Model
dump(pipeline, 'models\XGBosst.joblib')
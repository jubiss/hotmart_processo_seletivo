import pandas as pd
import datetime as datetime
from sklearn.base import BaseEstimator, TransformerMixin


class build_features(BaseEstimator, TransformerMixin):


    def __init__(self, filter_with_few_products=False):
        self.filter_with_few_products = filter_with_few_products
        self.features_prod_categ = None
        self.features_prod_niche = None
        self.feature_repurchase = None
        self.feature_creation_date = None
        self.feature_producer = None
        self.columns = None

    def fit(self, X, y=None):
        df = X.reset_index()
        df['purchase_value'] = y

        self.features_prod_categ = self.product_category_eng(df, 'product_category')
        self.features_prod_niche = self.product_category_eng(df, 'product_niche')
        self.feature_repurchase, self.columns_repurchase = self.repurchase_eng(df)
        #self.feature_creation_date = self.product_creation_date_eng(df)
        self.feature_producer, self.columns_producer = self.producer_feature_eng(df)
        return self
    
    def transform(self, X, y=None):
        # Product Category
        X = X.reset_index()
        X = X.merge(self.features_prod_categ, on=['product_category'], how='left').fillna(0)
        # Product Niche
        X = X.merge(self.features_prod_niche, on=['product_niche'], how='left')
        # Product Repurchase
        X = X.merge(self.feature_repurchase, on=['product_id'], how='left')
        X[self.columns_repurchase] = X[self.columns_repurchase].fillna(False)
        # Product creation date
        #X = X.merge(self.feature_creation_date, on=['product_id'], how='left')
        # Producer
        X = X.merge(self.feature_producer, on=['producer_id'], how='left')
        X[self.columns_producer] = X[self.columns_producer].fillna(0)
        
        #y= X.groupby('product_id').agg(target = ('purchase_value', 'sum'))

        X = X.drop(columns=['buyer_id', 'producer_id', 'product_category', 'product_niche', 'product_creation_date', 'affiliate_id', 
                            'purchase_id', 'purchase_date','affiliate_commission_percentual', 'purchase_device',
                            'purchase_origin', 'is_origin_page_social_network', 'Venda'])
        X = X.drop_duplicates()
        X = X.set_index('product_id')
        self.columns = X.columns
        return X

    
    def get_feature_names_out(self):
        # Return the column names of the transformed DataFrame

        return self.columns

    def producer_feature_eng(self, df, filter_with_few_products = False):

        producer_feat = df.groupby(['producer_id', 'product_id']).agg(
                                                        total_vendas=('purchase_value', 'sum'),
                                                        count_vendas=('purchase_value', 'count')).reset_index()

        producer_feat = producer_feat.groupby('producer_id').agg(
                                                        n_prod_producer=('product_id', 'nunique'),
                                                        count_vendas_producer=('count_vendas', 'sum'),
                                                        total_vendas_producer = ('total_vendas', 'sum'),
                                                        media_vendas_produtos_producer =('total_vendas', 'mean')).reset_index()
        if filter_with_few_products:
            producer_feat = producer_feat[(producer_feat['n_prod_producer'] > 5)]
        columns = producer_feat.drop(columns=['producer_id']).columns
        return producer_feat, columns

    def repurchase_eng(self, df):
        
        repurchase = df.groupby(['product_id', 'buyer_id']).agg(count_purchases = ('buyer_id', 'count')).reset_index()
        repurchase = repurchase.groupby(['product_id',]).agg(count_purchases = ('count_purchases', 'sum'),
                                                    count_buyers = ('buyer_id','nunique'))
        repurchase = repurchase[repurchase['count_buyers']*1.1 < repurchase['count_purchases']].reset_index()
        repurchase['repurchase'] = True
        return repurchase[['product_id', 'repurchase']], ['repurchase']

    def product_category_eng(self, df, column):
        #product_category, product_niche
        features = df.groupby(['product_id', column]).agg(
            total_sell = ('purchase_value', 'sum'),
            volume_sell = ('purchase_value', 'count'),
            num_buyers = ('buyer_id', 'nunique'),
        ).reset_index()

        features = features.groupby(column).agg(
            total_prod = ('product_id', 'count'),
            total_sell = ('total_sell', 'sum'),
            mean_sell = ('total_sell', 'mean'),
            std_sell = ('total_sell', 'std'),
            total_volume = ('volume_sell', 'sum'),
            mean_volume = ('volume_sell', 'mean'),
            std_volume = ('volume_sell', 'std'),
            total_buyers = ('num_buyers', 'sum'),
            mean_buyers = ('num_buyers', 'mean'),
            std_buyers = ('num_buyers', 'std')
        ).reset_index()

        # Rename the columns
        new_columns = {
            'total_prod': f'{column}_total_prod',
            'total_sell': f'{column}_total_sell',
            'mean_sell': f'{column}_mean_sell',
            'std_sell': f'{column}_std_sell',
            'total_volume': f'{column}_total_volume',
            'mean_volume': f'{column}_mean_volume',
            'std_volume': f'{column}_std_volume',
            'total_buyers': f'{column}_total_buyers',
            'mean_buyers': f'{column}_mean_buyers',
            'std_buyers': f'{column}_std_buyers'
        }

        features = features.rename(columns=new_columns)
        return features

    def affiliate_feature_eng(self, df, filter_with_few_products = False):
        # Fazer o rankeamento dos afiliados e levar em consideração os top 5 afiliados
        affiliate_n_prod = df.groupby(['affiliate_id', 'product_id']).agg(
                                                        total_vendas=('purchase_value', 'sum'),
                                                        count_vendas=('purchase_value', 'count')).reset_index()
        affiliate_n_prod = affiliate_n_prod.groupby('affiliate_id').agg(
                                                        n_prod_affiliate=('product_id', 'nunique'),
                                                        count_vendas_affiliate=('count_vendas', 'sum'),
                                                        total_vendas_affiliate = ('total_vendas', 'sum'),
                                                        media_vendas_produtos_affiliate =('total_vendas', 'mean'))
        if filter_with_few_products:
            affiliate_n_prod = affiliate_n_prod[(affiliate_n_prod['n_prod_affiliate'] > 5)]
        

        df = df.merge(affiliate_n_prod, how = 'left', on=['affiliate_id'])
        return df.drop(columns=['affiliate_id'])
    
def product_creation_date_eng(df):
    from datetime import datetime
    last_purchase = datetime(2016, 6, 30)
    df['product_creation_date'] = pd.to_datetime(df['product_creation_date'])
    df['years_since_creation'] = last_purchase.year - df['product_creation_date'].dt.year
    df['months_since_creation'] = df['years_since_creation']*12 + (last_purchase.month - df['product_creation_date'].dt.month)
    #creation_dates = df[['product_id', 'years_since_creation', 'months_since_creation']].drop_duplicates()
    return df


class TargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols):
        self.cols = cols
        self.target_encoders = {}

    def fit(self, X, y):
        breakpoint()
        df = pd.concat([X, y], axis=1)
        for col in self.cols:
            target_encoder = df.groupby(col)['target'].mean().to_dict()
            self.target_encoders[col] = target_encoder
        return self

    def transform(self, X):
        X_encoded = X.copy()
        for col in self.cols:
            X_encoded[col] = X_encoded[col].map(self.target_encoders[col])
        return X_encoded
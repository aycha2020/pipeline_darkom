from etl.clean import clean_data
from etl.features import feature_engineering
from etl.warehouse import build_warehouse


clean_data()
feature_engineering()
build_warehouse()
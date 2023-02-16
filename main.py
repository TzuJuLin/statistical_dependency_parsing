from reader import Corpus
from feature import FeatureDict

corp = Corpus("/Users/lintzuru/Desktop/WS22:23/parsing/test_feature")
corp.add_sentence()
gold_arc, feature_dict = FeatureDict(corp).extract_feature()
print(feature_dict)
print(gold_arc)

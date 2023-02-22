# statistical_dependency_parsing

This is a project for the **Statistical Dependency Parsing** course, taught by 
Agnieszka Faleńska, at Uni Stuttgart WS22/23

## Overview of the Parser

### Graph-based Dependency Parsing
### Perceptron Algorithm
### Linguistic Features
The lingusitc features that serves as the feature of the perceptron are taken from [McDonald et al 2005](https://aclanthology.org/H05-1066.pdf).
The feature template includes 6 uni-gram features, 7 bi-gram features and 4 surrounding word POS features and 1 in between POS features. The features are further combined with the direction of the arc and the distance between the head and the dependent.

For the English dataset, we derived around 80M features with a runtime of 14 minutes. As for the German dataset, around 40M features were derived within 7 minutes.

### Data Format
The code is written to handle conll06 format only.

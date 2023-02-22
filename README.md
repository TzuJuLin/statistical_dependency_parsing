## statistical_dependency_parsing

This is a project for the **Statistical Dependency Parsing** course, taught by 
Agnieszka Faleńska, at Uni Stuttgart WS22/23

## Overview of the Parser

### Graph-based Dependency Parsing
This parser follows the [Eisner's Algorithmn](https://aclanthology.org/1997.iwpt-1.10.pdf) as the decoder to find the best tree of a sentence given the scores of all the possible arcs. 
### Perceptron Algorithm
In this project, perceptron is used to learn the weight vector that is used to get the scores of the possible arcs in a given sentence. 
### Linguistic Features
The lingusitc features that serves as the feature of the perceptron are taken from [McDonald et al 2005](https://aclanthology.org/H05-1066.pdf).
The feature template includes 6 uni-gram features, 7 bi-gram features and 4 surrounding word POS features and 1 in between POS features. The features are further combined with the direction of the arc and the distance between the head and the dependent.

For the English dataset, we derived around 80M features with a runtime of 14 minutes. As for the German dataset, around 40M features were derived within 7 minutes.

### Data Format
The code is written to handle conll06 format.

## Usage

To train the parser run
````
```
./main.py train --data <training_data_path>
```
````

To train ther parser with a specific epoch (the default is 3)
````
```
./main.py train --data <training_data_path> --epoch <number of epoch>
```
````
To predict with the parser, you need to provide a trained model object
````
```
./ main.py predict --data <test_data_path> --model <model_path>
```
````


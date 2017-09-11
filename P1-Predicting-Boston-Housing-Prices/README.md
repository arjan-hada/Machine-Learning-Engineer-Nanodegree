## Project 1: Predicting Boston Housing Prices

In this project, we will apply basic machine learning concepts on data collected for housing prices in the Boston, Massachusetts area to predict the selling price of a new home. We will first explore the data to obtain important features and descriptive statistics about the dataset. Next, we will properly split the data into testing and training subsets, and determine a suitable performance metric for this problem. We will then analyze performance graphs for a learning algorithm with varying parameters and training set sizes. This will enable us to pick the optimal model that best generalizes for unseen data. Finally, we will test this optimal model on a new sample and compare the predicted selling price to your statistics.

### Install

This project requires **Python 2.7** and the following Python libraries installed:

- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org/)
- [matplotlib](http://matplotlib.org/)
- [scikit-learn](http://scikit-learn.org/stable/)
- [matplotlib](http://matplotlib.org/)

We will also need to have software installed to run and execute a [Jupyter Notebook](http://ipython.org/notebook.html)

We recommend installing [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 

### Code

This project contains three files:

- `P1-Predicting-Boston-Housing-Prices.ipynb`: This is the main file documenting the project.
- `housing.csv`: The project dataset. We'll load this data in the notebook.
- `visuals.py`: This Python script provides supplementary visualizations for the project. Do not modify.

The project is documented in the `P1-Predicting-Boston-Housing-Prices.ipynb` notebook file. We will also use the `visuals.py`Python file and the `housing.csv` dataset file. 

### Run

In a terminal or command window, navigate to the top-level project directory `P1-Predicting-Boston-Housing-Prices/` (that contains this README) and run one of the following commands:

```bash
ipython notebook P1-Predicting-Boston-Housing-Prices.ipynb
```  
or
```bash
jupyter notebook P1-Predicting-Boston-Housing-Prices.ipynb
```

This will open the Jupyter Notebook software and project file in our browser.

### Data

The modified Boston housing dataset consists of 489 data points, with each datapoint having 3 features. This dataset is a modified version of the Boston Housing dataset found on the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Housing).

**Features**
1.  `RM`: average number of rooms per dwelling
2. `LSTAT`: percentage of population considered lower status
3. `PTRATIO`: pupil-teacher ratio by town

**Target Variable**
4. `MEDV`: median value of owner-occupied homes
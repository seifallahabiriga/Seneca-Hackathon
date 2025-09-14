# ML Sport Project

## Overview
This project analyzes and predicts sports match outcomes using machine learning. The main working file is `3jeja_V2.ipynb`.

## Folder Structure
- `3jeja_LLM_version.ipynb`, `3jeja_V1.ipynb`, `3jeja_V2.ipynb`: Jupyter notebooks for data analysis and modeling.
- `my_model.pkl`: Trained machine learning model.
- `scrapped_data_sample/tweets.csv`: Sample of scraped tweets data.
- `training_data/`: Contains CSV files with team stats, matchday results, and league standings.

## Difference Between 3jeja Files

- **3jeja_V1.ipynb**:  
  The initial version of the analysis and modeling notebook. It includes basic data loading, cleaning, exploratory data analysis, and first attempts at feature engineering and model training.

- **3jeja_V2.ipynb**:  
  An improved version of V1. It features refined data preprocessing, enhanced feature engineering, improved model selection and evaluation, and possibly hyperparameter tuning and cross-validation.

- **3jeja_LLM_version.ipynb**:  
  This version incorporates Large Language Model (LLM) techniques. It uses LLMs for tasks such as text analysis or sentiment extraction from unstructured data (e.g., tweets), and may combine traditional ML with LLM outputs for richer predictions. it is still under work so it doesn't run and we reccomend using 3jeja_V2

## Data and Code Attribution

Some of the data and code used in this project are adapted from the [Football_Predictions](https://github.com/Oyoyo1/Football_Predictions.git) repository by Oyoyo1. Please refer to their repository for original resources and further information.

## Setup Instructions
1. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Open `3jeja_V2.ipynb` in Jupyter Notebook or VS Code.

## Usage
- Run the cells in `3jeja_V2.ipynb` to preprocess data, train models, and make predictions.
- Use `my_model.pkl` for loading the trained model in your applications.

## Data Sources
- `training_data/`: Contains all relevant match and team statistics for the 2023 season.
- `scrapped_data_sample/`: Contains sample social media data.

## Notes
- Ensure all required packages are installed before running the notebooks.
- Update data files as needed for new seasons or additional analysis.
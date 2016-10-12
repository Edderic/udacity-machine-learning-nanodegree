# README

## Code

The goal of this project is to predict when new students at Lingo Live are
going to take lessons. This project uses Python 2.7.11 and iPython Notebooks
(version 3.1.0).

### Overview

- `Scheduling Patterns.ipynb` is an iPython Notebook that goes opens the
  anonymized lesson request data (`data/export lesson requests 2016 09 08.pkl`)
and aggregates them into schedules for each user (`unique_user_summaries.pkl`).

- The predictions of different models over months of test data is done through
  `code/main.py`, which uses `unique_user_summaries.pkl` to generate the
predictions (`x_model_errors.pkl`).

- Sensitivity analysis is done through `code/sensitivity analysis.py`.

- Graphs of errors and the accompanying tables were then generated through
  `Predictions.ipynb`, which makes use of `x_model_errors.pkl`.

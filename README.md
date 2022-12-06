# Git Predict

## Predict Transition

This is a "simple" NLP exercise. The goal is to recreate the diff patch method: we provide a source code, a patch and we need to predict the resulting code.
The intention behind this exercise is to get familiar with NLP problems and Git knowledges.

### Run

1. `python download.py`: download the most popular repositories
2. `python parse_commit.py`: parse the repositories to get "transactions" data.
3. `python train.py`

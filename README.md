# 🏡 Property Recommender

An AI-powered property recommendation system using Linear Regression, A\* ranking, and Reinforcement Learning personalisation.

## Project Structure

```
property_recommender/
├── data/
│   └── dataset.xlsx          # Property dataset
├── preprocessing/
│   └── data_preprocessing.py # Data loading & encoding
├── models/
│   └── model.py              # Linear Regression training
├── core/
│   └── recommender.py        # Recommendation pipeline
├── algorithms/
│   └── astar.py              # A* ranking algorithm
├── rl/
│   └── rl.py                 # RL preference agent
├── utils/
│   └── utils.py              # Pretty-print helpers
├── main.py                   # Entry point
└── requirements.txt
```

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python main.py
```

### 3. Follow the prompts
```
Enter Budget: 800000
Min Bedrooms: 3
Min Bathrooms: 2
```

The system will display the top matching properties and ask for feedback to personalise future results.

## How It Works

| Step | Component | Description |
|------|-----------|-------------|
| 1 | Preprocessing | Loads Excel data, forward-fills missing values, one-hot encodes categorical columns |
| 2 | Model | Trains a Linear Regression model to predict property prices |
| 3 | Filter | Filters properties by budget, bedrooms, and bathrooms |
| 4 | A\* Ranking | Ranks filtered properties by combined price + distance score |
| 5 | RL Scoring | Personalises ranking based on user like/dislike feedback |

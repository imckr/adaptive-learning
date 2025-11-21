# Math Adventure - AI-powered Adaptive Learning Prototype

An AI-driven adaptive math learning prototype designed to dynamically adjust puzzle difficulty based on learner performance.
The system helps children (ages 5–10) practice basic math (addition, subtraction, multiplication, and division) while staying in their optimal challenge zone.

## Architecture

![alt text](architecture.png)

## Features

- **Math Puzzle Generator** : Creates random math problems at Easy, Medium, and Hard levels.

- **Performance Tracker** : Logs correctness and response time for each puzzle.

- **Adaptive Engine(ML + Rule-Based)** : Predicts the next difficulty level using a hybrid of logistic regression and rule-based logic.

- **Performance Summary & Graph** : Displays overall accuracy, average time, and recommended next level.

- **CLI Interface** : Simple console flow for easy testing and demonstration.

## Project Structure

- adaptive-learning-prototype/
  - ml_based/
    - requirements.txt
    - README.md
    - src /
      - main.py
      - puzzle_generator.py
      - tracker.py
      - adaptive_engine.py

  - rule_based/ # same as above

## Installation

> ### Clone the repository
```
git clone https://github.com/imckr/Adaptive-learning-prototype.git

cd Adaptive-learning-prototype/ml_based
```

> ### Install dependencies
```
pip install -r requirements.txt
```

> ### Run the prototype
```
python src/main.py
```

## How to play

1. Run the game - you'll be asked to enter your name and starting difficulty (Easy / Medium / Hard).

2. Answer the math questions that appear.

3. The system records your correctness and response time.

4. After each question, difficulty, adjusts automatically based on your performance:
   - if you're doing well --> next question is harder.
   - if you're struggling --> next question is easier.

5. After all questions, you'll see:
   - Accuracy percentage.
   - Average response time.
   - Recommended next difficulty level.
   - A **graph** showing accuracy and response time trends.

## ML Model (Logistic Regression)

The ML engine is trained on `adaptive_training_data.csv`, which maps accuracy and response time to the most suitable next difficulty level.

- Input features: `accuracy`, `avg_time`
- Output label: `next_level`
- Model: Logistic Regression (scikit-learn)
- Scaling: StandardScaler for balanced feature influence

This allows smooth, data-driven transitions instead of hard-coded thresholds.

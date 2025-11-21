# CLI based Adaptive Learning Game (supports five subject)

### *AI-Powered Dynamic Quiz Generator with Adaptive Difficulty, ML Engine & Performance Tracking*

This project is an **interactive command-line learning game** that generates **dynamic, subject-specific MCQs** using the **OpenAI API**.
It includes a **machine-learning adaptive engine**, a **performance tracker**, and **visual performance graphs** to create a personalized learning experience.

---

### Architecture

<img width="4675" height="1992" alt="architecture" src="https://github.com/user-attachments/assets/a70b614b-bba0-44b3-85dd-d5129d5334c7" />


## Features

### **1. AI-Generated MCQs (OpenAI API)**

* Dynamically generates high-quality MCQs across subjects like Math, Science, History, Geography, and English.
* Ensures:

  * 4 consistent answer choices
  * Fully structured JSON output
  * Explanation for each question
  * Difficulty score (1–10)

---

### **2. Adaptive Difficulty Engine (ML-Powered)**

* Trained on a synthetic dataset that includes:

  * Accuracy %
  * Time taken
  * Streak
  * Subject
  * Current level
* Uses **Logistic Regression + StandardScaler** to recommend next difficulty level:

  * Easy → Medium
  * Medium → Hard
  * Hard → Medium/Easy (if user struggles)

---

### **3. Performance Tracking & Graphs**

Tracks:

* Accuracy over time
* Time taken per question
* Streaks
* Overall summary

Plots include:

* Accuracy trend line
* Response time graph

Uses **matplotlib** to render graphs.

---

### **4. CLI-Based Game Flow**

Simple, clean terminal interface:

```
Welcome to Quiz Adventures — AI-Powered MCQ Game
1. Start New Session
2. View Performance Summary
3. View Performance Graph
4. Exit
```

---

### **5. Modular Architecture**

Organized into clean files:

```
src/
 ├── main.py              # Entry point
 ├── mcq_generator.py     # OpenAI MCQ generator
 ├── performance_tracker.py
 ├── adaptive_engine.py    # ML difficulty engine
 └── data/
        training_data.csv
```

---

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/adaptive-learning.git
cd adaptive-learning
```

### 2. Create Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## Run the Game

```sh
python src/main.py
```

---

## Example MCQ JSON Output

```json
{
  "question": "What is the chemical symbol for water?",
  "choices": ["H2O", "O2", "CO2", "NaCl"],
  "answer_index": 0,
  "explanation": "Water consists of two hydrogen atoms bonded to one oxygen atom.",
  "difficulty_score": 2
}
```

---

## Future Improvements

* Add memory-based reinforcement learning
* Introduce user profiles & progress graphs
* Export progress reports
* Add web UI (FastAPI + React/Streamlit)
* Add leaderboard & gamification

---

## Contributing

Open for contributions!
Suggestions, PRs, improvements — all welcome.

---

## License

MIT License.

---

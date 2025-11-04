import time
import json
from mcq_generator import generate_mcq
from adaptive_engine import AdaptiveMLEngine
from validator import validate_mcq
from tracker import PerformanceTracker


def ask_mcq(mcq):
    """Display MCQ and get user response."""
    print("\n||||      Question:", mcq["question"])
    for i, c in enumerate(mcq["choices"]):
        print(f"||||      {i+1}. {c}")

    try:
        ans = int(input("\n||||      Your answer (1-4): ")) - 1
    except ValueError:
        ans = None

    correct = (ans is not None and ans == mcq["answer_index"])
    return correct


def start_new_session(tracker):

    adaptive_engine = AdaptiveMLEngine()
    """Run a new quiz session for a selected subject and difficulty."""

    print("\n||||      Starting a new session...")
    print("\n-----------------------------------")
    print("|     Choose subject:             |")
    print("|     1. Math                     |")
    print("|     2. Biology                  |")
    print("|     3. Indian Law               |")
    print("|     4. Geography                |")
    print("|     5. English                  |")
    print("|     6. Back                     |")
    print("-----------------------------------")

    subject_choice = input("||||      : ")

    subjects = {
        "1": "Math",
        "2": "Biology",
        "3": "Indian Law",
        "4": "Geography",
        "5": "English"
    }

    topic = input("||||      Topic : ")

    if subject_choice == "6" or subject_choice not in subjects:
        return None

    subject = subjects[subject_choice]

    print("\n-----------------------------------")
    print("|     Choose difficulty level:    |")
    print("|     1. Easy                     |")
    print("|     2. Medium                   |")
    print("|     3. Hard                     |")
    print("|     4. Back                     |")
    print("-----------------------------------")

    diff_choice = input("||||      : ")
    difficulties = {"1": "easy", "2": "medium", "3": "hard"}

    if diff_choice == "4" or diff_choice not in difficulties:
        return None

    difficulty = difficulties[diff_choice]
    print(f"\n||||      Session started: {subject} ({difficulty.title()})")
    print("||||      You will be asked 5 questions.\n")

    past_questions = []
    # Track performance
    perf = {"total": 0, "correct": 0, "start_time": time.time()}

    for i in range(5):
        print(f"\n-----------------------------------\n||||      Q{i+1} of 5")

        mcq = generate_mcq(subject, difficulty, past_questions, topic)
        past_questions.append(mcq["question"])
        ok, reason = validate_mcq(mcq)
        if not ok:
            print("||||      Invalid MCQ generated:", reason)
            print("||||      Skipping question...\n")
            continue

        perf["total"] += 1
        start_time = time.time()
        correct = ask_mcq(mcq)
        end_time = time.time()
        time_taken = end_time - start_time

        if correct:
            print("\n||||      ✅ Correct!")
            print(f"||||      Explanation: {mcq.get('explanation', 'N/A')}\n")
            perf["correct"] += 1
        else:
            ans_idx = mcq["answer_index"]
            print(f"\n||||      ❌ Wrong.")
            print(f"||||      Correct answer: {mcq['choices'][ans_idx]}")
            print(f"||||      Explanation: {mcq.get('explanation', 'N/A')}\n")

        # Record each question in tracker
        tracker.record_performance(level=difficulty, correct=correct, time_taken=time_taken)
        difficulty_index = adaptive_engine.predict_next_level(subject, (perf["correct"]/perf["total"])*100, time_taken, tracker.get_streak(), tracker.get_current_level())
        if difficulty_index == 1:
            difficulty = "easy"
        elif difficulty_index == 2:
            difficulty = "medium"
        else:
            difficulty = "hard"

    perf["end_time"] = time.time()
    perf["duration"] = perf["end_time"] - perf["start_time"]

    # Compute summary
    summary = tracker.get_summary()

    print("\n--------------------------------------------------------------------------")
    print(f"Performance Summary for {tracker.name}")
    print("--------------------------------------------------------------------------")
    print(f"         Subject: {subject}")
    print(f"         Difficulty: {difficulty}")
    print(f"         Total Questions: {perf['total']}")
    print(f"         Correct Answers: {perf['correct']}")
    print(f"         Accuracy: {summary['accuracy']*100:.2f}%")
    print(f"         Average Time per Question: {summary['avg_time']:.2f}s")
    print(f"         Recommended Next Level: {summary['recommended_level']}")
    print(f"         Total Duration: {perf['duration']:.2f}s")
    print("--------------------------------------------------------------------------")
    print("         Great job! Returning to main menu...")
    print("--------------------------------------------------------------------------")

    return summary


def main():
    """Main game loop for the adaptive MCQ game."""

    # Welcome message
    print("---------------------------------------------------------------")
    print("       Welcome to Quiz Adventures — AI-Powered MCQ Game        ")
    print("---------------------------------------------------------------")

    name = input("\n||||      Enter your name: ")
    print(f"||||      Hello, {name}! Let's begin your learning journey.\n")

    tracker = PerformanceTracker(name)
    # adaptive_engine = AdaptiveMLEngine()
    performance_history = []
    active = True

    while active:
        print("\n-----------------------------------")
        print("|       Choose an option:         |")
        print("|     1. Start New Session        |")
        print("|     2. View Performance Summary |")
        print("|     3. View Performance Graph   |")
        print("|     4. Exit                     |")
        print("-----------------------------------")

        choice = input("||||      : ")

        if choice == "1":
            summary = start_new_session(tracker)
            if summary:
                performance_history.append(summary)

        elif choice == "2":
            print("\n||||      Fetching performance data...")
            summary = tracker.get_summary()

            print("\n--------------------------------------------------------------------------")
            print("|                      Session Summary:                                  |")
            print("--------------------------------------------------------------------------")
            print(f"         Total Attempts: {summary['total_attempts']}")
            print(f"         Correct Answers: {summary['correct_answers']}")
            print(f"         Accuracy: {summary['accuracy']*100:.2f}%")
            print(f"         Average Time: {summary['avg_time']:.2f}s")
            print(f"         Recommended Next Level: {summary['recommended_level']}")
            print("--------------------------------------------------------------------------")

        elif choice == "3":
            print("\n||||      Generating performance graph...")
            tracker.plot_performance(username=name)

        elif choice == "4":
            print("\n||||      Exiting the program. Goodbye!")
            active = False

        else:
            print("\n||||      Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

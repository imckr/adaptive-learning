import matplotlib.pyplot as plt
import time


class PerformanceTracker:
    """
    Tracks user performance (accuracy, time, difficulty) and 
    provides summaries, recommendations, and performance graphs.
    """

    def __init__(self, name: str):
        self.name = name
        self.records = []
        self.accuracy = 0.0
        self.avg_time = 0.0

    # --------------------------------------------------------------------------
    # Record Management
    # --------------------------------------------------------------------------

    def record_performance(self, level, correct: bool, time_taken: float):
        """
        Record performance for a single question/puzzle attempt.
        """
        self.records.append({
            "name": self.name,
            "level": level,
            "correct": correct,
            "time_taken": time_taken,
        })

    # --------------------------------------------------------------------------
    # Summary Methods
    # --------------------------------------------------------------------------

    def get_summary(self):
        """
        Compute summary statistics from performance records.
        Returns:
            dict: Summary including total attempts, accuracy, avg_time, etc.
        """
        summary = {
            "name": self.name,
            "total_attempts": 0,
            "correct_answers": 0,
            "accuracy": 0.0,
            "avg_time": 0.0,
            "recommended_level": "N/A"
        }

        if not self.records:
            return summary

        total_attempts = len(self.records)
        correct_count = sum(1 for r in self.records if r["correct"])
        accuracy = correct_count / total_attempts
        avg_time = sum(r["time_taken"] for r in self.records) / total_attempts
        current_level = self.records[-1]["level"]

        summary.update({
            "total_attempts": total_attempts,
            "correct_answers": correct_count,
            "accuracy": accuracy,
            "avg_time": avg_time,
            "recommended_level": self.get_recommended_level(current_level)
        })

        return summary

    # --------------------------------------------------------------------------
    # Adaptive Recommendation Logic
    # --------------------------------------------------------------------------

    def get_recommended_level(self, current_level=None):
        """
        Recommend next difficulty level based on current performance.
        Levels are represented as integers (1=Easy, 2=Medium, 3=Hard).
        """
        if not self.records:
            return 1  # Default to Easy if no data

        accuracy = sum(1 for r in self.records if r["correct"]) / len(self.records)
        avg_time = sum(r["time_taken"] for r in self.records) / len(self.records)

        # Rule-based adaptive logic
        if current_level is not None:
            if current_level == 1 and accuracy > 0.8:
                return 2
            elif current_level == 2 and accuracy > 0.8 and avg_time < 10:
                return 3
            elif current_level == 3 and (accuracy < 0.5 or avg_time > 20):
                return 2

        # Fallback general recommendation
        if accuracy > 0.8 and avg_time < 10:
            return 3
        elif accuracy < 0.5 or avg_time > 20:
            return 1
        else:
            return 2

    # --------------------------------------------------------------------------
    # Visualization
    # --------------------------------------------------------------------------

    def plot_performance(self, username=None):
        """
        Plot user performance trends — accuracy and response time over attempts.
        """
        if not self.records:
            print("||||      No performance data available to plot.")
            return

        username = username or self.name

        # Prepare data
        q_numbers = list(range(1, len(self.records) + 1))
        cumulative_correct = 0
        accuracy_progress = []
        times = []

        for i, record in enumerate(self.records):
            cumulative_correct += 1 if record["correct"] else 0
            accuracy = (cumulative_correct / (i + 1)) * 100
            accuracy_progress.append(accuracy)
            times.append(record["time_taken"])

        # Plot performance
        plt.figure(figsize=(8, 5))
        plt.plot(q_numbers, accuracy_progress, marker="o", label="Accuracy (%)", linewidth=2)
        plt.plot(q_numbers, times, marker="s", label="Response Time (s)", linewidth=2)
        plt.title(f"Performance Trend — {username}", fontsize=13, fontweight="bold")
        plt.xlabel("Question Number", fontsize=11)
        plt.ylabel("Value", fontsize=11)
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

    # --------------------------------------------------------------------------
    # ML Training Preparation
    # --------------------------------------------------------------------------

    def get_training_data(self):
        """
        Prepare past performance data for ML training (accuracy vs. avg_time).
        Returns:
            tuple: (list of dicts for input features, list of levels)
        """
        if not self.records:
            return [], []

        performance_data = []
        recommended_levels = []

        for r in self.records:
            performance_data.append({
                "accuracy": 1 if r["correct"] else 0,
                "avg_time": r["time_taken"]
            })
            recommended_levels.append(r["level"])

        return performance_data, recommended_levels
    
    def get_streak(self):
        """
        Get current correct answer streak.
        """
        streak = 0
        for record in reversed(self.records):
            if record["correct"]:
                streak += 1
            else:
                break
        return streak
    
    def get_current_level(self):
        """
        Get the current difficulty level based on the last record.
        """
        if not self.records:
            return 1  # Default to Easy if no data
        return self.records[-1]["level"]

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smart_budget_buddy.pipeline.main_workflow import run_pipeline

if __name__ == "__main__":
    student_id = 0
    if len(sys.argv) > 1:
        try:
            student_id = int(sys.argv[1])
        except ValueError:
            pass
    run_pipeline(student_id)

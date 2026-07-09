"""Entry point.
Single run:      python main.py
Scheduled loop:  python main.py --schedule"""
import sys, json
from orchestrator.graph import run_pipeline
from config import RUN_INTERVAL_HOURS, MOCK_MODE

def main():
    print(f"=== Competitive Creative Intelligence Engine (mock={MOCK_MODE}) ===")
    result = run_pipeline()
    print(json.dumps({k: v for k, v in result.items() if k != "brief"},
                     indent=2, default=str))
    print("\nOpen the dashboard:  streamlit run dashboard/app.py")

if __name__ == "__main__":
    if "--schedule" in sys.argv:
        from apscheduler.schedulers.blocking import BlockingScheduler
        sched = BlockingScheduler()
        sched.add_job(main, "interval", hours=RUN_INTERVAL_HOURS)
        main()
        print(f"Scheduler active: pipeline will re-run every {RUN_INTERVAL_HOURS}h. Ctrl+C to stop.")
        sched.start()
    else:
        main()
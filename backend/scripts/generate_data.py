import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.data.generator import generate_experiment_events


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[2] / "data" / "generated_experiment_events.csv"
    events = generate_experiment_events(path)
    print(f"Generated {len(events):,} experiment rows at {path}")

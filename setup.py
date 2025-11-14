import pandas as pd

from config import PROJECT_ROOT

store_dir = PROJECT_ROOT / "store"
prompt_dir = PROJECT_ROOT / "prompts"
store_dir.mkdir(exist_ok=True)
prompt_dir.mkdir(exist_ok=True)

primitive_response_path = store_dir / "primitive_response.csv"
if not primitive_response_path.exists():
    primitive_response_path.touch(exist_ok=True)
    pd.DataFrame(
        columns=pd.Index(["video_topic", "scenario", "size", "response"])
    ).to_csv(primitive_response_path, index=False)


temporal_response_path = store_dir / "temporal_response.csv"
if not primitive_response_path.exists():
    primitive_response_path.touch(exist_ok=True)
    pd.DataFrame(
        columns=pd.Index(["video_topic", "scenario", "size", "n_prev", "response"])
    ).to_csv(primitive_response_path, index=False)

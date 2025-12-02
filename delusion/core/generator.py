import json
import random
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader

from config import PROJECT_ROOT

from ..api.local_llm import LocalLLM


class DataGenerator:
    def __init__(self, model: str, base_url: str):
        self.store_dir, self.prompt_dir = self._check_dir()
        self.llm = LocalLLM(model=model, base_url=base_url)
        self.prompt_env = Environment(loader=FileSystemLoader(self.prompt_dir))

    def _check_dir(self) -> Path:
        store_dir = PROJECT_ROOT / "store"
        prompt_dir = PROJECT_ROOT / "prompts"
        if store_dir.exists() and prompt_dir.exists():
            return store_dir, prompt_dir
        else:
            raise FileNotFoundError(
                "Required directories do not exist. Please run setup.py to create them."
            )

    def _prompt_loader(self, file_name: str, context_data: dict) -> str:
        template = self.prompt_env.get_template(file_name)
        prompt = template.render(data=context_data)
        print(prompt)
        msg = [{"role": "user", "content": prompt}]
        return msg

    def generate_data(self, data_type: str) -> str:
        if data_type == "primitive":
            prompt_file = "primitive_v4.j2"
        elif data_type == "temporal":
            prompt_file = "temporal_v2.j2"

        # Using random choices for size and n_prev with equal weights
        size_list = ["mid-length", "long and detailed"]
        size_weight = [1, 1]
        prev_n_list = ["2", "3", "4", "5", "6"]
        prev_n_weight = [1, 1, 1, 1, 1]

        with open(self.store_dir / "topic.json", "r") as f:
            all_topic = json.load(f)

        with open(self.store_dir / "scenario.json", "r") as f:
            all_scenario = json.load(f)

        for i, scenario in enumerate(all_scenario):
            for j, topic in enumerate(all_topic):
                context_data = {
                    "video_topic": topic,
                    "scenario": scenario,
                    "size": random.choices(size_list, weights=size_weight)[0],
                }

                if data_type == "temporal":
                    context_data["n_prev"] = random.choices(
                        prev_n_list, weights=prev_n_weight
                    )[0]

                msg = self._prompt_loader(prompt_file, context_data)
                print(msg)
                print("=" * 50)
                print("Generating response...")
                print("=" * 50)
                response = self.llm.response(msg)
                if data_type == "temporal":
                    temporal_response_path = self.store_dir / "temporal_response.csv"
                    save_format = {
                        "video_topic": [topic],
                        "scenario": [scenario],
                        "size": [context_data["size"]],
                        "n_prev": [context_data["n_prev"]],
                        "response": [response],
                    }
                    pd.DataFrame(save_format).to_csv(
                        temporal_response_path, mode="a", header=False, index=False
                    )
                elif data_type == "primitive":
                    primitive_response_path = self.store_dir / "primitive_response.csv"
                    save_format = {
                        "video_topic": [topic],
                        "scenario": [scenario],
                        "size": [context_data["size"]],
                        "response": [response],
                    }
                    pd.DataFrame(save_format).to_csv(
                        primitive_response_path, mode="a", header=False, index=False
                    )
                print(
                    f"Generated data for topic {j}: {topic}, scenario {i}: {scenario}"
                )
                break
            break

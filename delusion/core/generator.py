import json
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
        return prompt

    def generate_data(self, data_type: str, size: str) -> str:
        if data_type == "primitive":
            prompt_file = "primitive.j2"

        with open(self.store_dir / "topic.json", "r") as f:
            all_topic = json.load(f)

        with open(self.store_dir / "scenario.json", "r") as f:
            all_scenario = json.load(f)

        for i, topic in enumerate(all_topic):
            for j, scenario in enumerate(all_scenario):
                context_data = {
                    "video_topic": topic,
                    "scenario": scenario,
                    "size": size,
                }
                prompt = self._prompt_loader(prompt_file, context_data)
                print(prompt)
                response = self.llm.chat(prompt)
                primitive_response_path = self.store_dir / "primitive_response.csv"
                save_format = {
                    "video_topic": [topic],
                    "scenario": [scenario],
                    "size": [size],
                    "response": [response],
                }
                pd.DataFrame(save_format).to_csv(
                    primitive_response_path, mode="a", header=False, index=False
                )
                print(
                    f"Generated data for topic {i}: {topic}, scenario {j}: {scenario}"
                )

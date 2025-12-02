from delusion.core.generator import DataGenerator

model = {"0": "Qwen3-8B-Q8_0.gguf"}
base_url = "http://127.0.0.1:8000/v1"

# Run the setup.py -> run.py

data = DataGenerator(model["0"], base_url)
data.generate_data("primitive")

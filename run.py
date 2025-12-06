from delusion.core.generator import DataGenerator

model = {
        "0": "Qwen3-8B-Q8_0.gguf",
        "1": "gpt-oss-20b-F16.gguf"
         }

base_url = "http://127.0.0.1:8000/v1"

# Run the setup.py -> run.py

data = DataGenerator(model["1"], base_url)
data.generate_data("primitive")

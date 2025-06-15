mkdir -p ~/.venv/rkllm-gradio/
python3 -m venv ~/.venv/rkllm-gradio/
source ~/.venv/rkllm-gradio/bin/activate
python3 -m pip install --no-cache-dir --upgrade -r requirements.txt
deactivate

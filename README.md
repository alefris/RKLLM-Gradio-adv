Run with PYTHON:
1) Pull this repository
2) Create a /model folder on your fs, where to store the model files
3) Download the LLM models from https://huggingface.co/c01zaut⁠ (already converted to the .rkllm format) or other huggingface repositories (search for rkllm or RK3588).
4) If the model definition is not yet present in the file _model_configs.py_, update the model_configs dictionary in _model_configs.py_ with the filename of the model and tweak the hyperparameters as recommended in the model card or how you see fit. 
5) Create a virtual Python environment with: _python -m venv <environment_name>_
6) Start the environment with: _source ./bin/activate_
7) Start the Graio app with: _python rkllm_server_gradio.py_
8) Open http://localhost:1212

Run with DOCKER CONTAINER
1) Run the image (tag: 1.1.4) with:
```
docker run --privileged -v /models:/app/models -p 1212:1212 alefris/rkllm-gradio-adv:1.1.4
```
Alternatively, you can use this docker compose:
```
services:
  chatbot:
    container_name: "chatbot"
    hostname: "chatbot"
    image: "alefris/rkllm-gradio-adv:1.1.4"
    networks:
      - internal
    ports:
      - "1212:1212/tcp"
    privileged: "true"
    restart: "unless-stopped"
    volumes:
      - "/models:/app/models"
```
Notes:
- _/models_ is the local folder where you downloaded your model files
- _1212_ is the local TCP port where the web server will be created
- _--privileged_ is needed for the NPU access
- Your container needs Internet access in order to download the models configuration files from huggingface.co. Those files will be stored in your /models folder

LATEST UPDATES (branch:1.1.4):
- Improved layout theme
- Added sliders for model hyperparameters
- Added button to reload model with custom hyperparameters

Notes:
- For the dark theme (which looks better than the light one), add "?__theme=dark" at the end of the URL you use, example: https://chatbot.mydomain.com/?__theme=dark⁠
- You can change the theme settings from the file "rkllm_server_gradio.py", section "theme". For the theme parameters, you can use the Gradio Theme Builder, on https://www.gradio.app/guides/theming-guide⁠

Credits:
- https://github.com/c0zaut/rkllm-gradio⁠
- https://github.com/fabiomatricardi/smolLM2-GradioChatbot⁠

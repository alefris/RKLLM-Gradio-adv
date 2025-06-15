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
1) Run the image (tag: 1.1.4_beta) with:
```
docker run --privileged -v /models:/app/models -v /sys/kernel/debug/rknpu/load:/rknpu_load:ro -e RESMON_STYLE=simple -e RESMON_FREQUENCY=2 -p 1212:1212 alefris/rkllm-gradio-adv:1.1.4_beta
```
Alternatively, you can use this docker compose:
```
services:
  chatbot:
    container_name: "chatbot"
    environment:
      - "RESMON_STYLE=simple"
      - "RESMON_FREQUENCY=2"
    hostname: "chatbot"
    image: "alefris/rkllm-gradio-adv:1.1.4_beta"
    networks:
      - internal
    ports:
      - "1212:1212/tcp"
    privileged: "true"
    restart: "unless-stopped"
    volumes:
      - "/models:/app/models"
      - "/sys/kernel/debug/rknpu/load:/rknpu_load:ro"
```
Notes:
- _/models_ is the local folder where you downloaded your model files
- _1212_ is the local TCP port where the web server will be created
- _--privileged_ is needed for the NPU access
- RESMON_STYLE controls the layout of the Rseource Monitor panel and can be set to simple or full. Full will show more details, simple just the basic ones
- RESMON_FREQUENCY sets the number of seconds for the Resource Monitor panel update frequency
- The bind mount of _/rknpu_load_ to _/sys/kernel/debug/rknpu/load_ is needed to read the NPU Load values and show them in the Resource monitor. Without the mount, the NPU Load will always show 0.00
- Your container needs Internet access in order to download the models configuration files from huggingface.co. Those files will be stored in your /models folder

LATEST UPDATES (branch:1.1.4_beta):
- Added button to "Unload module". In this way we can unload a model (and free up the resources) directly from the interface, without the need of stopping the container
- Activated "save_history=True" for the ChatInterface and added app key to identify the Gradio app. In this way you can create multiple chats and they will be preserved across browser sessions
- Added system prompt textbox below the hyperparameters sliders. A custom system prompt can be now entered when reloading a model (except for Gemma models, which do not support system prompt)
- Added Resources monitor (update frequency and style can be controlled by 2 variables inside the file: rkllm_server_gradio.py
- Added model configurations with an increased context length, such as:
        InternLM2.5-7B-Chat-1M (1M context length) --> model will load and work with a reduced 50K context length
        ahz-r3v/DeepSeek-R1-Distill-Qwen-7B-rk3588-rkllm-1.1.4 (32,768 context length) --> model will load and work with 32K context length
        limcheekin/Qwen2.5-7B-Instruct-1M-rk3588-1.1.4 (1M context length) --> model will load and work with a reduced 50K context length, occupying ~ 26Gb RAM
- More testing is needed: the library rkllm version 1.1.4 seems to have a context limit of 4096. Even if the model is able to load with 32K of 50K, it's not said that it will actually accept that many tokens.

Notes:
- For the dark theme (which looks better than the light one), add "?__theme=dark" at the end of the URL you use, example: https://chatbot.mydomain.com/?__theme=dark⁠
- You can change the theme settings from the file "rkllm_server_gradio.py", section "theme". For the theme parameters, you can use the Gradio Theme Builder, on https://www.gradio.app/guides/theming-guide⁠

Credits:
- https://github.com/c0zaut/rkllm-gradio⁠
- https://github.com/fabiomatricardi/smolLM2-GradioChatbot⁠

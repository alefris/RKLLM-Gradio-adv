Run with PYTHON:
1) Pull this repository
2) Create a /model folder on your fs, where to store the model files
3) Download the LLM files (extension .rkllm) from https://huggingface.co/c01zaut⁠ or other huggingface repositories (search for rkllm or RK3588). The files which will be recognized and loaded are the ones already listed in model_configs.py
4) You can download additional or different model files but you would then need to update the model definition within the file model_configs.py accordingly. If you add a new model, along with the filename and st_model_id, define the hyperparameters as recommended in the model card
5) Create a virtual Python environment with: python -m venv <environment_name>
6) Start the environment with: source ./bin/activate
7) Start the Gradio app with: python rkllm_server_gradio.py
8) Open http://localhost:1212

Run with DOCKER:

1) Start a container with the image (tag: 1.2.1):
```
docker run --privileged -v /models:/app/models -v /sys/kernel/debug/rknpu/load:/rknpu_load:ro -e RESMON_STYLE=simple -e RESMON_FREQUENCY=2 -p 1212:1212 alefris/rkllm-gradio-adv:1.2.1
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
    image: "alefris/rkllm-gradio-adv:1.2.1"
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
- /models is the local folder where you downloaded your model files
- 1212 is the local TCP port where the web server will be created
- privileged is needed for the NPU access
- RESMON_STYLE controls the layout of the Rseource Monitor panel and can be set to simple or full. Full will show more details, simple just the basic ones
- RESMON_FREQUENCY sets the number of seconds for the Resource Monitor panel update frequency
- The bind mount of /rknpu_load to /sys/kernel/debug/rknpu/load is needed to read the NPU Load values and show them in the Resource monitor. Without the mount, the NPU Load will always show 0.00
- Your container needs Internet access in order to download the models configuration files from huggingface.co. Those files will be stored in subfolders of your /models folder
- Concerning the model parameters, be aware of those indications:

| Parameter | Required | Description | Options |
| :-------- | :------- | :---------- | :------ |
| max_context_len | Required | Maximum context size for the model | Must be ≤ model's max_context and in any case ≤ 16384 (constraint of rkllm library v1.2.1) |
| max_new_tokens | Required | Max number of tokens to generate | Must be ≤ max_context_len |
| temperature | Required | Sampling temperature, affecting the randomness of token selection | Recommended range is between 0 and 2 |
| top_k | Required | Top-K sampling parameter for token generation | Recommended range is between 1 and 100 |
| top_p | Required | Top-P (nucleus) sampling parameter | Recommended range is between 0 and 1 |
| repeat_penalty | Required | Penalty for repeating tokens in generation | Recommended range is between 0 and 2 |
| frequency_penalty | Required | Penalizes frequent tokens during generation | Recommended range is between 0 and 2 |
| presence_penalty | Required | Penalizes tokens based on their presence in the input | Recommended range is between -1 and 1 |

LATEST UPDATES (branch:1.2.1):
- Updated library librkllmrt.so to version 1.2.1
- Updated ctypes_bindings.py and model_class.py to support library 1.2.1
- Added configuration for several some Qwen-3 models and Gemma3-4B (downloaded from Rockchip repository, since all the Gemma-3 models on Huggingface behave strangely)
- Added environment variables to control resources monitor style and update frequency. Those can be sent from your docker run or compose environment
- Removed empty \<think>\</think> tag when thinking models are used in non-thinking mode
- Added slider and configuration for Presence Penalty

Abou the layout:
- For the dark theme (which looks better than the light one), add "?__theme=dark" at the end of the URL you use, example: https://chatbot.mydomain.com/?__theme=dark⁠
- You can change the theme settings from the file "rkllm_server_gradio.py", section "theme". For the theme parameters, you can use the Gradio Theme Builder, on https://www.gradio.app/guides/theming-guide⁠

Credits:
- https://github.com/c0zaut/rkllm-gradio⁠
- https://github.com/fabiomatricardi/smolLM2-GradioChatbot⁠

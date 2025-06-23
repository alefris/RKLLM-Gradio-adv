model_configs = {
    "Llama-3.2-Instruct": {
        "base_config": {
            "st_model_id": "c01zaut/Llama-3.2-3B-Instruct-rk3588-1.1.1",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 20,
            "top_p": 0.9,
            "temperature": 0.6,
            "repeat_penalty": 1.1,
            "frequency_penalty": 0.3,
            "presence_penalty": 0.0,
            "system_prompt": "You are Llama 3.2, an artificial intelligence model trained by Meta. You are a helpful assistant."
            },
        "models": {
            "Llama-3.2-3B-Instruct": {"filename": "Llama-3.2-3B-Instruct-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"},
            "Llama-3.2-1B-Instruct": {"filename": "Llama-3.2-1B-Instruct-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"}
        }
    },
    "Cogito-v1-Preview-14B": {
        "base_config": {
            "st_model_id": "limcheekin/cogito-v1-preview-qwen-14B-rk3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 20,
            "top_p": 0.9,
            "temperature": 0.5,
            "repeat_penalty": 1.1,
            "frequency_penalty": 0.3,
            "presence_penalty": 0.0,
            "system_prompt": "You are Cogito. You are a helpful assistant."
            },
        "models": {
            "Cogito-v1-Preview-14B": {"filename": "cogito-v1-preview-qwen-14B-rk3588-w8a8_g128-opt-1-hybrid-ratio-0.0.rkllm"}
        }
    },
    "SmolLM2-1.7B-Instruct": {
        "base_config": {
            "st_model_id": "Venator2025/SmolLM2-1.7B-Instruct-rk3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.9,
            "temperature": 0.1,
            "repeat_penalty": 1.35,
            "frequency_penalty": 1.0,
            "presence_penalty": 0.0,
            "system_prompt": "You are a helpful AI assistant. Wait for the user to ask a question before responding."
        },
        "models": {
            "SmolLM2-1.7B-Instruct": {"filename": "SmolLM2-1.7B-Instruct-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "Phi3.5-Mini-Instruct": {
        "base_config": {
            "st_model_id": "c01zaut/Phi-3.5-mini-instruct-rk3588-1.1.2",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.8,
            "temperature": 0.7,
            "repeat_penalty": 1.1,
            "frequency_penalty": 0.9,
            "presence_penalty": 0.0,
            "system_prompt": "You are Phi 3.5 Mini, an artificial intelligence model trained by Microsoft. You are a helpful AI assistant."
        },
        "models": {
            "Phi3.5-Mini-Instruct": {"filename": "Phi-3.5-mini-instruct-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "Qwen-3-14B-base": {
        "base_config": {
            "st_model_id": "dulimov/Qwen3-14B-rk3588-1.2.1-base",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 20,
            "top_p": 0.8,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant. /no_think"
        },
        "models": {
            "Qwen-3-14B-base": {"filename": "Qwen3-14B-rk3588-w8a8-opt-1-hybrid-ratio-0.5.rkllm"}
        },
    },
    "Qwen-3-8B-16K": {
        "base_config": {
            "st_model_id": "dulimov/Qwen3-8B-rk3588-1.2.1-unsloth-16k",
            "max_context_len": 16384,
            "max_new_tokens": 8192,
            "top_k": 20,
            "top_p": 0.8,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant. /no_think"
        },
        "models": {
            "Qwen-3-8B-16K": {"filename": "Qwen3-8B-rk3588-w8a8_g128-opt-0-hybrid-ratio-0.5.rkllm"}
        },
    },
    "Qwen-3-4B-16K": {
        "base_config": {
            "st_model_id": "dulimov/Qwen3-4B-rk3588-1.2.1-unsloth-16k",
            "max_context_len": 16384,
            "max_new_tokens": 8192,
            "top_k": 20,
            "top_p": 0.8,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant. /no_think"
        },
        "models": {
            "Qwen-3-4B-16K": {"filename": "Qwen3-4B-rk3588-w8a8_g128-opt-0-hybrid-ratio-0.5.rkllm"}
        },
    },
    "Qwen-3-1.7B-16K": {
        "base_config": {
            "st_model_id": "dulimov/Qwen3-1.7B-rk3588-1.2.1-unsloth-16k",
            "max_context_len": 16384,
            "max_new_tokens": 8192,
            "top_k": 20,
            "top_p": 0.8,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant. /no_think"
        },
        "models": {
            "Qwen-3-1.7B-16K": {"filename": "Qwen3-1.7B-rk3588-w8a8_g128-opt-0-hybrid-ratio-0.5.rkllm"}
        },
    },
    "Qwen-2.5-Instruct": {
        "base_config": {
            "st_model_id": "Qwen/Qwen2.5-14B-Instruct",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 5,
            "top_p": 0.8,
            "temperature": 0.2,
            "repeat_penalty": 1.00,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        },
        "models": {
            "Qwen2.5-1.5B-Instruct": {"filename": "Qwen2.5-1.5B-Instruct-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"},
            "Qwen2.5-3B-Instruct": {"filename": "Qwen2.5-3B-Instruct-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"},
            "Qwen2.5-7B-Instruct": {"filename": "Qwen2.5-7B-Instruct-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"},
            "Qwen2.5-Coder-7B-Instruct": {"filename": "Qwen2.5-Coder-7B-Instruct-rk3588-w8a8_g128-opt-1-hybrid-ratio-0.5.rkllm"},
            "Qwen2.5-Coder-1.5B-Instruct-w8a8-hybrid": {"filename": "Qwen2.5-Coder-1.5B-Instruct-rk3588-w8a8-opt-0-hybrid-ratio-1.0.rkllm"}
        },
    },
    "Qwen-2.5-Coder-14B-Instruct": {
        "base_config": {
            "st_model_id": "c01zaut/Qwen2.5-Coder-14B-Instruct-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 5,
            "top_p": 0.8,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        },
        "models": {
            "Qwen-2.5-Coder-14B-Instruct": {"filename": "Qwen2.5-Coder-14B-Instruct-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        },
    },
    "Qwen-2.5-Math-1.5B": {
        "base_config": {
            "st_model_id": "c01zaut/Qwen2.5-Math-1.5B-Instruct-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.8,
            "temperature": 0.9,
            "repeat_penalty": 1.00,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        },
        "models": {
            "Qwen-2.5-Math-1.5B": {"filename": "Qwen2.5-Math-1.5B-Instruct-rk3588-w8a8_g128-opt-0-hybrid-ratio-1.0.rkllm"}
        }
    },
    "Qwen-2.5-Math-7B": {
        "base_config": {
            "st_model_id": "c01zaut/Qwen2.5-Math-7B-Instruct-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.8,
            "temperature": 0.9,
            "repeat_penalty": 1.00,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        },
        "models": {
            "Qwen-2.5-Math-7B": {"filename": "Qwen2.5-Math-7B-Instruct-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "Qwen-2.5-Coder-1.5B": {
        "base_config": {
            "st_model_id": "c01zaut/Qwen2.5-Coder-1.5B-Instruct-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.8,
            "temperature": 0.9,
            "repeat_penalty": 1.00,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        },
        "models": {
            "Qwen-2.5-Coder-1.5B": {"filename": "Qwen2.5-Coder-1.5B-Instruct-rk3588-w8a8_g128-opt-0-hybrid-ratio-0.5.rkllm"}
        }
    },
    "Marco-O1": {
        "base_config": {
            "st_model_id": "c01zaut/Marco-o1-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.8,
            "temperature": 0.9,
            "repeat_penalty": 1.00,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are a well-trained AI assistant, your name is Marco-o1. Created by AI Business of Alibaba International Digital Business Group.\n\n## IMPORTANT!!!!!!\nWhen you answer questions, your thinking should be done in <Thought>, and your results should be output in <Output>.\n<Thought> should be in English as much as possible, but there are 2 exceptions, one is the reference to the original text, and the other is that mathematics should use markdown format, and the output in <Output> needs to follow the language of the user input."
        },
        "models": {
            "Marco-o1": {"filename": "Marco-o1-rk3588-w8a8_g512-opt-0-hybrid-ratio-0.5.rkllm"}
        }
    },
    "OpenLongCoT-Base-Gemma2-2B": {
        "base_config": {
            "st_model_id": "c01zaut/OpenLongCoT-Base-Gemma2-2B-rk3588-1.1.1",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.8,
            "temperature": 0.1,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.0,
            "system_prompt": "You are a helpful assistant. Wait for the user to ask a question before responding."
        },
        "models": {
            "OpenLongCoT-Base-Gemma2-2B": {"filename": "OpenLongCoT-Base-Gemma2-2B-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"}
        }
    },
    "Gemma-3-4B-it": {
        "base_config": {
            "st_model_id": "datakurre/gemma-3-4b-it-rk3588-1.2.0",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 15,
            "top_p": 0.95,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.0,
            "system_prompt": "" #Gemma does not support system prompt
        },
        "models": {
            "Gemma-3-4B-it": {"filename": "gemma3_4b_w8a8_rk3588_h0.25.rkllm"}  #downloaded from https://meta.box.lenovo.com/v/link/view/ad7482f6712844b48902f07287ed3359  pwd:rkllm
        }
    },
    "Gemma-2-2B-it": {
        "base_config": {
            "st_model_id": "c01zaut/gemma-2-2b-it-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 15,
            "top_p": 0.95,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.0,
            "system_prompt": "" #Gemma does not support system prompt
        },
        "models": {
            "Gemma-2-2B-it-g256": {"filename": "gemma-2-2b-it-rk3588-w8a8_g256-opt-0-hybrid-ratio-0.0.rkllm"},
            "Gemma-2-2B-it": {"filename": "gemma-2-2b-it-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "Gemma-2-9B-it": {
        "base_config": {
            "st_model_id": "c01zaut/gemma-2-9b-it-rk3588-1.1.2",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 15,
            "top_p": 0.95,
            "temperature": 0.7,
            "repeat_penalty": 1.05,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.0,
            "system_prompt": "" #Gemma does not  support system prompt
        },
        "models": {
            "Gemma-2-9B-it": {"filename": "gemma-2-9b-it-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"},
            "Gemma-2-9B-it-g512": {"filename": "gemma-2-9b-it-rk3588-w8a8_g512-opt-1-hybrid-ratio-1.0.rkllm"}
        }
    },
    "InternLM-2.5-1.8B": {
        "base_config": {
            "st_model_id": "internlm/internlm2_5-1_8b-chat",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 30,
            "top_p": 0.8,
            "temperature": 0.5,
            "repeat_penalty": 1.0005,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are InternLM, a helpful, honest, and harmless AI assistant developed by Shanghai AI Laboratory."
        },
        "models": {
            "Internlm-2.5-1.8B-Chat-g512-opt": {"filename": "internlm2_5-1_8b-chat-rk3588-w8a8_g512-opt-1-hybrid-ratio-1.0.rkllm"},
            "Internlm-2.5-1.8B-Chat": {"filename": "internlm2_5-1_8b-chat-rk3588-w8a8-opt-0-hybrid-ratio-1.0.rkllm"},
            "Internlm-2.5-1.8B-Chat-opt": {"filename": "internlm2_5-1_8b-chat-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"}
        }
    },
    "InternLM-2.5-20B": {
        "base_config": {
            "st_model_id": "internlm/internlm2_5-20b-chat",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 30,
            "top_p": 0.8,
            "temperature": 0.5,
            "repeat_penalty": 1.0005,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are InternLM, a helpful, honest, and harmless AI assistant developed by Shanghai AI Laboratory."
        },
        "models": {
            "Internlm-2.5-20B-Chat-opt": {"filename": "internlm2_5-20b-chat-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"},
            "Internlm-2.5-20B-Chat-g512-opt": {"filename": "internlm2_5-20b-chat-rk3588-w8a8_g512-opt-1-hybrid-ratio-1.0.rkllm"},
            "Internlm-2.5-20B-Chat-g512": {"filename": "internlm2_5-20b-chat-rk3588-w8a8_g512-opt-0-hybrid-ratio-1.0.rkllm"}
        }
    },
    "InternLM-2.5-7B": {
        "base_config": {
            "st_model_id": "internlm/internlm2_5-7b-chat",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 30,
            "top_p": 0.8,
            "temperature": 0.5,
            "repeat_penalty": 1.0005,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.0,
            "system_prompt": "You are InternLM, a helpful, honest, and harmless AI assistant developed by Shanghai AI Laboratory."
        },
        "models": {
            "Internlm-2.5-7B-Chat-opt": {"filename": "internlm2_5-7b-chat-rk3588-w8a8-opt-1-hybrid-ratio-1.0.rkllm"}
        }
    },
    "Deepseek-Chat-7B": {
        "base_config": {
            "st_model_id": "c01zaut/deepseek-llm-7b-chat-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.9,
            "temperature": 0.7,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are DeepSeek Chat, a helpful, respectful and honest AI assistant developed by DeepSeek. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don’t know the answer to a question, please don’t share false information."
        },
        "models": {
            "Deepseek-Chat-7B": {"filename": "deepseek-llm-7b-chat-rk3588-w8a8_g256-opt-1-hybrid-ratio-0.5.rkllm"}
        }
    },
    "DeepSeek-R1-0528-Qwen-8B-16K": {
        "base_config": {
            "st_model_id": "dulimov/DeepSeek-R1-0528-Qwen3-8B-rk3588-1.2.1",
            "max_context_len": 16384,
            "max_new_tokens": 8192,
            "top_k": 1,
            "top_p": 0.95,
            "temperature": 0.6,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "Wait for the user to ask a question before responding. If the response is lengthy, structure it well and summarize it in paragraphs. Unless the user requests otherwise, your response should be in the same language as the user's question."
        },
        "models": {
            "DeepSeek-R1-0528-Qwen-8B-16K": {"filename": "DeepSeek-R1-0528-Qwen3-8B-rk3588-w8a8_g128-opt-0-hybrid-ratio-0.5.rkllm"}
        }
    },
    "DeepSeek-R1-Distill-Qwen-1.5B": {
        "base_config": {
            "st_model_id": "datakurre/DeepSeek-R1-Distill-Qwen-1.5B-rk3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.9,
            "temperature": 0.7,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "Wait for the user to ask a question before responding."
        },
        "models": {
            "DeepSeek-R1-Distill-Qwen-1.5B": {"filename": "DeepSeek-R1-Distill-Qwen-1.5B-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "DeepSeek-R1-Distill-Qwen-7B": {
        "base_config": {
            "st_model_id": "ahz-r3v/DeepSeek-R1-Distill-Qwen-7B-rk3588-rkllm-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 1,
            "top_p": 0.9,
            "temperature": 0.7,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "Wait for the user to ask a question before responding."
        },
        "models": {
            "DeepSeek-R1-Distill-Qwen-7B": {"filename": "DeepSeek-R1-Distill-Qwen-7B_W8A8_G128_RK3588_o0.rkllm"}
        }
    },
    "Deepseek-Coder-1.3B-Instruct": {
        "base_config": {
            "st_model_id": "c01zaut/deepseek-coder-1.3b-instruct-rk3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 50,
            "top_p": 0.95,
            "temperature": 0.8,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are Deepseek Coder, a helpful, respectful and honest AI assistant developed by DeepSeek."
        },
        "models": {
            "Deepseek-Coder-1.3B-Instruct": {"filename": "deepseek-coder-1.3b-instruct-rk3588-w8a8_g128-opt-1-hybrid-ratio-0.5.rkllm"}
        }
    },
    "Deepseek-Coder-7B-Instruct": {
        "base_config": {
            "st_model_id": "c01zaut/deepseek-coder-7b-instruct-v1.5-RK3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 50,
            "top_p": 0.95,
            "temperature": 0.8,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are Deepseek Coder, a helpful, respectful and honest AI assistant developed by DeepSeek."
        },
        "models": {
            "Deepseek-Coder-7B-Instruct": {"filename": "deepseek-coder-7b-instruct-v1.5-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "Deepseek-Math-7B-Instruct": {
        "base_config": {
            "st_model_id": "c01zaut/deepseek-math-7b-instruct-rk3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 40,
            "top_p": 0.9,
            "temperature": 0.6,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are Deepseek Coder, a helpful, respectful and honest AI assistant developed by DeepSeek."
        },
        "models": {
            "Deepseek-Math-7B-Instruct": {"filename": "deepseek-math-7b-instruct-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "MiniCPM3-4B": {
        "base_config": {
            "st_model_id": "c01zaut/MiniCPM3-4B-rk3588-1.1.4",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 50,
            "top_p": 0.7,
            "temperature": 0.7,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are MiniCPM, a helpful, respectful and honest AI assistant."
        },
        "models": {
            "MiniCPM3-4B": {"filename": "MiniCPM3-4B-rk3588-w8a8_g128-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    },
    "ChatGLM3-6B": {
        "base_config": {
            "st_model_id": "c01zaut/chatglm3-6b-rk3588-1.1.2",
            "max_context_len": 4096,
            "max_new_tokens": 4096,
            "top_k": 5,
            "top_p": 0.7,
            "temperature": 0.8,
            "repeat_penalty": 1.2,
            "frequency_penalty": 0.8,
            "presence_penalty": 0.0,
            "system_prompt": "You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's instructions carefully. Respond using markdown."
        },
        "models": {
            "ChatGLM3-6B": {"filename": "chatglm3-6b-rk3588-w8a8-opt-0-hybrid-ratio-0.0.rkllm"}
        }
    }
}

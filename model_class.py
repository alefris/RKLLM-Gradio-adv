from transformers import AutoTokenizer
from ctypes_bindings import *
from model_configs import model_configs
import threading
import time
import sys
import os

MODEL_PATH = "./models"

# Create a dict of various model configs, and then check the ./models directory if any exist
# This will become the content of the model selector's drop down menu
def available_models():
    if not os.path.exists(MODEL_PATH):
        os.mkdir(MODEL_PATH)
    # Initialize the dict of available models as empty
    rkllm_model_files = {}
    # Populate the dictionary with found models, and their base configurations
    for family, config in model_configs.items():
            for model, details in config["models"].items():
                filename = details["filename"]
                if os.path.exists(os.path.join(MODEL_PATH, filename)):
                    rkllm_model_files[model] = {}
                    rkllm_model_files[model].update({"name": model,"family": family, "filename": filename, "config": config["base_config"]})
    return rkllm_model_files

# Define the callback function
def callback_impl(result, userdata, state):
    global global_text, global_state, split_byte_data
    if state == LLMCallState.RKLLM_RUN_FINISH:
        global_state = state
        print("\n")
        sys.stdout.flush()
    elif state == LLMCallState.RKLLM_RUN_ERROR:
        global_state = state
        print("run error")
        sys.stdout.flush()
    elif state == LLMCallState.RKLLM_RUN_GET_LAST_HIDDEN_LAYER:
        '''
        If using the GET_LAST_HIDDEN_LAYER function, the callback interface will return the memory pointer: last_hidden_layer, the number of tokens: num_tokens, and the size of the hidden layer: embd_size.
        With these three parameters, you can retrieve the data from last_hidden_layer.
        Note: The data needs to be retrieved during the current callback; if not obtained in time, the pointer will be released by the next callback.
        '''
        if result.last_hidden_layer.embd_size != 0 and result.last_hidden_layer.num_tokens != 0:
            data_size = result.last_hidden_layer.embd_size * result.last_hidden_layer.num_tokens * ctypes.sizeof(ctypes.c_float)
            print(f"data_size: {data_size}")
            global_text.append(f"data_size: {data_size}\n")
            output_path = os.getcwd() + "/last_hidden_layer.bin"
            with open(output_path, "wb") as outFile:
                data = ctypes.cast(result.last_hidden_layer.hidden_states, ctypes.POINTER(ctypes.c_float))
                float_array_type = ctypes.c_float * (data_size // ctypes.sizeof(ctypes.c_float))
                float_array = float_array_type.from_address(ctypes.addressof(data.contents))
                outFile.write(bytearray(float_array))
                print(f"Data saved to {output_path} successfully!")
                global_text.append(f"Data saved to {output_path} successfully!")
        else:
            print("Invalid hidden layer data.")
            global_text.append("Invalid hidden layer data.")
        global_state = state
        time.sleep(0.05)
        sys.stdout.flush()
    else:
        # Save the output token text and the RKLLM running state
        global_state = state
        # Monitor if the current byte data is complete; if incomplete, record it for later parsing
        try:
            if split_byte_data == None or split_byte_data == "" or split_byte_data == '':
                global_text.append((b"" + result.contents.text).decode('utf-8'))
                print((split_byte_data + result.contents.text).decode('utf-8'), end='')
                split_byte_data = bytes(b"")
            else:
                global_text.append((split_byte_data + result.contents.text).decode('utf-8'))
                print((split_byte_data + result.contents.text).decode('utf-8'), end='')
                split_byte_data = bytes(b"")
        except:
            if result.contents.text is not None:
                split_byte_data += result.contents.text
        sys.stdout.flush()

# Connect the callback function between the Python side and the C++ side
callback_type = ctypes.CFUNCTYPE(None, ctypes.POINTER(RKLLMResult), ctypes.c_void_p, ctypes.c_int)
callback = callback_type(callback_impl)

class RKLLMLoaderClass:
#    def __init__(self, model="", qtype="w8a8", opt="1", hybrid_quant="1.0", maxnewtok=None, temp=None, freqpen=None, reppen=None, maxconlen=None, topk=None, topp=None, system_prompt=None):
    def __init__(self, model="", qtype="w8a8", maxnewtok=None, temp=None, freqpen=None, reppen=None, maxconlen=None, topk=None, topp=None, system_prompt=None):
        self.qtype = qtype
#        self.opt = opt
        self.model = model
#        self.hybrid_quant = hybrid_quant
        self.maxnewtok = maxnewtok
        self.temp = temp
        self.freqpen = freqpen
        self.reppen = reppen
        self.maxconlen = maxconlen
        self.topk = topk
        self.topp = topp
        self.system_prompt = system_prompt
        if self.model == "":
            print("No models loaded yet!")
        else:
            self.available_models = available_models()
            self.model = self.available_models[model]
            self.family = self.model["family"]
            self.model_path = "models/" + self.model["filename"]
            self.base_config = self.model["config"]
            self.model_name = self.model["name"]
            self.st_model_id = self.base_config["st_model_id"]
            if self.system_prompt is None:
             self.system_prompt = self.base_config["system_prompt"]
            else:
             self.system_prompt = self.system_prompt
             print("The System Prompt is " + str(self.system_prompt)) 
            self.rkllm_param = RKLLMParam()
            self.rkllm_param.model_path = bytes(self.model_path, 'utf-8')
            if self.maxconlen is None:
             self.rkllm_param.max_context_len = self.base_config["max_context_len"]
            else:
             self.rkllm_param.max_context_len = self.maxconlen
             print("The value of Max Content Lenght is set to " + str(self.rkllm_param.max_context_len))
            if self.maxnewtok is None:
             self.rkllm_param.max_new_tokens = self.base_config["max_new_tokens"]
            else:
             self.rkllm_param.max_new_tokens = self.maxnewtok
             print("The value of Max New Tokens is set to " + str(self.rkllm_param.max_new_tokens))
            self.rkllm_param.skip_special_token = True
            if self.topk is None:
             self.rkllm_param.top_k = self.base_config["top_k"]
            else:
             self.rkllm_param.top_k = self.topk
             print("The value of top_k is set to " + str(self.rkllm_param.top_k))
            if self.topp is None:
             self.rkllm_param.top_p = self.base_config["top_p"]
            else:
             self.rkllm_param.top_p = self.topp
             print("The value of top_p is set to " + str(self.rkllm_param.top_p))
            self.rkllm_param.n_keep = -1
            if self.temp is None:
             self.rkllm_param.temperature = self.base_config["temperature"]
            else:
             self.rkllm_param.temperature = self.temp
             print("The value of Temperature is set to " + str(self.rkllm_param.temperature))
            if self.reppen is None:
             self.rkllm_param.repeat_penalty = self.base_config["repeat_penalty"]
            else:
             self.rkllm_param.repeat_penalty = self.reppen
             print("The value of Repetition Penalty is set to " + str(self.rkllm_param.repeat_penalty))
            if freqpen is None:
             self.rkllm_param.frequency_penalty = self.base_config["frequency_penalty"]
            else:
             self.rkllm_param.frequency_penalty = self.freqpen
             print("The value of Frequency Penalty is set to " + str(self.rkllm_param.frequency_penalty))
             print()
            self.rkllm_param.presence_penalty = 0.0
            self.rkllm_param.mirostat = 0
            self.rkllm_param.mirostat_tau = 5.0
            self.rkllm_param.mirostat_eta = 0.1
            self.rkllm_param.is_async = False
            self.rkllm_param.img_start = "<image>".encode('utf-8')
            self.rkllm_param.img_end = "</image>".encode('utf-8')
            self.rkllm_param.img_content = "<unk>".encode('utf-8')
            self.rkllm_param.extend_param.base_domain_id = 0
            self.rkllm_param.extend_param.enabled_cpus_num = 4
            self.rkllm_param.extend_param.enabled_cpus_mask = (1 << 4)|(1 << 5)|(1 << 6)|(1 << 7)
            self.handle = RKLLM_Handle_t()
            self.rkllm_init = rkllm_lib.rkllm_init
            self.rkllm_init.argtypes = [ctypes.POINTER(RKLLM_Handle_t), ctypes.POINTER(RKLLMParam), callback_type]
            self.rkllm_init.restype = ctypes.c_int
            self.rkllm_init(self.handle, self.rkllm_param, callback)
            self.rkllm_run = rkllm_lib.rkllm_run
            self.rkllm_run.argtypes = [RKLLM_Handle_t, ctypes.POINTER(RKLLMInput), ctypes.POINTER(RKLLMInferParam), ctypes.c_void_p]
            self.rkllm_run.restype = ctypes.c_int

            self.set_chat_template = rkllm_lib.rkllm_set_chat_template
            self.set_chat_template.argtypes = [RKLLM_Handle_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
            self.set_chat_template.restype = ctypes.c_int
           # self.system_prompt = "<|im_start|>system You are a helpful assistant. <|im_end|>"
           # self.prompt_prefix = "<|im_start|>user"
           # self.prompt_postfix = "<|im_end|><|im_start|>assistant"
            self.prompt_prefix = ""
            self.prompt_postfix = ""
            self.set_chat_template(self.handle, ctypes.c_char_p(self.system_prompt.encode('utf-8')), ctypes.c_char_p(self.prompt_prefix.encode('utf-8')), ctypes.c_char_p(self.prompt_postfix.encode('utf-8')))

            self.rkllm_abort = rkllm_lib.rkllm_abort
            self.rkllm_abort.argtypes = [RKLLM_Handle_t]
            self.rkllm_abort.restype = ctypes.c_int
            self.rkllm_destroy = rkllm_lib.rkllm_destroy
            self.rkllm_destroy.argtypes = [RKLLM_Handle_t]
            self.rkllm_destroy.restype = ctypes.c_int



    # Record the user's input prompt
    def get_user_input(self, user_message, history):
        history = history + [[user_message, None]]
        return "", history
    def tokens_to_ctypes_array(self, tokens, ctype):
        # Converts a Python list to a ctypes array.
        # The tokenizer outputs as a Python list.
        return (ctype * len(tokens))(*tokens)
    # Run inference
    def run(self, prompt):
        self.rkllm_infer_params = RKLLMInferParam()
        ctypes.memset(ctypes.byref(self.rkllm_infer_params), 0, ctypes.sizeof(RKLLMInferParam))
        self.rkllm_infer_params.mode = RKLLMInferMode.RKLLM_INFER_GENERATE
        self.rkllm_input = RKLLMInput()
        self.rkllm_input.input_mode = RKLLMInputMode.RKLLM_INPUT_TOKEN
        self.rkllm_input.input_data.token_input.input_ids = self.tokens_to_ctypes_array(prompt, ctypes.c_int)
        self.rkllm_input.input_data.token_input.n_tokens = ctypes.c_ulong(len(prompt))
        self.rkllm_run(self.handle, ctypes.byref(self.rkllm_input), ctypes.byref(self.rkllm_infer_params), None)
        return
    # Release RKLLM object from memory
    def release(self):
        self.rkllm_abort(self.handle)
        self.rkllm_destroy(self.handle)
    # Retrieve the output from the RKLLM model and print it in a streaming manner
    def get_RKLLM_output(self, message, history):
        # Link global variables to retrieve the output information from the callback function
        global global_text, global_state
        global_text = []
        global_state = -1
        user_prompt = {"role": "user", "content": message}
        #history.append(user_prompt)
        # Gemma 2 does not support system prompt.
        if self.system_prompt == "":
            prompt = [user_prompt]
        else:
            prompt = [
                {"role": "system", "content": self.system_prompt},
                user_prompt
            ]
        # print(prompt)
        TOKENIZER_PATH="%s/%s"%(MODEL_PATH,self.st_model_id.replace("/","-"))
        if not os.path.exists(TOKENIZER_PATH):
            print("Tokenizer not cached locally, downloading to %s"%TOKENIZER_PATH)
            os.mkdir(TOKENIZER_PATH)
            tokenizer = AutoTokenizer.from_pretrained(self.st_model_id, trust_remote_code=True)
            tokenizer.save_pretrained(TOKENIZER_PATH)
        else:
            tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
        prompt = tokenizer.apply_chat_template(prompt, tokenize=True, add_generation_prompt=True)
        # response = {"role": "assistant", "content": "Loading..."}
        response = {"role": "assistant", "content": ""}
        #history.append(response)
        model_thread = threading.Thread(target=self.run, args=(prompt,))
        model_thread.start()
        model_thread_finished = False
        while not model_thread_finished:
            while len(global_text) > 0:
                response["content"] += global_text.pop(0)

                #Strip thinking tags if /no_think has been set in the prompt or in input message (reason: even if /no_think has been set, most models will anyhow output an empty <think> </think> tag)
                if ("/no_think" in self.system_prompt and not "/think" in message) or ("/think" in self.system_prompt and "/no_think" in message):
                  response["content"] = str(response["content"]).replace("<think>", " ")
                  response["content"] = str(response["content"]).replace("</think>", " ")

                # Marco-o1
                response["content"] = str(response["content"]).replace("<Thought>", "\\<Thought\\>")
                response["content"] = str(response["content"]).replace("</Thought>", "\\<\\/Thought\\>")
                response["content"] = str(response["content"]).replace("<Output>", "\\<Output\\>")
                response["content"] = str(response["content"]).replace("</Output>", "\\<\\/Output\\>")
                time.sleep(0.005)

                #Qwen-3
                response["content"] = str(response["content"]).replace("<think>", "\\<Thought\\>")
                response["content"] = str(response["content"]).replace("</think>", "\\<\\/Thought\\>")

                # Gradio automatically pushes the result returned by the yield statement when calling the then method
                yield response
            model_thread.join(timeout=0.005)
            model_thread_finished = not model_thread.is_alive()

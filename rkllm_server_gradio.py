import sys 
import resource
import time
import gradio as gr
import random
import string
import tiktoken
import datetime
import os  # Added import for os

#Added for system resource monitor
import subprocess
import psutil

from ctypes import *
from model_class import *
#from mesh_utils import *

# Set environment variables
os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
os.environ["GRADIO_SERVER_PORT"] = "1212"
os.environ["RKLLM_LOG_LEVEL"] = "1"

# Get environment variables for Resource Monitor style and update frequency, set defauts if not present
resmon_style = os.getenv('RESMON_STYLE', 'simple')
resmon_frequency = os.getenv('RESMON_FREQUENCY', 2)
resmon_frequency = int(resmon_frequency)

# Set path and name of logfile, use /dev/null to trash the output instead of saving it into a file
LOGFILENAME = "/dev/null"
# LOGFILENAME = genRANstring(5)

# Set resource limit
resource.setrlimit(resource.RLIMIT_NOFILE, (102400, 102400))

history = []

if __name__ == "__main__":
    rkllm_model = None  # Initialize rkllm_model as None


    if resmon_style == 'simple':
      resmon_panel_scale=1
    else:
      resmon_panel_scale=2


    def resmon():
       #I calculate the average of the 3 NPU cores usage %
        try:
           npu_usage = sum(float(p.split(':')[-1].strip().replace('%', '')) for p in open('/rknpu_load').read().strip().split(',') if 'Core' in p) / 3.0
        except FileNotFoundError:
        # Set npu_usage to 0.0 if the file /sys/kernel/debug/rknpu/load is not acessible - probably the bind mount was not set from the docker container
           npu_usage = 0.0
        cpu_usage = psutil.cpu_percent(percpu=False, interval=0.5)
        cpu_utl = psutil.cpu_times_percent(percpu=False, interval=0.5)
        cpu_sys = cpu_utl.system
        cpu_usr = cpu_utl.user
        cpu_idl = cpu_utl.idle
        load_avg = psutil.getloadavg()
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_total = ram.total / (1024 ** 3)
        ram_avail =  ram.available / (1024 ** 3)
        ram_used = ram_total - ram_avail
        disk_usage = psutil.disk_usage('/').percent
        disk_used = psutil.disk_usage('/').used / (1024 ** 3)
        disk_free = psutil.disk_usage('/').free / (1024 ** 3)
        disk_tot = psutil.disk_usage('/').total / (1024 ** 3) 
        net = psutil.net_io_counters(pernic=False, nowrap=True)
        sent_mb = net.bytes_sent / (1024 ** 2)
        recv_mb = net.bytes_recv / (1024 ** 2)
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as fcpu:
            tempcpu = float(fcpu.read()) / 1000.0
        with open('/sys/class/thermal/thermal_zone5/temp', 'r') as fgpu:
            tempgpu = float(fgpu.read()) / 1000.0
        with open('/sys/class/thermal/thermal_zone6/temp', 'r') as fnpu:
            tempnpu = float(fnpu.read()) / 1000.0

        if resmon_style == 'simple':

         formatted_output = (
             f"RAM Used: {ram_usage:3.2f}% (Free: {ram_avail:2.2f} Gb) - "
             f"Disk Used: {disk_usage:3.2f}% (Free: {disk_free:4.2f} Gb) - "
             f"CPU/NPU Temp: {tempcpu:3.1f}/{tempnpu:3.1f} °C - "
             f"CPU/NPU Usage: {cpu_usage:3.2f}/{npu_usage:3.2f} %"
         )

        else:
         formatted_output = (
             f"RAM Used: {ram_usage:3.2f}% ( Total/Used/Avail: [ {ram_total:2.2f} | {ram_used:2.2f} | {ram_avail:2.2f} ] Gb )  -  "
             f"Disk Used: {disk_usage:3.2f}% ( Total/Used/Free: [ {disk_tot:4.2f} | {disk_used:4.2f} | {disk_free:4.2f} ] Gb )  -  "
             f"Load Avg. 1/5/15min: [ {round(load_avg[0], 2):3.2f} | {round(load_avg[1], 2):3.2f} | {round(load_avg[2], 2):3.2f} ] %\n"
             f"Network Sent/Received: [ {sent_mb:4.2f} | {recv_mb:4.2f} ] Mb  -  "
             f"CPU/GPU/NPU Temperature: [ {tempcpu:3.1f} | {tempgpu:3.1f} | {tempnpu:3.1f} ] °C  -  "
             f"CPU/NPU Usage: [ {cpu_usage:3.2f} | {npu_usage:3.2f} ] % "
             f"( Sys/User/Idle: [ {cpu_sys:3.2f} | {cpu_usr:3.2f} | {cpu_idl:3.2f} ] % )"
          )

        return str(formatted_output)



    def unload_model():
        global rkllm_model
        if rkllm_model is not None:
           print("=========UNLOADING MODEL================================================================")
           print("Unloading Model, releasing resources...")
           rkllm_model.release()
           rkllm_model = None
           print("=====================================================================================")
           statusBox_content = "The Model has been successfully unloaded!\nIf you want to reload the same model, press the button 'Reload the model with the parameters above'\nIf you want to load a different model, select it from the dropdown."
        else:
           statusBox_content = "No Model loaded."
        return statusBox_content  # Keep the dropdown value and update status box

 
    # Helper function to define initializing model before class is declared
    def initialize_model(model, max_tokens, temperature, freq_penalty, rep_penalty, pres_penalty, max_conlen, top_k, top_p, sys_prompt):
        global rkllm_model
        try:
            if rkllm_model is not None:
                rkllm_model.release()
        except AttributeError:
         print("No model loaded! Continuing with initialization...")
        model_init = ""
        model_lower = model.lower()
        if model_lower.startswith("gemma"):
            sys_prompt = ""
            model_init = "System Prompt was emptied. Gemma models do not support it.\n"
            print("Model Gemma was selected. Emptying system prompt\n")
        print()
        init_msg = "=========INITIALIZING=================================================================="
        print(init_msg)
        sys.stdout.flush()
        rkllm_model = RKLLMLoaderClass(model=model, maxnewtok=max_tokens, temp=temperature, freqpen=freq_penalty, reppen=rep_penalty, prespen=pres_penalty, maxconlen=max_conlen, topk=top_k, topp=top_p, system_prompt=sys_prompt )
        model_init += f"RKLLM Model: {rkllm_model.model_name} has been initialized successfully!\n"
     # add instructions to enable or disable model thinking for Qwen-3 models
        if model_lower.startswith("qwen3") or model_lower.startswith("qwen-3"):
            model_init += "To enable or disable the model thinking, set /think or /no_think in the System Prompt and reload the model.\n"
        model_init += "In case of errors, the container will restart automatically. Wait some seconds and reload this page to start again."
       # print(model_init)
        complete_init = "====================================================================================="
        print(complete_init)
        print()
        output = model_init
        sys.stdout.flush()
        #return output
        return rkllm_model.rkllm_param.max_new_tokens, rkllm_model.rkllm_param.temperature, rkllm_model.rkllm_param.frequency_penalty, rkllm_model.rkllm_param.repeat_penalty, rkllm_model.rkllm_param.presence_penalty, rkllm_model.rkllm_param.max_context_len, rkllm_model.rkllm_param.top_k, rkllm_model.rkllm_param.top_p, rkllm_model.system_prompt,  output


    # Helper function to stream LLM output into the chat box
    def get_RKLLM_output(message, history):
        try:
            for chunk in rkllm_model.get_RKLLM_output(message, history):
                yield chunk
        except RuntimeError as e:
            print(f"ERROR: {e}")

    def countTokens(text):
        """
        Use tiktoken to count the number of tokens
        text -> str input
        Return -> int number of tokens counted
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(text))
        return num_tokens

    # Reset the individual statistics variables and clear chatbot history
    def reset_statistics(chatbot):
        prompttokens = ''
        assistanttokens = ''
        totaltokens = ''
        totalseconds = ''
        overallSpeed = ''
        genspeed = ''
        evalSpeed = ''
        gr_ttft_seconds = ''
        gr_tokens = ''
        chatbot.clear()
        return chatbot, '\n', '0 seconds', '0 t/s', '\n\n\n'
        print("Statistics have been reset.")

    def writehistory(filename, text):
        """
        Save a string into a logfile with Python file operations
        filename -> str pathfile/filename
        text -> str, the text to be written in the file
        """
        with open(f'{filename}', 'a', encoding='utf-8') as f:
            f.write(text)
            f.write('\n')

    def genRANstring(n):
        """
        n = int number of char to randomize
        Return -> str, the filename with n random alphanumeric characters
        """
        N = n
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        print(f'Logfile_{res}.txt  CREATED')
        return f'Logfile_{res}.txt'

  #Theme definition
    theme = gr.themes.Ocean(
        primary_hue="blue",
        secondary_hue="blue",
        neutral_hue="zinc",
        text_size="md",
        spacing_size="sm",
        font=[gr.themes.GoogleFont("Oxanium"), "Arial", "sans-serif"]
    ).set(
        prose_text_size='*text_md',
        input_text_size='*text_md',
        button_large_text_size='*text_md',
        button_small_text_weight='200',
        button_medium_text_weight='400',
        button_large_text_weight='600',
        block_background_fill='*neutral_100',
        block_info_text_color='*neutral_950',
        block_title_background_fill='*neutral_200',
        block_title_background_fill_dark='*neutral_950',
        block_title_border_width='0',
        block_title_text_color='*neutral_900',
        block_title_text_color_dark='*neutral_50',
        block_padding='*spacing_lg',
        block_title_padding='*spacing_lg',
        block_title_radius='*radius_md',
        chatbot_text_size='*text_md',
        layout_gap='*spacing_md',
        checkbox_label_gap='*spacing_sm'
         )

 # INTERFACE
    # Create a Gradio interface

    with gr.Blocks(fill_width=True, fill_height=True, theme=theme, title="AI Chatbot") as chatRKLLM:

        writehistory(LOGFILENAME, f'{datetime.datetime.now()}>> using model changeme\n================================================================================\n\n')

        with gr.Row(): #height=35, variant='default'):
            gr.Markdown(
                f"""### Advanced AI ChatBot Interface based on Gradio and Rkllm. Inference accelerated by Rockchip RK3588 NPU """)

            #Displays the system resources
            sys_mon = gr.Textbox(value=resmon, every=resmon_frequency, lines=1, label="System Resources", container=False, show_label=False, scale=resmon_panel_scale, interactive=False)

        with gr.Row(): #, variant='panel'):
            available_models = available_models()
            model_dropdown = gr.Dropdown(choices=available_models, label="Select the Model to load", value="", allow_custom_value="True")
            statusBox = gr.Textbox(lines=3, container=False, show_label=False)

        with gr.Row():
            # HYPERPARAMETERS
            with gr.Column(scale=1):
                max_conlen = gr.Slider(minimum=1024, maximum=16384, value=0, step=1, label="Max Context Lenght")
                max_tokens = gr.Slider(minimum=1024, maximum=16384, value=0, step=1, label="Max New Tokens")
                temperature = gr.Slider(minimum=0.0, maximum=2.0, value=0.0, step=0.1, label="Temperature")
                freq_penalty = gr.Slider(minimum=0.0, maximum=2.0, value=0.0, step=0.1, label="Frequency Penalty")
                rep_penalty = gr.Slider(minimum=0.00, maximum=2.00, value=0.00, step=0.01, label="Repetition Penalty")
                pres_penalty = gr.Slider(minimum=-1.0, maximum=1.0, value=-1.0, step=0.1, label="Presence Penalty")
                top_k = gr.Slider(minimum=1, maximum=100, value=0, step=1, label="Top-k Sampling")
                top_p = gr.Slider(minimum=0.00, maximum=1.00, value=0.00, step=0.01, label="Top-p (Nucleus) Sampling")
                sys_prompt = gr.Textbox(lines=2, label="System Prompt", container=True, show_label=True) 
                rldbtn = gr.Button("Reload the Model with the parameters above", variant="primary", interactive=False)

                unload_button = gr.Button("Unload Model", variant="primary", interactive=False)
                unload_button.click(fn=unload_model, outputs=[statusBox]).then(fn=lambda: gr.update(interactive=False), inputs=None, outputs=unload_button)

                rldbtn.click(fn=initialize_model, inputs=[model_dropdown, max_tokens, temperature, freq_penalty, rep_penalty, pres_penalty, max_conlen, top_k, top_p, sys_prompt], outputs=[max_tokens, temperature, freq_penalty, rep_penalty, pres_penalty, max_conlen, top_k, top_p, sys_prompt, statusBox]).then(fn=lambda: gr.update(interactive=True), inputs=None, outputs=unload_button).then(fn=lambda: gr.update(interactive=True), inputs=None, outputs=rldbtn)

                model_dropdown.change(fn=initialize_model, inputs=model_dropdown, outputs=[max_tokens, temperature, freq_penalty, rep_penalty, pres_penalty, max_conlen, top_k, top_p, sys_prompt, statusBox]).then(fn=lambda: gr.update(interactive=True), inputs=None, outputs=unload_button).then(fn=lambda: gr.update(interactive=True), inputs=None, outputs=rldbtn)


            # CHATBOT AREA
            with gr.Column(scale=3):
              with gr.Tabs():
               with gr.TabItem("Streaming Chat (seamless, no statistics)"):
                txt2txt = gr.ChatInterface(fn=get_RKLLM_output, type="messages", stop_btn=False, save_history=True, fill_width=True, fill_height=True)
                txt2txt.chatbot.height = "60vh"
                txt2txt.chatbot.resizable = True
                txt2txt.saved_conversations.secret = "alefrisrkllmgradiochatbot060125"
                txt2txt.saved_conversations.storage_key = "_saved_conversations"

               with gr.TabItem("Chat with Statistics (no streaming)"):
                 with gr.Row():
                   with gr.Column(scale=1):
                    # KPIs
                     ttft_seconds = gr.Text(label='Time to First Token', value='\n', container=True, show_label=True)
                     inference_time = gr.Text(label='Inference Time', value='0 seconds', container=True, show_label=True)
                     speed = gr.Text(label='Generation Speed', value='0 t/s', container=True, show_label=True)
                     tokens_stats = gr.Text(label='Tokens Statistics', value='\n\n\n', container=True, show_label=True)
                     log_filename = gr.Text(label='Log Filename', value=LOGFILENAME, container=True, show_label=True)

                     tokens_stats.value = "N/A"
                     ttft_seconds.value = "N/A"
                     speed.value = "N/A"
                     inference_time.value = "N/A"

                     #Create the reset button
                     reset_button = gr.Button("Reset Statistics and clear Chat", variant="primary")

                   with gr.Column(scale=4):
                     chatbot = gr.Chatbot(type="messages", show_copy_button=True, avatar_images=['user.png', 'bot.png'], layout='bubble', resizable=True, height="60vh")
                     msg = gr.Textbox(lines=1, placeholder="Type your message here...", container=False, show_label=False)
                     clear = gr.ClearButton([msg, chatbot])

                     #define the reset button click to Reset the individual statistics variables and clear chatbot history
                     reset_button.click(fn=reset_statistics, inputs=[chatbot], outputs=[chatbot, ttft_seconds, inference_time, speed, tokens_stats])

               def chat(message, history, temperature, freq_penalty, rep_penalty, pres_penalty, max_tokens, max_conlen, top_k, top_p, sys_prompt):
                    """
                    Get as an input the chatbot gradio type and the conversation history with hyperparameters
                    message -> str coming from the gradio textbox
                    history -> list, following the chat template format
                    temperature -> float, the temperature setting coming from a gradio slider
                    freq_penalty -> float, the frequency_penalty setting coming from a gradio slider
                    rep_penalty -> float, the repetition_penalty setting coming from a gradio slider
                    pres_penalty -> float, the presence_penalty setting coming from a gradio slider
                    max_tokens -> int, the max_tokens setting coming from a gradio slider
                    max_conlen -> int, the max_context_len setting coming from a gradio slider
                    top_k -> int, the top_k setting coming from a gradio slider
                    top_p -> float, the top_p setting coming from a gradio slider
                    Return ->   history - list, following the chat template format
                    clear_prompt - str, empty string to reset the user text input widget
                    gr_ttft_seconds - str, text with Time to First Token in seconds
                    gr_inference_time - str, text with total Inference time in seconds
                    gr_speed - str, text with generation speed in tokens/seconds
                    gr_tokens - str, text with number of tokens breakdown
                    """
                    firstToken = 0
                    history.append({"role": "user", "content": message})
                    entire_prompt = ''
                    for items in history:
                        entire_prompt += items['content']
                        #entire_prompt = ''.join(item['content'] for item in history)
                    prompttokens = countTokens(entire_prompt)
                    messagetokens = countTokens(message)
                    start = datetime.datetime.now()
                    stream = rkllm_model.get_RKLLM_output(message, history)
                    clear_prompt = ''
                    assistant_content = ""
                    for chunk in stream:
                        #print(chunk)  # Inspect the structure of chunk in output - for debug
                        if 'content' in chunk:
                            content = chunk['content']
                            if firstToken == 0:
                                ttft_time = datetime.datetime.now() - start
                                genStartTime = datetime.datetime.now()
                                ttft_seconds = ttft_time.total_seconds()
                                gr_ttft_seconds = f'\n'
                                history.append({"role": "assistant", "content": content})  # Append a new entry for the assistant
                                firstToken = 1
                            else:
                                history[-1]['content'] += "\t\t\n" #I add a custom set of tab and newlines before each new content so I can then split the lines afterwards
                                history[-1]['content'] += content # Continue appending to the last assistant entry

                            #only get the last line of the content. That is the line which will be displayed in the chatbot
                            last_content = history[-1]['content']
                            last_line = last_content.split("\t\t\n")[-1] if last_content else ""
                            history[-1]['content'] = last_line

                            assistanttokens = countTokens(history[-1]['content'])
                            TdeltaGeneration = (datetime.datetime.now() - genStartTime)
                            deltaGeneration = TdeltaGeneration.total_seconds()
                            Ttotalseconds = (datetime.datetime.now() - start)
                            totalseconds = Ttotalseconds.total_seconds()
                            assistanttokens = countTokens(history[-1]['content'])
                            totaltokens = prompttokens + assistanttokens
                            overallSpeed = totaltokens / totalseconds
                            evalSpeed = prompttokens / ttft_seconds
                            gr_ttft_seconds = f'Time to First Token: {ttft_seconds:.1f} seconds\nPrompt Eval: {evalSpeed:.2f}  t/s in {ttft_seconds:.1f} seconds'
                            try:
                                genspeed = assistanttokens / deltaGeneration
                            except ZeroDivisionError:
                                genspeed = 0
                            gr_InferenceTime = f'{totalseconds} seconds'  # INFTIME
                            gr_genspeed = f'{genspeed:.2f}  t/s'  # SPEED
                            gr_tokens = f'Prompt Tokens: {messagetokens}\nChat History Tokens: {prompttokens}\nOutput Tokens: {assistanttokens}\nTOTAL Tokens: {totaltokens}'



                    yield history, clear_prompt, gr_ttft_seconds, gr_InferenceTime, gr_genspeed, gr_tokens


                    stats = f'''---
Prompt Tokens: {prompttokens}
Output Tokens: {assistanttokens}
TOTAL Tokens: {totaltokens}
>>> Inference time:   {totalseconds} seconds
>>> Inference speed:  {overallSpeed:.2f}  t/s
>>> Generation speed: {genspeed:.2f}  t/s
>>> Prompt EVAL speed: {evalSpeed:.2f}  t/s
>>> {gr_ttft_seconds}
{gr_tokens}
---
'''
                    # Save in the log file prompt and reply
                    tosave = f'{datetime.datetime.now()}\nUSER > {message}\n BOT > {history[-1]["content"]}\n{stats}\n\n'
                    writehistory(LOGFILENAME, tosave)

               clear.click(lambda: ([], ""), None, [chatbot, msg])
               msg.submit(chat, [msg, chatbot, temperature, freq_penalty, rep_penalty, pres_penalty, max_tokens, max_conlen, top_k, top_p, sys_prompt], [chatbot, msg, ttft_seconds, inference_time, speed, tokens_stats])

    chatRKLLM.queue()
    chatRKLLM.launch()

    print("=====================================================================================")
    print("Closing down, releasing RKLLM model resources...")
    if rkllm_model is not None:
        rkllm_model.release()
    print("=====================================================================================")

import subprocess
import traceback
from io import StringIO
from contextlib import redirect_stdout

import gradio as gr
from modules import script_callbacks, shared
from modules.ui_components import ResizeHandleRow

def execute_shell_command(command):
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)
    
    return output
    
def create_shell_tab(lines):
    with gr.Tab("Shell", elem_id="qic-shell-tab"):
        with gr.Row(), ResizeHandleRow(equal_height=False):
            with gr.Column(scale=1):
                inp = gr.Textbox(value="", label="Shell command", lines=lines, elem_id="qic-shell-input", elem_classes="qic-console")
                btn = gr.Button("Run", variant='primary', elem_id="qic-shell-submit")
            
            with gr.Column(scale=1):
                out = gr.Code(value="# Output will appear here\n\n# Tip: Press `ctrl+space` to execute the current command", language="shell", label="Output", lines=lines, interactive=False, elem_id="qic-shell-output", elem_classes="qic-console")
        
        btn.click(fn=execute_shell_command, inputs=inp, outputs=out)

def on_ui_tabs():
    with gr.Blocks(elem_id="qic-root", analytics_enabled=False) as ui_component:
        create_shell_tab(shared.opts.qic_default_num_lines)

        return [(ui_component, "QIC Console", "qic-console")] 


def on_ui_settings():
    settings_section = ('qic-console', "QIC Console")
    options = {
        "qic_default_num_lines": shared.OptionInfo(30, "Default number of console lines", gr.Number, {"precision": 0}).needs_reload_ui(),
        "qic_hide_warning": shared.OptionInfo(False, "Hide warning message", gr.Checkbox).needs_reload_ui(),
    }

    for name, opt in options.items():
        opt.section = settings_section
        shared.opts.add_option(name, opt)


script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_ui_settings(on_ui_settings)

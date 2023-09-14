from modules import script_callbacks, shared
from pathlib import Path
import gradio as gr
import subprocess
import hashlib
import shlex
import os

extension_root = Path(__file__).resolve().parents[1]
check_command_path = extension_root.joinpath('.check_command')
custom_command = ''


class OptionMarkdown(shared.OptionInfo):
    def __init__(self, text):
        super().__init__(str(text).strip(), label='', component=lambda **kwargs: gr.Markdown(**kwargs))
        self.do_not_save = True


class CustomAutoLaunch(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def confirm_permission():
    if shared.cmd_opts.disable_extension_access:
        raise CustomAutoLaunch('[Permission Denied]: Custom autolaunch command is in Read-only mode')
    else:
        command_hash = hashlib.sha256(shared.opts.custom_autolaunch_command.encode("utf8")).hexdigest()
        with open(check_command_path, 'w', encoding='utf-8') as file:
            file.write(f'{command_hash}{shared.opts.custom_autolaunch_command}')


def validate_command_integrity():
    global custom_command
    try:
        with open(check_command_path, 'r', encoding='utf-8') as file:
            read_check = file.read()
        if read_check[:64] == hashlib.sha256(read_check[64:].encode("utf8")).hexdigest() and read_check[64:] == shared.opts.custom_autolaunch_command:
            custom_command = read_check[64:]
            return True
    except Exception as e:
        raise CustomAutoLaunch(f'{e}\n[Warning]: custom autolaunch command validation failed due to above reason\nskip executing custom command.')


OptionInfo_command = (shared.OptionInfo(None,
                                        label='Custom autolaunch command',
                                        component=gr.Textbox,
                                        restrict_api=True,
                                        component_args={'interactive': not shared.cmd_opts.disable_extension_access},
                                        onchange=confirm_permission,
                                        ))


if shared.cmd_opts.disable_extension_access:
    OptionInfo_command.do_not_save = True
    OptionInfo_command.info('Read-only')


with open(extension_root.joinpath('explanation.md'), 'r') as f:
    option_explanation_md = OptionMarkdown(f.read())

shared.options_templates.update(shared.options_section(('system', 'System'), {
        "custom_autolaunch_command_explanation": option_explanation_md,
        "custom_autolaunch_enable": shared.OptionInfo(False, 'Enable custom autolaunch'),
        "custom_autolaunch_command": OptionInfo_command,
    }))


def run_custom_launch_command(demo, _app, *_args, **_kwargs):
    try:
        if custom_command:
            command = shlex.split(custom_command.format(url=demo.local_url))
            subprocess.Popen(command)
    except Exception as e:
        print(f'{e}\n[ERROR]: Failed custom autolaunch: with command {shared.opts.custom_autolaunch_command}')


def check_autolaunch(*_args, **_kwargs):
    if shared.opts.custom_autolaunch_enable and shared.opts.custom_autolaunch_command:
        auto_launch = False
        env_sd_webui_restarting = os.getenv('SD_WEBUI_RESTARTING') or os.getenv('SD_WEBUI_RESTARTING ')
        if env_sd_webui_restarting != '1':
            if hasattr(shared.opts, 'auto_launch_browser'):  # webui >= 1.6.0
                if shared.opts.auto_launch_browser == "Remote" or shared.cmd_opts.autolaunch:
                    auto_launch = True
                elif shared.opts.auto_launch_browser == "Local":
                    if hasattr(shared.cmd_opts, 'webui_is_non_local'):  # webui > 1.6.0
                        if not shared.cmd_opts.webui_is_non_local:
                            auto_launch = True
                    elif not any([shared.cmd_opts.share, shared.cmd_opts.listen, shared.cmd_opts.ngrok, shared.cmd_opts.server_name]):  # webui = 1.6.0
                        auto_launch = True
        elif shared.cmd_opts.autolaunch:  # webui < 1.6.0
            auto_launch = True

        if auto_launch and validate_command_integrity():
            os.environ.setdefault('SD_WEBUI_RESTARTING', '1')
            os.environ.setdefault('SD_WEBUI_RESTARTING ', '1')
            script_callbacks.on_app_started(run_custom_launch_command)


script_callbacks.on_before_ui(check_autolaunch)

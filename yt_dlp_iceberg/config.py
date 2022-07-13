from strictyaml import load, Map, Str, Int, Seq, YAMLError, Bool, MapPattern, Optional
from pathlib import Path
import os

config_file_name = 'config.yaml' if os.path.exists('config.yaml') else os.environ.get('CONFIG', None)
if not (config_file_name and os.path.exists(config_file_name)):
    raise FileNotFoundError(
        f"CWD {os.path.abspath(os.path.curdir)} must either contain config.yaml or the environment variable CONFIG must point to an config file.")

schema = Map({
    Optional("base_folder"): Str(),
    Optional("ytdlp_exec"): Str(),
    Optional("update"): Bool(),
    Optional("presets"): MapPattern(Str(), Map({
        Optional("interval_minutes"): Int(),
        Optional("post_command"): Str(),
        Optional("options"): Seq(Str()),
    })),
    "projects": MapPattern(Str(), Map({
        "target": Str(),
        Optional("interval_minutes"): Int(),
        Optional("folder"): Str(),
        Optional("post_command"): Str(),
        Optional("preset"): Str(),
        Optional("options"): Seq(Str()),
    }))})


def get_parsed_data():
    return load(Path(config_file_name).read_text('utf-8'), schema).data

import argparse
import os
import pathlib
import time
from subprocess import Popen

from yt_dlp_iceberg.config import get_parsed_data
from yt_dlp_iceberg.preset import Preset
from yt_dlp_iceberg.project import Project

parser = argparse.ArgumentParser(description='Continuously archive the internet.')
parser.add_argument('--continuous', action=argparse.BooleanOptionalAction, default=False,
                    help='Performs an archival check every minute, sleeping for 60 seconds after each check.')
parser.add_argument('--once', action=argparse.BooleanOptionalAction, default=False,
                    help='Performs an archival check immediately.')
parser.add_argument('--force', action=argparse.BooleanOptionalAction, default=False,
                    help='Performs an archival immediately regardless of project intervals.')

args = parser.parse_args()


def perform():
    parsed_data = get_parsed_data()
    if parsed_data.get('base_folder', None):
        if not pathlib.Path(parsed_data["base_folder"]).is_dir():
            raise FileNotFoundError(
                f"base_folder provided ({parsed_data['base_folder']}) must exist and be a folder.")
        os.chdir(parsed_data["base_folder"])

    if parsed_data.get('update'):
        os.system(f"{parsed_data.get('ytdlp_exec', 'yt-dlp')} -U")

    for name in parsed_data["projects"]:
        _project = parsed_data["projects"][name]
        if not _project.get('folder'):
            _project["folder"] = name

        # replace preset in-place with a Preset object
        if _project.get('preset'):
            if str(_project.get('preset')) not in parsed_data['presets'].keys():
                print(f"Preset {_project['preset']} is not a defined preset!")
            print("Using preset:", _project['preset'])
            _project['preset'] = Preset(**(parsed_data['presets'][_project['preset']]))
        project = Project(**_project)
        if not pathlib.Path(project.folder).is_dir():
            os.mkdir(project.folder)
        os.chdir(project.folder)

        if project.need_update() or args.force:
            print(name + (": forced to run" if args.force else ": needs to run"))
            project.update_interval_file()
            project.run_ytdlp(parsed_data["ytdlp_exec"] if parsed_data.get('ytdlp_exec') else None)
            print(name + ": ran")
        else:
            print(name + ": does not need to run")
        if _project.get('post_command'):
            print(name + ": running Popen for post_command")
            Popen(project.post_command.replace("ABS_FOLDER", os.getcwd()))
        os.chdir('..')


def run():
    if args.once or args.force:
        perform()
    if args.continuous:
        while True:
            perform()
            print("Performed, sleeping 60s")
            time.sleep(60)


if __name__ == '__main__':
    run()

import argparse
import os
import pathlib
import time
from subprocess import Popen

from yt_dlp_iceberg.config import parsed_data
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
    if parsed_data.get('base_folder', None):
        if not pathlib.Path(parsed_data["base_folder"]).is_dir():
            raise FileNotFoundError(
                f"base_folder provided ({parsed_data['base_folder']}) must exist and be a folder.")
        os.chdir(parsed_data["base_folder"])
    for name in parsed_data["projects"]:
        _project = parsed_data["projects"][name]
        if not _project.get('folder'):
            _project["folder"] = name
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
            Popen(project.post_command)
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

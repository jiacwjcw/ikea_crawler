import os

from dynaconf import Dynaconf

SETTINGS = Dynaconf(
    root_path=str(os.path.realpath(__file__)).split("__init__.py")[0],
    envvar_prefix="DYNACONF",
    settings_files=[
        "settings.yaml",
        ".secrets.yaml",
        "projects.yaml",
    ],
    environment=True,
    env_switcher="ENV",
)

ROOT_DIR = str(os.path.realpath(__file__)).split("configs")[0].replace("\\", "/")
REPORT_DIR = os.path.join(ROOT_DIR, "reports")
LOG_DIR = os.path.join(ROOT_DIR, "logs")

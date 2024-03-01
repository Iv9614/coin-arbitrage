import os
import subprocess
from ast import literal_eval
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

_configs: dict[str, Any] = {
    "DEBUG": False,
    "GITLAB_API_VERSION": "v4",
    "REDIS_BASE_URL": "devops-redis-service:6379",
    "TIMEZONE": "Asia/Taipei",
}

# Define the base folder of the project
BASE_FOLDER: Path = Path(__file__).parent.parent
LOG_FOLDER: Path = BASE_FOLDER / "logs"

TEMP_REMOTE_DEPLOY_FOLDER: Path = BASE_FOLDER / "temp"


# Kubernetes default variables
K8S_NAMESPACE_ORIGINAL: str = "default"
K8S_NAMESPACE_DEFAULT: str = "iiidevops"
K8S_NAMESPACE_SYSTEM_SECRET: str = "iiidevops-env-secret"
K8S_CLUSTER_RUNNER: str = "runner"
K8S_CLUSTER_SYSTEM: str = "system"
K8S_CLUSTERS: list[str] = [K8S_CLUSTER_RUNNER, K8S_CLUSTER_SYSTEM]

# Gitlab default variables
DEFAULT_REPO_GROUP = "iiidevops"


def __create_folders() -> None:
    # Create default directories
    for folder in [LOG_FOLDER, TEMP_REMOTE_DEPLOY_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def __load() -> None:
    """
    Load the environment variables from the .env file or os environment variables.

    Returns:
        None
    """
    env_folder: Path = BASE_FOLDER / "env"
    if os.path.exists(env_folder):
        env_file: Path = env_folder / f"{__get_branch_name()}.env"

        if os.path.isfile(env_file):
            load_dotenv(env_file)

    __create_folders()


def __get_branch_name() -> str:
    """
    Get the current branch name, if not found, return "default".

    Returns:
        str: The current branch name
    """
    command: list[str] = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    process: subprocess.Popen = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, _ = process.communicate()
    branch_name: str = output.decode().strip()

    if not branch_name:
        branch_name = "default"

    return branch_name


def __convert_bool(value: str) -> bool:
    """
    Convert the string value to boolean value

    Args:
        value: The string value

    Returns:
        bool: The boolean value
    """
    if value.lower() in ["true", "t", "1", "yes", "y", "on"]:
        return True

    elif value.lower() in ["false", "f", "0", "no", "n", "off"]:
        return False

    else:
        raise ValueError(f"Cannot convert {value} to boolean value.")


def __auto_convert(env: Any) -> Any:
    if isinstance(env, str):
        try:
            env = __convert_bool(env)

        except ValueError:
            try:
                # Auto guess type, only support int, float, list, dict
                env = literal_eval(env)

            except (ValueError, SyntaxError):
                pass
    elif env is None:
        env = None
    else:
        raise ValueError(f"Cannot convert {env}, should be a string.")

    return env


def get(key: str, default: Any = None, convert: bool = False) -> Any:
    """
    Get the value of the key from the config file, if not found, return the default value

    Args:
        key: The key of the config
        default: The default value if the key is not found
        convert: If the value should be converted to the correct type, otherwise, return the string type value

    Returns:
        Any: The value of the key
    """
    env: Any = os.getenv(key)

    if convert:
        env = __auto_convert(env)

    if env is not None:
        return env

    if key in _configs and _configs[key] is not None:
        return _configs[key]

    else:
        return default


# Indirectly call the __load function
__load()

import os
from enum import StrEnum
from pathlib import Path
from dotenv import load_dotenv


class Enviroment(StrEnum):
    """
    Application enviromnts types.

    Defines the possible enviroments the application can run in:
    development, staging, test, prodcution

    Attributes:
        DEVELOPMENT (str): the development enviroment.
        STAGING (str): the staging enviroment.
        TEST (str): the test enviroment.
        PRODUCTION (str): the production enviroment.
    """

    DEVELOPMENT = "development"
    STAGING = "staging"
    TEST = "test"
    PRODUCTION = "production"

def get_enviroment() -> Enviroment:
    """ 
    Get the current enviroment.

    Must be set via export APP_ENV=development|statging|test|production.
    it will be used to load the appropiate .env file only.

    Returns:
        Enviroment: the current enviroment (devlopment, staging, test, prodution)
    """

    match os.getenv("APP_ENV", "development").lower():
        case "production" | "prod":
            return Enviroment.PRODUCTION
        case "staging" | "stage":
            return Enviroment.STAGING
        case "testing" | "test":
            return Enviroment.TEST
        case _:
            return Enviroment.DEVELOPMENT

def load_env_file():
    """
    Load enviroment-specific .env file.

    Returns:
    str | path | None: The path to the loaded .env file, or None if no file was found.
    """
    env = get_enviroment()
    print(f"loading enviroment: {env}")
    base_dir = Path(__file__).parents[2]

    # Load enviroment variable with priority order
    env_files = [Path(base_dir, f".env.{env.value}"), Path(base_dir, ".env")]

    # load the first env file exist
    for env_file in env_files:
        if env_file.is_file():
            load_dotenv(env_file, override= True)
            print(f"Loaded enviroment from: {env_file}")
            return env_file

    # Fallback to default if no env file is found
    return None

print(get_enviroment())


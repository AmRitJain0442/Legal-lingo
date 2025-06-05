import os
from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(Exception):
    pass


class Settings:
    def __init__(self):
        self.app_name: str = os.getenv("APP_NAME", "Legal Lingo API")
        self.app_version: str = os.getenv("APP_VERSION", "1.0.0")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

        self.postgres_user: str = os.getenv("POSTGRES_USER")
        self.postgres_password: str = os.getenv("POSTGRES_PASSWORD")
        self.postgres_host: str = os.getenv("POSTGRES_HOST")
        self.postgres_port: str = os.getenv("POSTGRES_PORT")
        self.postgres_db: str = os.getenv("POSTGRES_DB")

        self.api_prefix: str = os.getenv("API_PREFIX", "/api")

        self.sql_echo: bool = os.getenv("SQL_ECHO", "false").lower() == "true"

        self._validate_config()

    def _validate_config(self) -> None:
        missing_vars = []

        required_db_vars = {
            "POSTGRES_USER": self.postgres_user,
            "POSTGRES_PASSWORD": self.postgres_password,
            "POSTGRES_HOST": self.postgres_host,
            "POSTGRES_PORT": self.postgres_port,
            "POSTGRES_DB": self.postgres_db,
        }

        for var_name, var_value in required_db_vars.items():
            if not var_value:
                missing_vars.append(var_name)

        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        try:
            int(self.postgres_port)
        except ValueError:
            raise ConfigurationError(
                f"POSTGRES_PORT must be a valid number, got: {self.postgres_port}"
            )

    def validate_database_config(self) -> bool:
        try:
            self._validate_config()
            return True
        except ConfigurationError:
            return False

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


try:
    settings = Settings()
except ConfigurationError as e:
    print(f"Configuration Error: {e}")
    print("Please check your environment variables and try again.")
    settings = None

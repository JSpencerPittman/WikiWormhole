import yaml
import sys
import os


def generate_config(location: str):
    config = {
        "PERSONAL_WEBSITE": "https://github.com/<PERSONAL_ACCOUNT_HERE>",
        "EMAIL_ADDRESS": "example@email.com"
    }

    filepath = os.path.join(location, "config2.yaml")
    with open(filepath, "w") as file:
        yaml.dump(config, file)


if __name__ == "__main__":
    generate_config(sys.argv[1])

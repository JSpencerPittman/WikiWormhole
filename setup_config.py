import yaml


def generate_config():
    config_data = {
        "PERSONAL_WEBSITE": "https://github.com/PERSONALWEBSITE",
        "EMAIL_ADDRESS": "example@email.com"
    }

    with open('config.yaml', 'w') as file:
        yaml.dump(config_data, file)


if __name__ == "__main__":
    generate_config()

from importlib.resources import files


def get_default_data(site_name: str) -> str:
    return files(f"zyte_test_websites.{site_name}").joinpath("data.json").read_text()

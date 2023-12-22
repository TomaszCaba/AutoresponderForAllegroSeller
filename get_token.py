from main import get_access_token, save_token_to_file


def main():
    response = get_access_token()
    save_token_to_file(response)


if __name__ == "__main__":
    main()

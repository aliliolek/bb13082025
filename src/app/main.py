from pprint import pprint
from api_client import get_api

api = get_api()

def main() -> None:
  print(api.get_account_information())
  print(api.get_current_balance(accountType="FUND"))



if __name__ == "__main__":
    main()

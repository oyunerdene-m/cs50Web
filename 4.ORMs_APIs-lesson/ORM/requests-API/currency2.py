import requests


def main():
  base = input("Base currency: ")
  other = input("Other currency: ")

  #"http://data.fixer.io/api/latest?access_key=apikey&base=EUR&symbols=USD"
  res = requests.get("http://data.fixer.io/api/latest", params={"access_key": "6ecf162da9b29cd2507bb70fb5fd6295", "base": base, "symbols": other})
  if res.status_code != 200:
    raise Exception("ERROR: API request unsuccessful.")
  data = res.json()

  rates = data["rates"][other]
  print(f"1 {base} equals to {rates} {other}.")
  
if __name__ == "__main__":
  main()
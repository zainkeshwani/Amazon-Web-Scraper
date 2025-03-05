from bs4 import BeautifulSoup
import requests
import pandas as pd

# Take user input for the item to search
item = input("Enter the item you want to search for on Amazon: ")
max_price = int(input("Enter the maximum price you are willing to pay: "))
num_res = int(input("Enter the number of results you want to see: "))

# Create the search URL using the user input
url = f"https://www.amazon.com/s?k={item.replace(' ', '+')}&ref=nb_sb_noss_2"
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

# Send the GET request to Amazon
webpage = requests.get(url, headers=headers)

# If status code isn't 200, print an error and stop
if webpage.status_code != 200:
  print(f"Error fetching page, status code: {webpage.status_code}")
else:
  soup = BeautifulSoup(webpage.content, "html.parser")

  # Find all product links (adjust the class name as needed)
  links = soup.find_all("a", attrs={"class": "a-link-normal"})

  names = soup.find_all(
      "h2",
      attrs={
          "class": "a-size-medium a-spacing-none a-color-base a-text-normal"
      })

  # Find the price for each product
  prices = soup.find_all("span", attrs={"class": "a-price-whole"})

  # If no links or prices are found, print a message
  if not links or not prices:
    print("No product links or prices found.")
  else:
    # Collect the specified number of product links and prices
    product_info = []
    if num_res > len(prices):
      num_res = len(prices)

    for name, price in zip(names[:num_res], prices[:num_res]):
      product_name = name.get_text(strip=True)
      # Clean the price string
      product_price_str = price.get_text().strip()

      # Check if the price string is valid and convert to integer
      if product_price_str:
        # Remove any commas or other non-numeric characters
        product_price_str = ''.join(filter(str.isdigit, product_price_str))

        if product_price_str:  # Ensure it's not empty
          product_price = int(product_price_str)  # Convert to integer
        else:
          continue  # Skip if the price is invalid

        if product_price > max_price:
          continue

        product_info.append((product_name, product_price))

    # Print the collected product names and prices
    print("\nTop products within your price range:")
    for idx, (product_name, product_price) in enumerate(product_info, 1):
      print(f"{idx}. {product_name} - Price: ${product_price}")
      print()
    want_links = input("Do you want to see the links for the items? (y/n): ")
    if(want_links == "y"):
      for idx, (product_name, product_price) in enumerate(product_info, 1):
        print(f"{idx}. {product_name} - Price: ${product_price}")
        print(f"Link: {links[idx-1]['href']}")
        print()

from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv 
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# Fetch the page content
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", 
    "Accept-Language": "en-US",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
})

web_product = response.text 
soup = BeautifulSoup(web_product, 'html.parser')

title = soup.find(name="span", id="productTitle").getText(strip=True)
price_whole = soup.find(name="span", class_="a-price-whole")
price_fraction = soup.find(name="span", class_="a-price-fraction")

if price_whole and price_fraction:
    price = float(f"{price_whole.getText(strip=True)}{price_fraction.getText(strip=True)}")

    if price < 100:
        msg = EmailMessage()
        msg.set_content(f"The product '{title}' is under 100. Go buy it now!")
        msg['Subject'] = 'Product under 100'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'jonisefiu1@gmail.com'

        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
            connection.send_message(msg)
            print("Email sent")
else:
    print("Price or title not found.")

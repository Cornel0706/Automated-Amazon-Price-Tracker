import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
SMTP_SERVER  = os.getenv("SMTP_ADDRESS")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

webpage_link = "https://www.amazon.com/ZOTAC-AI-Enhanced-Gaming-Desktop-Computer/dp/B0G22KLB4R/ref=sr_1_2_sspa?crid=1MIBTC739VXL9&dib=eyJ2IjoiMSJ9.XGpoNK9e52_OSELbztlFHPsexB7_2hquboJ79z4LG_MXaIMFVFg0mqooc1MG8gafO6Iskck1NZlKGYbwKyNE0Q7NQxZpRblXzNBgZSTeggHBRiVorhe6gU-hNFDJerT-gyeOjpl9rZ5AJKJnPokcx6orZ3-HEriEP5ObEYcRFix1Xd_AuwSVnS0nEC4KgmOPdgsfukm4VECMNHqZVCvxEeXpcxQagNYVI2GumwN0JCI.vJsyD05NvsAYBgmV69Au0EPOWVUO9JIkTttQAGT6-mk&dib_tag=se&keywords=Gaming%2BPC&qid=1765882572&refinements=p_n_g-1004207420091%3A13580788011%2Cp_n_g-1004196779091%3A18107822011&rnid=3012494011&sprefix=gaming%2B%2Caps%2C236&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}
response = requests.get(webpage_link, headers=header)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

price_whole = soup.find(name="span", class_="a-price-whole").getText().split(".")[0]
price_decimal = soup.find(name="span", class_="a-price-fraction").getText()
final_price = f"{price_whole}.{price_decimal}"

product_title = soup.find(name="span", id="productTitle").getText().strip()

currency = soup.find(name="span", class_="a-price-symbol").getText().strip()

if float(final_price.replace(',', '')) < 13000:
    with smtplib.SMTP(SMTP_SERVER, port=587) as connection:
        connection.starttls()

        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs="zamfirescucorneliuandrei@gmail.com",
            msg= f"Subject: Amazon Price Alert!\n\nThe price for '{product_title}' has dropped to {currency} {final_price} ."
        )
    print("Email sent successfully!")
else:
    print("The price is not low enough yet!")





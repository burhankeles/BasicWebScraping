from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import MySQLdb
db = MySQLdb.connect(host = "localhost",user = "root",passwd = "",db = "productinfo", init_command = "set names utf8")
insertrec = db.cursor()
req = Request('https://www.n11.com/telefon-ve-aksesuarlari/cep-telefonu?pg=5', headers={'User-Agent': 'XYZ/3.0','Accept-Encoding':'utf-8'})
uClient = urlopen(req)
page_html = uClient.read().decode('UTF-8').strip()
uClient.close()
page_soup = soup(page_html,"html.parser")
containers = page_soup.find_all("div",{"class":"columnContent adBg"})

for container in containers:
      title_product = container.select_one("h3.productName").get_text(strip=True)
      price_product = container.select_one("a.newPrice").get_text(strip=True)
      seller_product = container.select_one("span.sallerName").get_text(strip=True)
      seller_rating = container.select_one("span.point").get_text(strip=True)
      #print(title_product)
      #print(price_product)
      print(seller_rating)
      sqlquery_seller= f"SELECT id FROM sellerinfo where sellername = '{seller_product}'"
      sqlquery_none_existing = f"INSERT INTO sellerinfo( sellername, sellerrating) VALUES ('{seller_product}','{seller_rating}')"
      sqlquery_product = f"INSERT INTO productinfo( sellerid, productname, productprice) VALUES (({sqlquery_seller}),'{title_product}','{price_product}')"
      if insertrec.execute(sqlquery_seller) == True:
            insertrec.execute(sqlquery_product)
            print(sqlquery_product)
      else:
            insertrec.execute(sqlquery_none_existing)
            print(sqlquery_none_existing)
            insertrec.execute(sqlquery_product)
            print(sqlquery_product)
      #sqlquery_product = f""
      #print(sqlquery_seller)
      #insertrec.execute(sqlquery_seller)
      #insertrec.execute(sqlquery_product)
      db.commit()
db.close()



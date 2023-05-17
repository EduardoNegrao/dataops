from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
 "type": "service_account",
  "project_id": "meu-projeto-atividade-384223",
  "private_key_id": "f60aeeb2e5b65643f78567e188d1c87a68963f79",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDitrCS3EKvcf7q\nWdxksKmKVQCZvdGF6k/fbmUa8+Jp2HfOjrzx8gVK77uRoG3IFdg7JrPDfOq/Zb62\nJukw8InS12+M7EVxfe6U5rcUShio7jm41TRLS8lCHdI9+niZvQf7TsJ4dlc9hHc+\n7aTDRO/bqhtHYddxP9SR+bh+EEHZ3tfpTc02Xu8JrIC5nI+Ltn3Kx7cYSIw76dej\n8tV9d5wXuRSlFnd8nwHqOULw+W1MsMFkwEPzdceFYTixZo8jVAhLqizxqAQjaSZD\n9Y7IS6LihffaPXujRlbh6ZGIR81xmsNvpEbUwA09LXJXJjRq5urfTeGylVQ162+O\n5pqlunxDAgMBAAECggEAG3asDy5VebFigvsdwqjP8Oz5JKak8gb/Y/6YitpObCoH\n4WLTKq/5yikeXLbFdb6HsiqvDhhcy5DEuIYgK4iH+Z2VasnYY7Ywp6MHPJL5R8WM\nAoL5UcG9gJ/iLxXfdCg9Bkl1L2iOiuo4E8xv8COytrZ1lYEZuyNTWdeZbNQFViH5\nLAms+oTYrUk9gzVCZa6Ka08BHsjG+ZMWCyIDMosKheq0ekSKmmSx9+/3WJDMMfGE\n5RuHN/O77sGJLmVk7QDFlsEvihF00FQcDuHx1X5TzpXeYMoraRl5DPgONG9kwBqd\nR11YFB6rxHZU/aLNo8U4pdf+ILJrVlhDsbmS58n+QQKBgQD+NWgGnovy5cWv/Eom\nhbmXF0y/zJ+3ORGDzbVIpUcBd05i1qinMWkRTdwUHqIVED7EPUkSvv7XDxtAgIIp\nKl1mvjZ5CxiMsvj0iAe3gWRzNdjGv0hP5oH7yq2Ya1IM+0DOhQ9FRpMjqXT2QVXD\nS96KWLruuWcnvKBq5y/KMXFzIwKBgQDkT66qwjNtD58jqVY6XZHXdCLCe85PPm71\n1UVwlEW5EW5j3nRdHRboXiGuHHhGgl0RB5fQhC2NKUFLvgOJl2WqsYKXQhMIlbeK\nu6OF+JKYefbXstFvmzPr9QzbNJOvpWsp5aDbt0wIh14FOlr+VvOY463wmOBlRDJp\nz4+2QkZ0YQKBgFbFIAbyY067w2i4sw7HInxCRb5KOFIwNpxIwRJU6BHGCYmPP+4h\n3X08mFx9wFF0RBhz2td9PjtmOqUfuE4Y2dzSHIHgmbac+IFvVUL79a+lt6LPc/1h\n7whlPDAEofMwaASWQoog9uR7WSMdVgrdgM60TsphmqZjqlYTJ6raiaEFAoGBAJwf\nPPK5z87BQvJw5m0M9SDe4rIZVS/tIpVqnIxqZ+8w00rpoKrXrIWDcQaNo1Wb6aYu\nigrlh/yifGsd6W9aHwSFVCa44SkasCLnQt/m5d/sbvZ66iqmd+/fZ0Yygtc2h7xj\nsQbuJckjQBDVIcoQjY08DAKdl7zH0K14aO6aDXGhAoGBAO25vW8onfw/IYlwPVxL\nNlObQ9RVROSEqKipnS+ORFT0zaHP4UeiHps4u7xzxqbakAvHLxGZKIAdaCQfhhLT\ndizsTH1BE0ZIKPKWfuPJ6wlyqKNklKYand5F8wH5ii8SnrRSY3AO0Dy7YoCdJ6nv\nFtTGfgU11W5cAbJUXQISJJct\n-----END PRIVATE KEY-----\n",
  "client_email": "bot-dataops@meu-projeto-atividade-384223.iam.gserviceaccount.com",
  "client_id": "100355511356223944835",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-dataops%40meu-projeto-atividade-384223.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"

}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('gitactions_bucket_dataops') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 

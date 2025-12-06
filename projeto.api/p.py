import requests
import psycopg2

conexao = psycopg2.connect(
    database="paises",
    host="localhost",
    user="postgres",
    password="1234",
    port="5432"
)

url = "https://restcountries.com/v3.1/all?fields=name,capital,region,population"
response = requests.get(url)
data = response.json()

cursor = conexao.cursor()

for country in data:
    name = country["name"]["common"]
    capital = country.get("capital", ["Unknown"])
    population = country.get("population", 0)
    region = country.get("region", "Unknown")

    cursor.execute(
        """
        INSERT INTO countries (name, capital, population, region) 
        VALUES (%s, %s, %s, %s)
        """,
        (name, capital, population, region)
    )

conexao.commit()
cursor.close()
conexao.close()

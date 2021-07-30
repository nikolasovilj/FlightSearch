import pandas as pd
import sqlalchemy as sa
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.dialects import postgresql as pg_dialect
from sqlalchemy.sql import select

df = pd.read_csv("IATA-complete.csv")

engine = sa.create_engine("postgresql://king-ict:king-ict@localhost:5432/king-ict", echo=True)

metadata = MetaData()

airports = Table('airports', metadata,
    Column('id', pg_dialect.INTEGER , primary_key=True),
    Column('IATA', pg_dialect.VARCHAR , nullable=False, unique=True),
    Column('Airport_name', pg_dialect.VARCHAR, nullable=False),
    Column('City', pg_dialect.VARCHAR, nullable=False),
    Column('State', pg_dialect.VARCHAR, nullable=True),
    Column('Country', pg_dialect.VARCHAR, nullable=False),
    Column('Country_alpha_2', pg_dialect.VARCHAR, nullable=True),
    Column('Country_alpha_3', pg_dialect.VARCHAR, nullable=True),
    Column('lat', pg_dialect.FLOAT, nullable=True),
    Column('lng', pg_dialect.FLOAT, nullable=True)
)

metadata.create_all(engine)

aerodromi = df.to_dict(orient='records')

ins = airports.insert()

print(str(ins))

result = engine.execute(ins, aerodromi)

s = select(airports)

r = engine.execute(s)

for i in r:
    print(i)
    break



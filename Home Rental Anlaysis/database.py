import sqlite3

def connect_to_database():
    connection = sqlite3.connect('rental_properties.db')
    return connection

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS houses (
        id TEXT PRIMARY KEY,
        type TEXT,
        address1 TEXT,
        address2 TEXT,
        city TEXT,
        area TEXT,
        postcode TEXT,
        rentPpw DOUBLE,
        deposit DOUBLE,
        lat DOUBLE,
        lon DOUBLE,
        url TEXT,
        thumb TEXT,
        specialOffer BOOLEAN,
        availableRooms INTEGER            
    )''')

    connection.commit()

def insert_house(connection, id, type, address1, address2, city, area, postcode, rentppw, deposit, lat, lon, url, thumb, specialoffer,availablerooms):
    cursor = connection.cursor()
    cursor.execute(f"""INSERT or REPLACE INTO houses
                    (id,type,address1,address2,city,area,postcode,rentppw,deposit,lat,lon,url,thumb,specialoffer,availablerooms)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (id,type,address1,address2,city,area,postcode,rentppw,deposit,lat,lon,url,thumb,specialoffer,availablerooms))
    connection.commit()

def get_all_cities(connection):
    cursor = connection.cursor()
    cursor.execute(f'Select distinct(city) from houses')
    cities = []
    for row in cursor.fetchall():
        cities.append(row[0])
    return cities

def get_all_types(connection):
    cursor = connection.cursor()
    cursor.execute(f'Select distinct(type) from houses')
    types = []
    for row in cursor.fetchall():
        types.append(row[0])
    return types

def get_houses_count_in_city(connection, city = None):
    cursor = connection.cursor()
    if city:
        query = f"SELECT count(*) FROM houses WHERE city = '{city}'"
    else:
        query = f"SELECT count(*) FROM houses"
    cursor.execute(query)
    num_houses = cursor.fetchone()[0]
    return num_houses

def get_avg_min_max_rent_in_city(connection, city, aggregation):
    cursor = connection.cursor()
    if city:
        query = f"SELECT {aggregation}(rentppw) FROM houses WHERE city = '{city}'"
    else:
        query = f"SELECT {aggregation}(rentppw) FROM houses"
    cursor.execute(query)
    price = cursor.fetchone()[0]
    return int(price)

def delete_tables(connection, tables):
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"DROP TABLE {table}")
        connection.commit()
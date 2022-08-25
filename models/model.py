import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class PostgreSQLDatabase():
    """postgresql database"""

    def __init__(self):
        pass

    __instance = None

    @staticmethod
    def get_instance(re_init=False):
        if PostgreSQLDatabase.__instance is None or re_init is True:
            return PostgreSQLDatabase()
        return PostgreSQLDatabase.__instance

    def connect(self):
        try:
            db_name = os.environ.get('DB_NAME')
            print(db_name)
            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=DB_USER,
                password=DB_PASSWORD,
                host="localhost",
                port="5432"
            )
            print(self.conn)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            self.dict_cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print(f"Connected to {db_name}")
        except Exception:
            print("Connection to PostgreSQL failed")
        return True

    def create_truck_table(self):
        create_truck = ("CREATE TABLE IF NOT EXISTS trucks"
                        "("
                        "id uuid DEFAULT uuid_generate_v4 (),"
                        "driver_name VARCHAR (50) NOT NULL,"
                        "number_plate VARCHAR (50) NOT NULL,"
                        "color VARCHAR (50) NOT NULL,"
                        "model VARCHAR (50) NOT NULL,"
                        "date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),"
                        "phone_number VARCHAR (50) NOT NULL,"
                        "NIN_number VARCHAR (50) NOT NULL,"
                        "duration_type VARCHAR (50) NOT NULL,"
                        "charge_value INTEGER NOT NULL,"
                        "PRIMARY KEY (id)"
                    ")")

        self.cur.execute(create_truck)
        return True

    def create_car_table(self):
        create_car = ("CREATE TABLE IF NOT EXISTS cars"
                      "("
                      "id uuid DEFAULT uuid_generate_v4 (),"
                      "driver_name VARCHAR (50) NOT NULL,"
                      "number_plate VARCHAR (50) NOT NULL,"
                      "color VARCHAR (50) NOT NULL,"
                      "model VARCHAR (50) NOT NULL,"
                      "date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),"
                      "phone_number VARCHAR (50) NOT NULL,"
                      "NIN_number VARCHAR (50) NOT NULL,"
                      "duration_type VARCHAR (50) NOT NULL,"
                      "charge_value INTEGER NOT NULL,"
                      "PRIMARY KEY (id)"
                    ")")
        self.cur.execute(create_car)
        return True

    def create_taxis_table(self):
        create_taxis = ("CREATE TABLE IF NOT EXISTS taxis"
                        "("
                        "id uuid DEFAULT uuid_generate_v4 (),"
                        "driver_name VARCHAR (50) NOT NULL,"
                        "number_plate VARCHAR (50) NOT NULL,"
                        "color VARCHAR (50) NOT NULL,"
                        "model VARCHAR (50) NOT NULL,"
                        "date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),"
                        "phone_number VARCHAR (50) NOT NULL,"
                        "NIN_number VARCHAR (50) NOT NULL,"
                        "duration_type VARCHAR (50) NOT NULL,"
                        "charge_value INTEGER NOT NULL,"
                        "PRIMARY KEY (id)"
                    ")")

        self.cur.execute(create_taxis)
        return True

    def create_coasters_table(self):
        create_coasters = ("CREATE TABLE IF NOT EXISTS coasters"
                           "("
                           "id uuid DEFAULT uuid_generate_v4 (),"
                           "driver_name VARCHAR (50) NOT NULL,"
                           "number_plate VARCHAR (50) NOT NULL,"
                           "color VARCHAR (50) NOT NULL,"
                           "model VARCHAR (50) NOT NULL,"
                           "date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),"
                           "phone_number VARCHAR (50) NOT NULL,"
                           "NIN_number VARCHAR (50) NOT NULL,"
                           "duration_type VARCHAR (50) NOT NULL,"
                           "charge_value INTEGER NOT NULL,"
                           "PRIMARY KEY (id)"
                        ")")

        self.cur.execute(create_coasters)
        return True

    def create_boda_bodas_table(self):
        create_boda_bodas = ("CREATE TABLE IF NOT EXISTS bodabodas"
                             "("
                             "id uuid DEFAULT uuid_generate_v4 (),"
                             "driver_name VARCHAR (50) NOT NULL,"
                             "number_plate VARCHAR (50) NOT NULL,"
                             "color VARCHAR (50) NOT NULL,"
                             "model VARCHAR (50) NOT NULL,"
                             "date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),"
                             "phone_number VARCHAR (50) NOT NULL,"
                             "NIN_number VARCHAR (50) NOT NULL,"
                             "duration_type VARCHAR (50) NOT NULL,"
                             "charge_value INTEGER NOT NULL,"
                             "PRIMARY KEY (id)"
                        ")")

        self.cur.execute(create_boda_bodas)
        return True

    def create(
        self,
        driver_name: str,
        number_plate: str,
        color: str,
        model: str,
        phone_number: str,
        nin_number: str,
        duration_type: str,
        charge_value: int,
        vehicle_type: str
    ):

        try:
            if vehicle_type == "trucks":
                self.create_truck_table()
            elif vehicle_type == "cars":
                self.create_car_table()
            elif vehicle_type == "taxis":
                self.create_taxis_table()
            elif vehicle_type == "coasters":
                self.create_coasters_table()
            elif vehicle_type == "bodabodas":
                self.create_boda_bodas_table()

            insert_stmt = (
                """INSERT INTO {}
                (
                    driver_name,
                    number_plate,
                    color,
                    model,
                    phone_number,
                    nin_number,
                    duration_type,
                    charge_value
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
            )
            record_to_insert = (
                driver_name,
                number_plate,
                color,
                model,
                phone_number,
                nin_number,
                duration_type,
                charge_value
            )

            query = insert_stmt.format(vehicle_type)

            record_id = self.cur.execute(query, record_to_insert)
            count = self.cur.rowcount
            # getting record id
            record = self.cur.fetchone()
            sql_select_query = """SELECT * from {} where id=%s""".format(
                vehicle_type)
            self.cur.execute(sql_select_query, (record,))
            # getting full record_object
            record_data = self.cur.fetchone()

            recordObject = []
            columnNames = [column[0] for column in self.cur.description]

            if record is not None:
                created_object = dict(zip(columnNames, record_data))
                recordObject.append(dict(zip(columnNames, record_data)))
                print(recordObject)
                print(count, "Record inserted successfully into {} table".format(vehicle_type))
                reason = "Data inserted into database successfully"
                return True, created_object

        except (Exception, psycopg2.Error) as error:
            print(error)
            print("Failed to insert record into mobile table: ", error)
            reason = "failed to insert data"
            return False, reason

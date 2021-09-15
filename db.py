import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect("users.db", check_same_thread=False)
        self.cur = self.con.cursor()

    def save(self) -> None:
        self.con.commit()

    def close(self) -> None:
        self.con.close()

    def create_table(self) -> None:
        """
        Create Database Table
        """
        sql_statement = """
        CREATE TABLE user
        (phone text, password text, secret text)
        """
        self.cur.execute(sql_statement)
        self.save()

    def insert_values(self, table_name, args: dict) -> None:
        """
        Insert value to table
        """
        phone = args.get("phone")
        password = args.get("password")
        secret = args.get("secret")

        sql_statement = f"""
        INSERT INTO {table_name}
        VALUES ('{phone}', '{password}', '{secret}')
        """
        self.cur.execute(sql_statement)
        self.save()

    def delete_values(self, table_name):
        pass

    def select_secret_key(self, phone):
        """
        Select secret key
        """
        sql_statement = f"""
        SELECT secret
        FROM user
        WHERE phone = :phone
        """
        self.cur.execute(sql_statement, {"phone": phone})
        result = self.cur.fetchone()
        self.save()
        return result[0]
    
    def select_password(self, phone):
        """
        Select password
        """
        sql_statement = f"""
        SELECT password
        FROM user
        WHERE phone = :phone
        """
        self.cur.execute(sql_statement, {"phone": phone})
        result = self.cur.fetchone()
        self.save()
        return result[0]
    
    def select_all_phone(self):
        """
        Select all phone
        """
        sql_statement = f"""
        SELECT phone
        FROM user
        """
        self.cur.execute(sql_statement)
        result = self.cur.fetchall()
        result = self._remove_tuple(result)
        self.save()
        return result
    
    def _remove_tuple(self, result):
        for res in range(len(result)):
            result[res] = result[res][0]
        return result
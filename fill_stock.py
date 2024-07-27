import sqlite3

DATABASE = 'database.db'


def get_db():
    try:
        conn = sqlite3.connect(DATABASE)
        print(f"Подключение к базе данных {DATABASE} успешно установлено.")
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


def create_stock_table():
    conn = get_db()
    if conn is None:
        print("Не удалось подключиться к базе данных. Таблица не будет создана.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                size TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Таблица 'stock' успешно создана или уже существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы 'stock': {e}")
    finally:
        conn.close()


def fill_stock():
    conn = get_db()
    if conn is None:
        print("Не удалось подключиться к базе данных. Данные не будут добавлены.")
        return

    cursor = conn.cursor()

    try:
        # Удаляем текущие записи в таблице stock
        cursor.execute('DELETE FROM stock')
        conn.commit()
        print("Таблица 'stock' очищена.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении данных: {e}")
        conn.rollback()

    # Вставляем новые данные
    stock_data = [
        ('Куртка рабочая', 'XL', 2500.0, 10, 'Склад A'),
        ('Брюки рабочие', 'L', 1800.0, 15, 'Склад B'),
        ('Жилетка сигнальная', 'M', 1200.0, 20, 'Склад C'),
        ('Перчатки защитные', 'S', 500.0, 30, 'Склад D'),
        ('Фартук медицинский', 'XL', 1500.0, 12, 'Склад E'),
        ('Беруши защитные', 'M', 300.0, 25, 'Склад F'),
        ('Шлем строительный', 'L', 2000.0, 8, 'Склад G'),
        ('Очки защитные', 'S', 700.0, 18, 'Склад H'),
        ('Респиратор противогаза', 'XL', 3500.0, 5, 'Склад I'),
        ('Ботинки защитные', 'L', 2800.0, 12, 'Склад J'),
        ('Каска строительная', 'M', 1800.0, 15, 'Склад K'),
        ('Пояс сигнальный', 'S', 1000.0, 20, 'Склад L'),
        ('Фартук поварской', 'XL', 1200.0, 25, 'Склад M'),
        ('Рукавицы механика', 'L', 600.0, 30, 'Склад N'),
        ('Куртка утепленная', 'M', 3500.0, 8, 'Склад O'),
        ('Брюки медицинские', 'S', 1800.0, 15, 'Склад P'),
        ('Жилетка охранный', 'XL', 2000.0, 12, 'Склад Q'),
        ('Перчатки монтажные', 'L', 500.0, 20, 'Склад R'),
        ('Фартук строительный', 'M', 1500.0, 25, 'Склад S'),
        ('Маска медицинская', 'S', 800.0, 30, 'Склад T'),
        ('Беруши монтажные', 'XL', 400.0, 10, 'Склад U'),
        ('Шлем медицинский', 'L', 2500.0, 15, 'Склад V'),
        ('Очки монтажные', 'M', 700.0, 18, 'Склад W'),
        ('Респиратор медицинский', 'S', 3000.0, 5, 'Склад X'),
        ('Ботинки медицинские', 'XL', 3000.0, 12, 'Склад Y'),
        ('Каска монтажная', 'L', 1800.0, 15, 'Склад Z'),
        ('Пояс строительный', 'M', 1000.0, 20, 'Склад AA'),
        ('Фартук монтажный', 'S', 1200.0, 25, 'Склад AB'),
        ('Рукавицы медицинские', 'XL', 600.0, 30, 'Склад AC')
    ]

    try:
        cursor.executemany("INSERT INTO stock (item_name, size, price, quantity, location) VALUES (?, ?, ?, ?, ?)", stock_data)
        conn.commit()
        print("Данные успешно добавлены в таблицу 'stock'.")
    except sqlite3.Error as e:
        print(f"Ошибка при вставке данных: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    create_stock_table()
    fill_stock()

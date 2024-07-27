from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Генерируем случайный секретный ключ для сессий

DATABASE = 'database.db'


# Функция для получения соединения с базой данных
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


# Создание структуры базы данных
def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')

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
    conn.close()


# Главная страница
@app.route('/')
def index():
    if 'username' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('employee_dashboard'))
    return redirect(url_for('login'))


# Страница продуктов
@app.route('/products', methods=['GET', 'POST'])
def products():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        status = request.form['status']
        cursor.execute("INSERT INTO products (code, name, category, quantity, price, status) VALUES (?, ?, ?, ?, ?, ?)",
                       (code, name, category, quantity, price, status))
        conn.commit()

    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)


# Добавление продукта
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        status = request.form['status']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (code, name, category, quantity, price, status) VALUES (?, ?, ?, ?, ?, ?)",
                       (code, name, category, quantity, price, status))
        conn.commit()
        conn.close()
        return redirect(url_for('products'))
    return render_template('add_product.html')


# Редактирование продукта
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']
        status = request.form['status']

        cursor.execute("""
            UPDATE products
            SET code = ?, name = ?, category = ?, quantity = ?, price = ?, status = ?
            WHERE id = ?
        """, (code, name, category, quantity, price, status, id))

        conn.commit()
        return redirect(url_for('products'))

    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    conn.close()

    return render_template('edit_product.html', id=id, product=product)


# Удаление продукта
@app.route('/delete_product/<int:id>')
def delete_product(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        client = request.form['client']
        for key, value in request.form.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                if quantity > 0:
                    cursor.execute("INSERT INTO orders (client, product_id, quantity) VALUES (?, ?, ?)",
                                   (client, product_id, quantity))
                    cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
                    conn.commit()

    cursor.execute('SELECT * FROM stock')
    stock_items = cursor.fetchall()

    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    conn.close()
    return render_template('orders.html', stock_items=stock_items, products=products)


# Страница склада
@app.route('/stock')
def stock():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    stock_items = cursor.fetchall()
    conn.close()
    return render_template('stock.html', stock_items=stock_items)


# Отчетность
@app.route('/reports')
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stock')
    stock_items = cursor.fetchall()

    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    cursor.execute('''
        SELECT orders.client, stock.item_name, orders.quantity, orders.order_date 
        FROM orders 
        JOIN stock ON orders.product_id = stock.id
    ''')
    orders = cursor.fetchall()

    cursor.execute('SELECT DISTINCT client FROM orders')
    clients = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT DISTINCT item_name FROM stock')
    product_names = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT DISTINCT location FROM stock')
    locations = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template('reports.html', stock_items=stock_items, products=products, orders=orders,
                           clients=clients, product_names=product_names, locations=locations)
# Панель администратора
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session and session['is_admin']:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))


# Панель сотрудника
@app.route('/employee_dashboard')
def employee_dashboard():
    if 'username' in session and not session.get('is_admin'):
        return render_template('employee_dashboard.html')
    return redirect(url_for('login'))


# Страница сотрудников
@app.route('/employees')
def employees():
    if 'username' in session and session['is_admin']:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        conn.close()
        return render_template('employees.html', employees=employees)
    else:
        return redirect(url_for('login'))


# Добавление сотрудника
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'username' in session and session['is_admin']:
        if request.method == 'POST':
            name = request.form['name']
            position = request.form['position']
            login = request.form['login']
            password = request.form['password']

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employees (name, position, login, password) VALUES (?, ?, ?, ?)",
                           (name, position, login, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('employees'))
        return render_template('add_employee.html')
    else:
        return redirect(url_for('login'))


# Редактирование сотрудника
@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if 'username' in session and session['is_admin']:
        conn = get_db()
        cursor = conn.cursor()

        if request.method == 'POST':
            name = request.form['name']
            position = request.form['position']
            login = request.form['login']
            password = request.form['password']

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor.execute("""
                UPDATE employees
                SET name = ?, position = ?, login = ?, password = ?
                WHERE id = ?
            """, (name, position, login, hashed_password, id))

            conn.commit()
            return redirect(url_for('employees'))

        cursor.execute('SELECT * FROM employees WHERE id = ?', (id,))
        employee = cursor.fetchone()
        conn.close()

        return render_template('edit_employee.html', id=id, employee=employee)
    else:
        return redirect(url_for('login'))


# Удаление сотрудника
@app.route('/delete_employee/<int:id>')
def delete_employee(id):
    if 'username' in session and session['is_admin']:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employees WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('employees'))
    else:
        return redirect(url_for('login'))


# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE login = ? AND password = ?", (username, hashed_password))
        admin = cursor.fetchone()

        if admin:
            session['username'] = username
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))

        cursor.execute("SELECT * FROM employees WHERE login = ? AND password = ?", (username, hashed_password))
        employee = cursor.fetchone()

        if employee:
            session['username'] = username
            session['is_admin'] = False
            return redirect(url_for('employee_dashboard'))

        return "Неправильное имя пользователя или пароль"

    return render_template('login.html')


# Логаут
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
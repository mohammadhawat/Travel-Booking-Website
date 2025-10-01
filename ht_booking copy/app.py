# Mohammad Hawat - Student ID: 24056361

from flask import Flask, render_template, request, redirect, session
from db_config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                           (name, email, hashed_pw))
            conn.commit()
            conn.close()
            return "✅ Registered successfully!"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user'] = user[1]
            session['user_id'] = user[0]
            return redirect('/')
        else:
            return "❌ Invalid credentials. Try again."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = session['user_id']
    selected_day = ''
    selected_class = ''

    if request.method == 'POST' and 'seats' in request.form and 'journey_id' in request.form and request.form['seats'].strip():
        journey_id = request.form['journey_id']
        seats = int(request.form['seats'])

        cursor.execute("SELECT origin, destination, departure_time, arrival_time, fare, travel_class, seat_capacity, seats_booked FROM journeys WHERE id = %s", (journey_id,))
        journey = cursor.fetchone()

        if not journey:
            return "Journey not found."

        capacity = journey[6]
        booked = journey[7]
        if booked + seats > capacity:
            return "❌ Not enough seats available."

        cursor.execute("UPDATE journeys SET seats_booked = seats_booked + %s WHERE id = %s", (seats, journey_id))
        cursor.execute("INSERT INTO bookings (user_id, journey_id, seats_booked) VALUES (%s, %s, %s)",
                       (user_id, journey_id, seats))
        conn.commit()

        cursor.execute("""
            SELECT origin, destination, departure_time, arrival_time, fare, travel_class, bookings.seats_booked, booking_time
            FROM bookings
            JOIN journeys ON bookings.journey_id = journeys.id
            WHERE bookings.user_id = %s
            ORDER BY booking_time DESC
            LIMIT 1
        """, (user_id,))
        data = cursor.fetchone()
        conn.close()

        booking = {
            'origin': data[0],
            'destination': data[1],
            'departure_time': data[2],
            'arrival_time': data[3],
            'fare': float(data[4]),
            'travel_class': data[5],
            'seats_booked': data[6],
            'booking_time': data[7],
            'total': round(float(data[4]) * int(data[6]), 2)
        }

        return render_template('confirmation.html', booking=booking, user=session.get('user'))

    else:
        query = "SELECT id, origin, destination, departure_time, arrival_time, fare, travel_class FROM journeys WHERE 1=1"
        filters = []

        selected_day = request.form.get('filter_day') or ''
        selected_class = request.form.get('filter_class') or ''

        if selected_day:
            query += " AND travel_day = %s"
            filters.append(selected_day)
        if selected_class:
            query += " AND travel_class = %s"
            filters.append(selected_class)

        cursor.execute(query, tuple(filters))
        journeys = cursor.fetchall()
        conn.close()

        return render_template('book.html', journeys=journeys, user=session.get('user'),
                               selected_day=selected_day, selected_class=selected_class)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users WHERE id = %s", (session['user_id'],))
    data = cursor.fetchone()

    user_data = {
        'name': data[0],
        'email': data[1]
    }

    message = ''

    if request.method == 'POST':
        new_pw = request.form['new_password']
        hashed_pw = generate_password_hash(new_pw)

        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_pw, session['user_id']))
        conn.commit()
        message = "✅ Password updated successfully."

    conn.close()
    return render_template('profile.html', user=session.get('user'), user_data=user_data, message=message)

@app.route('/emailpreview')
def email_preview():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT origin, destination, departure_time, arrival_time, fare, travel_class, bookings.seats_booked, booking_time
        FROM bookings
        JOIN journeys ON bookings.journey_id = journeys.id
        WHERE bookings.user_id = %s
        ORDER BY booking_time DESC
        LIMIT 1
    """, (session['user_id'],))
    
    data = cursor.fetchone()
    conn.close()

    if not data:
        return "No bookings found."

    booking = {
        'origin': data[0],
        'destination': data[1],
        'departure_time': data[2],
        'arrival_time': data[3],
        'fare': float(data[4]),
        'travel_class': data[5],
        'seats_booked': data[6],
        'booking_time': data[7],
        'total': round(float(data[4]) * int(data[6]), 2)
    }

    return render_template('email_preview.html', booking=booking, user=session.get('user'))

@app.route('/mybookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bookings.id, origin, destination, departure_time, arrival_time, fare, travel_class,
               bookings.seats_booked, booking_time
        FROM bookings
        JOIN journeys ON bookings.journey_id = journeys.id
        WHERE bookings.user_id = %s
        ORDER BY booking_time DESC
    """, (user_id,))

    bookings = cursor.fetchall()
    conn.close()
    return render_template('mybookings.html', bookings=bookings, user=session.get('user'))

@app.route('/cancelbooking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT journey_id, seats_booked FROM bookings WHERE id = %s AND user_id = %s",
                   (booking_id, user_id))
    data = cursor.fetchone()

    if data:
        journey_id, seats = data
        cursor.execute("DELETE FROM bookings WHERE id = %s AND user_id = %s", (booking_id, user_id))
        cursor.execute("UPDATE journeys SET seats_booked = seats_booked - %s WHERE id = %s", (seats, journey_id))
        conn.commit()

    conn.close()
    return redirect('/mybookings')

@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        else:
            return "❌ Invalid admin credentials."
    return render_template('adminlogin.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/adminlogin')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.name, origin, destination, departure_time, arrival_time, fare, travel_class,
               bookings.seats_booked, booking_time
        FROM bookings
        JOIN journeys ON bookings.journey_id = journeys.id
        JOIN users ON bookings.user_id = users.id
        ORDER BY booking_time DESC
    """)
    bookings = cursor.fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings, user=session.get('user'))

@app.route('/admin/reports')
def admin_reports():
    if not session.get('admin'):
        return redirect('/adminlogin')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT origin, destination, COUNT(*) AS total_bookings
        FROM bookings
        JOIN journeys ON bookings.journey_id = journeys.id
        GROUP BY origin, destination
        ORDER BY total_bookings DESC
        LIMIT 5
    """)
    popular_routes = cursor.fetchall()

    cursor.execute("""
        SELECT users.name, COUNT(*) AS total
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        GROUP BY users.name
        ORDER BY total DESC
        LIMIT 5
    """)
    top_users = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(journeys.fare * bookings.seats_booked)
        FROM bookings
        JOIN journeys ON bookings.journey_id = journeys.id
    """)
    total_revenue = cursor.fetchone()[0] or 0.00

    conn.close()
    return render_template('admin_reports.html',
                           popular_routes=popular_routes,
                           top_users=top_users,
                           total_revenue=round(total_revenue, 2),
                           user=session.get('user'))
@app.route('/admin/passwords', methods=['GET', 'POST'])
def admin_passwords():
    if not session.get('admin'):
        return redirect('/adminlogin')

    message = ''

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        form_type = request.form.get('type')

        if form_type == 'admin':
            new_pw = request.form['new_admin_password']
            hashed_pw = generate_password_hash(new_pw)
            # This is a simulated storage method — storing hashed admin password in a local file
            with open("admin_password.txt", "w") as f:
                f.write(hashed_pw)
            message = "✅ Admin password updated (simulated — see note)."

        elif form_type == 'user':
            email = request.form['user_email']
            new_pw = request.form['new_user_password']
            hashed_pw = generate_password_hash(new_pw)
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_pw, email))
            conn.commit()
            message = f"✅ Password updated for {email}."

        conn.close()

    return render_template('admin_passwords.html', user=session.get('user'), message=message)
@app.route('/dbtest')
@app.route('/admin/journeys', methods=['GET', 'POST'])
def manage_journeys():
    if not session.get('admin'):
        return redirect('/adminlogin')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        form_type = request.form['form_type']

        if form_type == 'add':
            cursor.execute("""
                INSERT INTO journeys (origin, destination, departure_time, arrival_time, fare, seat_capacity, travel_class, travel_day)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form['origin'],
                request.form['destination'],
                request.form['departure_time'],
                request.form['arrival_time'],
                request.form['fare'],
                request.form['seat_capacity'],
                request.form['travel_class'],
                request.form['travel_day']
            ))

        elif form_type == 'update':
            cursor.execute("""
                UPDATE journeys
                SET origin=%s, destination=%s, departure_time=%s, arrival_time=%s,
                    fare=%s, travel_class=%s, travel_day=%s, seat_capacity=%s
                WHERE id=%s
            """, (
                request.form['origin'],
                request.form['destination'],
                request.form['departure_time'],
                request.form['arrival_time'],
                request.form['fare'],
                request.form['travel_class'],
                request.form['travel_day'],
                request.form['seat_capacity'],
                request.form['journey_id']
            ))

        elif form_type == 'delete':
            cursor.execute("DELETE FROM journeys WHERE id = %s", (request.form['journey_id'],))

        conn.commit()

    cursor.execute("SELECT * FROM journeys")
    journeys = cursor.fetchall()
    conn.close()
    return render_template('admin_journeys.html', journeys=journeys, user=session.get('user'))
@app.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if not session.get('admin'):
        return redirect('/adminlogin')

    conn = get_db_connection()
    cursor = conn.cursor()
    message = ''

    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        email = request.form['email']
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        conn.commit()
        message = f"✅ User {user_id} updated."

    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('admin_users.html', users=users, user=session.get('user'), message=message)
def db_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        result = cursor.fetchone()
        conn.close()
        return f"Users in database: {result[0]}"
    except Exception as e:
        return f"Database error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
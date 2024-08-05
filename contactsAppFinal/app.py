
from flask import Flask, Flask, render_template, request, redirect, url_for, session, jsonify

from utils.establishDBConnection import get_db_connection

app = Flask(__name__, template_folder='templates')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn=get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM contatcs' )
        data=cur.fetchall()
        cur.close()
        jsonify(data=data)

    else:
        return render_template("login.html")
    

    #The contact Details page (Mohamed Ali)
@app.route("/contacts")
def contact_list(): 
    '''If the user ID is not present in view, the user will be redirected to the login page. 
    If the user ID is present, a database will be used to fetch the user's contact list and display it in the contacts.html page.'''
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else: 
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM contacts WHERE user_id = %s', (session['user_id'],))
        contacts = cur.fetchall()
        cur.close()
        return render_template("contacts.html", contacts=contacts) # name the page contacts.html 
    

@app.route("/contact/<int:contact_id>")
def view_contact(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM contacts WHERE id = %s AND user_id = %s', (contact_id, session['user_id']))
        contact = cur.fetchone()
        cur.close()

        return render_template("view_contact.html", contact=contact)


@app.route("/contact/<int:contact_id>/edit", methods=['GET', 'POST'])
def edit_contact(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        cur.execute('UPDATE contacts SET name = %s, email = %s, phone = %s WHERE id = %s AND user_id = %s',
                    (name, email, phone, contact_id, session['user_id']))
        conn.commit()
        cur.close()
        return redirect(url_for('contact_list'))
    else:
        cur.execute('SELECT * FROM contacts WHERE id = %s AND user_id = %s', (contact_id, session['user_id']))
        contact = cur.fetchone()
        cur.close()
        return render_template("edit_contact.html", contact=contact)

@app.route("/contact/<int:contact_id>/delete", methods=['POST'])
def delete_contact(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = %s AND user_id = %s', (contact_id, session['user_id']))
    conn.commit()
    cur.close()

    return redirect(url_for('contact_list'))

if __name__ == "__main__":
    app.run(debug=True)

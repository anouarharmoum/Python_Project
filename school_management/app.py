from flask import  Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def layout():
    return render_template('layout.html')

@app.route("/notes")
def notes():
    return render_template("pages/Note/notes.html")

@app.route("/students")
def students():
    return render_template("pages/students/students.html")    

@app.route('/notes/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get form data
        student_id = request.form.get('student_id')
        exam = request.form.get('exam')
        tp = request.form.get('tp')
        control = request.form.get('control')
        absence = request.form.get('absence')
        final_note = request.form.get('final_note')

        # Save to database (example only, replace with your DB logic)
        # db.execute("INSERT INTO notes (student_id, exam, tp, control, absence, final_note) VALUES (?, ?, ?, ?, ?, ?)",
        #            (student_id, exam, tp, control, absence, final_note))
        # db.commit()

        return redirect(url_for('/'))  # Redirect to main page

    return render_template('pages/Note/create.html')



if __name__ == "__main__":
    app.run(debug=True)
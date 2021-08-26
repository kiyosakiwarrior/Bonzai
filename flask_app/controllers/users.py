from flask import render_template,redirect,request,session
from flask_app import app

from flask_app.models.user import User
from flask_app.models.thought import Thought, Comment


@app.route('/')
def index():
    # call the get all classmethod to get all friends
    return render_template("index.html")

@app.route('/personal')
def personal():
    # call the get all classmethod to get all friends
    return render_template("personal.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    # call the get all classmethod to get all friends
    all_thoughts = Thought.get_all_thoughts()
    if "user_id" not in session:
        return redirect("/")
    user = User.get_one_by_id(session)
    users = User.get_all()
    return render_template("thoughts.html", user = user, users = users, all_thoughts = all_thoughts)

@app.route('/users', methods=['POST'])
def create_user():
    print("Got Post Info")
    # Here we add two properties to session to store the name and email

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password']
    }
    if not User.validate_registration(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    if not User.unique_email(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    if not User.validate_email(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    session['user_id'] = User.save(data)
    return redirect ("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    print("Got Post Info")
    # Here we add two properties to session to store the name and email
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    if not User.email_match(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    if not User.password_match(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    user = User.get_one(data)
    session['user_id'] = user.id 
    return redirect('/dashboard')

@app.route('/create_thought/<int:userid>', methods=["POST"])
def create_thought(userid):
    data = {
        "thought": request.form["thought"],
        "user_id" : userid
    }
    if not Thought.validate_submission(request.form):
        # we redirect to the template with the form.
        return redirect('/dashboard')
    Thought.save_thought(data)
    return redirect("/dashboard")

@app.route('/destroy/<int:id>')
def destroy(id):
    data = {
        "id" : id
    }
    Thought.destroy(data)
    return redirect("/dashboard")

@app.route('/show/<int:user_id>')
def show(user_id):
    if "user_id" not in session:
        return redirect("/")
    data ={ 
        "user_id": user_id
    }
    thoughts = Thought.get_user_thoughts(data)
    user = User.get_one_by_id(session)
    selected_user = User.get_one_by_id(data)
    return render_template("show_thoughts.html", user=user, selected_user=selected_user, thoughts=thoughts)

@app.route('/comments/<int:id>/<int:user_id>')
def comments(id,user_id):
    if "user_id" not in session:
        return redirect("/")
    data ={ 
        "id": id
    }
    thought = Thought.get_one_thought(data)
    all_comments = Comment.get_comments(data)
    user = User.get_one_by_id(session)
    data = {
        "user_id": user_id
    }
    users = User.get_all()
    selected_user = User.get_one_by_id(data)
    return render_template("comments.html", user=user, users=users, selected_user=selected_user, thought=thought, all_comments = all_comments)

@app.route('/create_comment/<int:user_id>/<int:thought_id>/<int:selected_user_id>', methods=["POST"])
def create_comment(user_id, thought_id, selected_user_id):
    data = {
        "comment": request.form["comment"],
        "user_id" : user_id,
        "id" : thought_id
    }
    Comment.save_comment(data)
    thought = Thought.get_one_thought(data)
    all_comments = Comment.get_comments(data)
    user = User.get_one_by_id(session)
    data = {
        "user_id": selected_user_id
    }
    users = User.get_all()
    selected_user = User.get_one_by_id(data)
    return render_template("comments.html", user=user, users=users, selected_user=selected_user, thought=thought, all_comments = all_comments)

@app.route('/destroy_comment/<int:id>/<int:thought_id>/<int:selected_user_id>')
def destroy_comment(id, thought_id, selected_user_id):
    data = {
        "comment_id" : id,
        "id" : thought_id
    }
    Comment.destroy_comment(data)
    thought = Thought.get_one_thought(data)
    all_comments = Comment.get_comments(data)
    user = User.get_one_by_id(session)
    data = {
        "user_id": selected_user_id
    }
    users = User.get_all()
    selected_user = User.get_one_by_id(data)
    return render_template("comments.html", user=user, users=users, selected_user=selected_user, thought=thought, all_comments = all_comments)

@app.route('/like/<int:id>')
def like(id):
    data = {
        "id" : id
    }
    Thought.like(data)
    return redirect("/dashboard")

@app.route('/dislike/<int:id>')
def dislike(id):
    data = {
        "id" : id
    }
    Thought.dislike(data)
    return redirect("/dashboard")

'''
@app.route('/edit/<int:id>')
def edit(id):
    if "user_id" not in session:
        return redirect("/")
    data ={ 
        "id":id
    }
    return render_template("edit.html", recipe=Thought.get_one_recipe(data))

@app.route('/update', methods=['POST'])
def update():
    Thought.update(request.form)
    return redirect("/dashboard")
'''
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Pehle login karen."
login_manager.login_message_category = "warning"


# ---------------- Models ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship("Task", backref="owner", lazy=True,
                            cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default="")
    priority = db.Column(db.String(10), default="Medium")  # Low / Medium / High
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    @property
    def is_overdue(self):
        return bool(self.due_date and not self.completed and self.due_date < date.today())


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ---------------- Helpers ----------------
def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def get_user_task(task_id):
    """Sirf current user ka apna task milega, kisi aur ka nahi."""
    return Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()


# ---------------- Auth routes ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("Saari fields bharna zaroori hai.", "danger")
        elif len(password) < 6:
            flash("Password kam az kam 6 characters ka hona chahiye.", "danger")
        elif password != confirm:
            flash("Dono passwords match nahi kar rahe.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Ye email pehle se registered hai.", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account ban gaya. Ab login karen.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=bool(request.form.get("remember")))
            flash(f"Welcome, {user.username}!", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)
            return redirect(url_for("index"))

        flash("Email ya password galat hai.", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Aap logout ho gaye.", "info")
    return redirect(url_for("login"))


# ---------------- Task routes ----------------
@app.route("/")
@login_required
def index():
    status = request.args.get("status", "all")
    search = request.args.get("q", "").strip()

    query = Task.query.filter_by(user_id=current_user.id)
    if status == "active":
        query = query.filter_by(completed=False)
    elif status == "completed":
        query = query.filter_by(completed=True)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    tasks = query.order_by(Task.completed, Task.created_at.desc()).all()

    total = Task.query.filter_by(user_id=current_user.id).count()
    done = Task.query.filter_by(user_id=current_user.id, completed=True).count()
    stats = {
        "total": total,
        "completed": done,
        "active": total - done,
        "percent": int((done / total) * 100) if total else 0,
    }
    return render_template("index.html", tasks=tasks, stats=stats,
                           status=status, search=search)


@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Task ka title likhna zaroori hai.", "danger")
        return redirect(url_for("index"))

    task = Task(
        title=title,
        description=request.form.get("description", "").strip(),
        priority=request.form.get("priority", "Medium"),
        due_date=parse_date(request.form.get("due_date")),
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    flash("Task add ho gaya.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
@login_required
def toggle(task_id):
    task = get_user_task(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit(task_id):
    task = get_user_task(task_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title khali nahi ho sakta.", "danger")
            return redirect(url_for("edit", task_id=task.id))
        task.title = title
        task.description = request.form.get("description", "").strip()
        task.priority = request.form.get("priority", "Medium")
        task.due_date = parse_date(request.form.get("due_date"))
        db.session.commit()
        flash("Task update ho gaya.", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", task=task)


@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete(task_id):
    task = get_user_task(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task delete ho gaya.", "warning")
    return redirect(url_for("index"))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
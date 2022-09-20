from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from expenses_app import app, db, bcrypt
from expenses_app.forms import ExpenseForm, JoinGroupForm, LoginForm, RegistrationForm
from expenses_app.models import User, Group, Expense


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('groups'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('groups'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Sėkmingai prisijungta', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    groups = current_user.groups
    form = JoinGroupForm()
    if form.validate_on_submit():
        group = Group.query.get(form.group_id.data)
        current_user.groups.append(group)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('groups'))
    return render_template('groups.html', groups=groups, form=form)


@app.route('/groups/<int:group_id>', methods=['GET', 'POST'])
@login_required
def expenses(group_id):
    group = Group.query.get(group_id)
    if group not in current_user.groups or group is None:
        abort(404)

    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            description=form.description.data,
            group_id=group.id,
            user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('expenses', group_id=group.id))
    return render_template('expenses.html', group=group, form=form)


@app.errorhandler(404)
def klaida_404(klaida):
    return render_template("404.html"), 404

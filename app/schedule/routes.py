from flask import render_template, redirect, url_for
from flask_login import login_required
from flask_babel import _
from app import db
from app.schedule.forms import AddEmployee
from app.models import Employee
from app.schedule import bp


@bp.route('/', methods=['GET', 'POST'])
@login_required
def schedule():
    # schedule_posts = SchedulePost().query.order_by(SchedulePost.timestamp.desc()).all()
    return render_template('schedule.html', title=_('schedule'))


# Employees
@bp.route('/employees')
@login_required
def employees():
    employees_ = Employee.query.order_by(Employee.last_name).all()
    return render_template('employees.html', title=_('Employees'), employees=employees_)


@bp.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = AddEmployee()
    if form.validate_on_submit():
        add_employee_ = Employee(
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            patronymic=form.patronymic.data,
            is_active=form.is_active.data,
            preferred_time=form.preferred_time.data,
            work_hours_in_day=form.work_hours_in_day.data
        )
        db.session.add(add_employee_)
        db.session.commit()
        return redirect(url_for('schedule.employees'))
    return render_template('add_employee.html', title=_('Add Employee'), form=form)


@bp.route('/edit_employee/<id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    edit_employee_ = Employee.query.filter_by(id=id).first()
    form = AddEmployee(
        last_name=edit_employee_.last_name,
        first_name=edit_employee_.first_name,
        patronymic=edit_employee_.patronymic,
        is_active=edit_employee_.is_active,
        preferred_time=edit_employee_.preferred_time,
        work_hours_in_day=edit_employee_.work_hours_in_day
    )
    if form.validate_on_submit():
        edit_employee_.last_name = form.last_name.data
        edit_employee_.first_name = form.first_name.data
        edit_employee_.patronymic = form.patronymic.data
        edit_employee_.is_active = form.is_active.data
        edit_employee_.preferred_time = form.preferred_time.data
        edit_employee_.work_hours_in_day = form.work_hours_in_day.data
        db.session.commit()
        return redirect(url_for('schedule.employees'))
    return render_template('add_employee.html', title=_('Edit Employee'), form=form)


@bp.route('/deactivate_employee/<id>')
@login_required
def deactivate_employee(id):
    pass


@bp.route('/add_schedule')
@login_required
def add_schedule():
    return render_template('add_schedule.html', title=_('Add Schedule'))
    

@bp.route('/edit_schedule/<id>')
@login_required
def edit_schedule(id):
    pass


@bp.route('/delete_schedule/<id>')
@login_required
def delete_schedule(id):
    pass

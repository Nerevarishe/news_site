from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    news = db.relationship('News', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    # Источник новости. ORD-<id> при создании новости из модуля приказов, SOP-<id> - из модуля СОПов.
    source = db.Column(db.String, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post: {}'.format(self.body)


class FaqPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Title: {}, Post: {}'.format(self.title, self.body)


class LawPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Title: {}, Post: {}'.format(self.title, self.body)


class ExpdateTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String)
    exp_date = db.Column(db.DateTime, index=True)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Drug Name: {}\n Exp. Date: {}\n amount: {}'.format(self.drug_name, self.exp_date, self.amount)


class SOPPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Title: {}, Post: {}'.format(self.title, self.body)


class EdinfoPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'Title: {}, Post: {}'.format(self.title, self.body)


class DefecturaCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String)
    comment = db.Column(db.String)
    employee_name = db.Column(db.String)
    in_zd = db.Column(db.Boolean, default=False, index=True)
    date = db.Column(db.Date, index=True)
    ip = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Drug name: {}, date: {}'.format(self.drug_name, self.date)


class DrugstoreList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ds_name = db.Column(db.String)
    ds_adress = db.Column(db.String)
    ds_worktime = db.Column(db.String)
    ds_phone = db.Column(db.String)
    ds_ip_phone = db.Column(db.String)

    def __repr__(self):
        return 'id: {}, ds_name: {}, ds_adress: {}, ds_worktime: {}, ds_phone: {}, ds_ip_phone: {}' \
            .format(self.id, self.ds_name, self.ds_adress, self.worktime, self.ds_phone, self.ds_ip_phone)


class ServiceCenterList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brands = db.Column(db.String)
    sc_adress = db.Column(db.String)
    sc_phone = db.Column(db.String)
    
    def __repr__(self):
        return 'id: {}, brands: {}, sc_adress: {}, sc_phone: {}'.format(self.id, self.brands, self.sc_adress,
                                                                        self.sc_phone)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String, index=True)
    first_name = db.Column(db.String)
    patronymic = db.Column(db.String)
    is_active = db.Column(db.Boolean(), default=True)
    preferred_time = db.Column(db.String)
    work_hours_in_day = db.Column(db.String)
    shift = db.Column(db.Integer, db.ForeignKey('shift.id'))

    def __repr__(self):
        return '''id: {}, {} {} {}
        Preferred time: {}
        Is Employee active: {}
        Work hours in day: {}'''.format(self.id, self.last_name, self.firs_name, self.patronymic, self.preferred_time,
                                         self.is_active, self.work_hours_in_day)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String)
    month = db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    hours_in_month = db.Column(db.Integer)
    vacation_days = db.Column(db.Integer)
    vacation_start_date = db.Column(db.DateTime)
    vacation_end_date = db.Column(db.DateTime)
    
    def __repr__(self):
        return '''year: {}
        month: {}
        employee: {}
        hours in month: {}
        vacation days: {}
        vacation start date: {}
        vacation end date: {}''' \
        .format(self.year, self.month,
                Employee.query.filter_by(id=self.employee_id).first().last_name,
                self.hours_in_month, self.vacation_days, self.vacation_start_date,
                self.vacation_end_date)
    
    
class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shift_name = db.Column(db.String)
    comment = db.Column(db.String)
    employees = db.relationship('Employee', backref='shift_', lazy='dynamic')

    def __repr__(self):
        return '''Shift: {}
        Comment: {}
        Employees: {}
        '''.format(self.shift_name, self.comment, self.employees)


class DeferredDrug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String)
    drug_amount = db.Column(db.Integer)
    comment = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
from odoo import fields,models

class Employee(models.Model):
    _name="employee.ept"
    _description = "Employee Management System Demo"

    name=fields.Char(string="Employee Name", help="Name of employee")
    department_id = fields.Many2one('employee.department.ept', string="Department", help="Department data from department model")
    shift_id = fields.Many2one('employee.department.shift.ept', string="Shift", help="Shift data from shift model")
    job_position = fields.Char(string="Job Position", help="Job Position Field")
    salary = fields.Float(string="Salary", help="Salary field of this model")
    hire_date = fields.Date(string="Higher Date", help="Hire Date field of this model")
    gender = fields.Selection(selection=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')])
    job_type = fields.Selection(selection=[('Permanent', 'Permanent'), ('Ad Hoc', 'Ad Hoc')])
    is_manager = fields.Boolean(string="Is Manager?", help="Identify this employee is manager or not")
    manager_id = fields.Many2one('employee.ept', string="Manager", help="main id of this table will refer as manager id")
    related_user_id = fields.Many2one('res.users', string="User", help="this data will be load from user model")
    employee_ids = fields.One2many('employee.ept', 'manager_id', string="Manager")
    increment_percentage = fields.Float(string="Increment %", help="Enter value for increment percentage")


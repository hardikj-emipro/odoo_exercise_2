from odoo import models,fields

class Department_Shift(models.Model):
    _name = "employee.department.shift.ept"
    _description="Employee Management System Demo"
    _rec_name = "shift"

    shift = fields.Selection(selection=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('Night', 'Night')])
    employee_ids = fields.One2many('employee.ept', 'shift_id', string="Employee")


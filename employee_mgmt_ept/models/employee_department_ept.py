from odoo import fields,models

class Department_Demo(models.Model):
    _name="employee.department.ept"
    _description="Employee Management System Demo"

    name=fields.Char(string="Department Name", required=True, help="Department field of department for Employee Management System")
    employee_ids = fields.One2many('employee.ept', 'department_id', string="Employee")
    manager_id = fields.Many2one('res.users', string="Manager", help="Manager data will be come from Users model")
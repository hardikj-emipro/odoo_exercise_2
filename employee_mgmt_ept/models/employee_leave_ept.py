from odoo import models,fields

class Employee_Leave(models.Model):
    _name="employee.leave.ept"
    _description="Employee Management System Demo"
    _rec_name="employee_id"

    employee_id = fields.Many2one('employee.ept', string="Employee", help="Employee name load from employee model")
    department_id = fields.Many2one('employee.department.ept', related="employee_id.department_id", store=False, string="Department", help="Department name load from department model")
    start_date = fields.Date(string="From Date", help="Leave start from date")
    end_date = fields.Date(string="To Date", help="Leave end to date")
    status = fields.Selection(selection=[('Draft', 'Draft'), ('Approved', 'Approved'), ('Refused', 'Refused'),
                                         ('Cancelled', 'Cancelled')], default='Draft')
    leave_description=fields.Text(string="Reason", required=True, help="leave description field")
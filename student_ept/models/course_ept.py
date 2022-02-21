from odoo import models,fields

class Course_Demo(models.Model):
    _name="course.ept"
    _description="Student & Course Demo Many 2 Many Relation Ship Concept"

    name=fields.Char(string="Course Name", help="Course Name for student model")
    student_ids=fields.Many2many('res.student.ept', string="Student Info", help="Many to many relation ship concept with student")

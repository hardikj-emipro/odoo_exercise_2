from odoo import models,fields

class Student_Demo(models.Model):
    _name="res.student.ept"
    _description="Student Ept"

    name=fields.Char(string="Student Name", help="Student Name Filed of Student EPT Module")
    class_name=fields.Char(string="Class", help="Class Field of Student EPT Module")
    date_of_birth=fields.Date(string="Date of Birth", help="Date of birth of Student")
    course_ids=fields.Many2many('course.ept', string="Course", help="Many to many relation ship concept with course")
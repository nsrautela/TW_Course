from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    course_id = fields.Many2one('course.info', string="Course")
    instructor_id = fields.Many2one('instructor.info', string="Instructor")
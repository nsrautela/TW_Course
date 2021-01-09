from odoo import api, fields, models, _

class InstructorInfo(models.Model):
    _name = 'instructor.info'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True, copy=False)

class CourseInfo(models.Model):
    _name = 'course.info'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True, copy=False)
    date = fields.Datetime('Date', default=fields.Datetime.now, readonly=1)
    instructor_id = fields.Many2one('instructor.info', 'Instructor', required=True, track_visibility='onchange')
    rooms_id = fields.Many2one('rooms.info', 'Rooms', required=True, track_visibility='onchange')
    lessons_ids = fields.Many2many('lessons.info', string='Lessons', required=True)
    attendees_lines = fields.One2many('attendees.lines', 'course_id', string='Attendees')

    @api.onchange('rooms_id')
    def onchange_warehouse_id(self):
        lines = []
        if self.rooms_id:
            self.lessons_ids = [(6, 0, [x.id for x in self.rooms_id.lessons_ids])]
            # lines
            for line in self.rooms_id.attendees_lines:
                lines.append(line.id)
            self.attendees_lines = lines

class AttendeesLine(models.Model):
    _name = "attendees.lines"

    rooms_id = fields.Many2one('rooms.info', string="Rooms")
    course_id = fields.Many2one('course.info', string="Course")
    attendees_name_id = fields.Many2one('res.partner', string="Name")







from odoo import api, fields, models, _
from odoo.exceptions import UserError

class LessonsInfo(models.Model):
    _name = 'lessons.info'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True, copy=False)

class LocationsInfo(models.Model):
    _name = 'locations.info'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True, copy=False)
    lessons_ids = fields.Many2many('lessons.info', string='Lessons', required=True)

class RoomsInfo(models.Model):
    _name = 'rooms.info'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char(string='Name', required=True, copy=False, track_visibility='onchange')
    date = fields.Datetime('Date', default=fields.Datetime.now, readonly=1)
    locations_id = fields.Many2one('locations.info', 'Locations', required=True, track_visibility='onchange')
    lessons_ids = fields.Many2many('lessons.info', string='Lessons', required=True)
    attendees_lines = fields.One2many('attendees.lines', 'rooms_id', string='Attendees')
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('cancel', 'Cancel')], string="State", default="draft", track_visibility='onchange')

    def _check_attendees_lines(self):
        for rec in self:
            attendees_len = len(rec.attendees_lines)
            if attendees_len >25 :
                return False
        return True

    _constraints = [(_check_attendees_lines,_('Warning:\n Please Carefull, Attendees should not be exceed more then 25.'),['attendees_lines']), ]

    @api.multi
    def unlink(self):
        for rec in self:
            if not rec.state == 'draft':
                raise UserError(_('You can only delete records that are in Draft State.'))
            return super(RoomsInfo, self).unlink()

    @api.multi
    def button_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    @api.multi
    def button_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.onchange('locations_id')
    def onchange_warehouse_id(self):
        if self.locations_id:
            self.lessons_ids = [(6, 0, [x.id for x in self.locations_id.lessons_ids])]







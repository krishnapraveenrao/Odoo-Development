from odoo import fields, models


class QualityAction(models.Model):
    _name = "quality.action"
    _description = "Corrective Action"

    name = fields.Char(
        string="Action Required",
        required=True,
    )

    nc_id = fields.Many2one(
        "quality.nc",
        string="Non-Conformance",
        required=True,
        ondelete="cascade",
    )

    owner_id = fields.Many2one(
        "res.users",
        string="Action Owner",
    )

    target_date = fields.Date(
        string="Target Date",
    )

    is_complete = fields.Boolean(
        string="Complete",
    )

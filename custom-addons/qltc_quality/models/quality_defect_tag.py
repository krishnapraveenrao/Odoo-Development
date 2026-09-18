from odoo import fields, models


class QualityDefectTag(models.Model):
    _name = "quality.defect.tag"
    _description = "Defect Category"

    name = fields.Char(
        string="Defect Type",
        required=True,
    )

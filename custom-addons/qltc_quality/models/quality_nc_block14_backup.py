from odoo import api, fields, models
from odoo.exceptions import ValidationError


class QualityNC(models.Model):
    _name = "quality.nc"
    _description = "Supplier Non-Conformance"

    name = fields.Char(
        string="Reference",
        default="New",
        required=True,
        copy=False,
        readonly=True,
    )

    supplier_id = fields.Many2one(
        "res.partner",
        string="Supplier",
        required=True,
    )

    responsible_id = fields.Many2one(
        "res.users",
        string="Responsible",
        default=lambda self: self.env.user,
    )

    part_number = fields.Char(
        string="Part Number",
    )

    defect_tag_ids = fields.Many2many(
        "quality.defect.tag",
        string="Defect Types",
    )

    defect_description = fields.Text(
        string="Defect Found",
    )

    quantity_affected = fields.Float(
        string="Quantity Affected",
    )

    cost_impact = fields.Float(
        string="Estimated Cost Impact",
    )

    raise_date = fields.Date(
        string="Date Raised",
        default=fields.Date.today,
    )

    due_date = fields.Date(
        string="Action Due",
    )

    is_repeat = fields.Boolean(
        string="Repeat Occurrence",
    )

    severity = fields.Selection(
        [
            ("minor", "Minor"),
            ("major", "Major"),
            ("critical", "Critical"),
        ],
        string="Severity",
        default="minor",
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("investigating", "Under Investigation"),
            ("action", "Action Assigned"),
            ("closed", "Closed"),
        ],
        string="Status",
        default="draft",
    )

    action_ids = fields.One2many(
        "quality.action",
        "nc_id",
        string="Corrective Actions",
    )

    action_count = fields.Integer(
        string="Actions",
        compute="_compute_action_counts",
        store=True,
    )

    open_action_count = fields.Integer(
        string="Open Actions",
        compute="_compute_action_counts",
        store=True,
    )

    is_overdue = fields.Boolean(
        string="Overdue",
        compute="_compute_is_overdue",
    )

    @api.depends("action_ids", "action_ids.is_complete")
    def _compute_action_counts(self):
        for record in self:
            record.action_count = len(record.action_ids)
            record.open_action_count = len(
                record.action_ids.filtered(
                    lambda action: not action.is_complete
                )
            )

    @api.depends("due_date", "state")
    def _compute_is_overdue(self):
        today = fields.Date.today()

        for record in self:
            record.is_overdue = bool(
                record.due_date
                and record.state != "closed"
                and record.due_date < today
            )

    @api.onchange("severity", "raise_date")
    def _onchange_severity(self):
        base_date = self.raise_date or fields.Date.today()

        if self.severity == "critical":
            self.due_date = fields.Date.add(base_date, days=3)
        elif self.severity == "major":
            self.due_date = fields.Date.add(base_date, days=7)
        elif self.severity == "minor":
            self.due_date = fields.Date.add(base_date, days=14)
        else:
            self.due_date = False

    @api.constrains("severity", "raise_date", "due_date")
    def _check_due_date(self):
        for record in self:
            if (
                record.raise_date
                and record.due_date
                and record.due_date < record.raise_date
            ):
                raise ValidationError(
                    "Action Due date cannot be earlier than Date Raised."
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.nc")
                    or "New"
                )

        return super().create(vals_list)



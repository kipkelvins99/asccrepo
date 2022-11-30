from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.team'

    branch_id = fields.Many2one("res.branch", string='Branch',
                                default=False, domain="[('company_id', '=', company_id)]"
                                # compute='_compute_branch'
                                )

    @api.depends('company_id')
    def _compute_branch(self):
        company = self.company_id
        branch_ids = self.env.user.branch_ids

        branch = branch_ids.filtered(
            lambda branch: branch.company_id == company)

        print(branch.ids, branch_ids, company,'branch.ids[0]')
        if branch:
            self.branch_id = branch.ids[0]
        else:
            self.branch_id = False
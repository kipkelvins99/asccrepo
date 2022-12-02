from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    agent_id = fields.Many2one('res.partner', 'Agent', domain="[('is_agent', '=', True)]")
    product_id = fields.Many2one('product.product', 'Product')
    branch_id = fields.Many2one("res.branch", string='Branch',
                                default=False,
                                # domain="[('company_id', '=', company_id)]"
                                # compute="_compute_branch"
                                )
    team_id = fields.Many2one(
        'crm.team', string='Sales Team', check_company=True, index=True, tracking=True,
        domain="[('branch_id', '=', branch_id)]",
        ondelete="set null", readonly=False, default=False)
    user_id = fields.Many2one(
        'res.users', string='Salesperson',
        domain="['&', ('branch_id', '=', branch_id), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True, default=False)

    @api.onchange('agent_id')
    def onchange_agent(self):
        self.agent_id.is_agent = True

    # @api.onchange('branch_id')
    # def onchange_branch_id(self):
    #     s
    #     print(self.user_id, self.team_id, 'oooo')

    @api.depends('company_id')
    def _compute_branch(self):
        company = self.company_id
        branch_ids = self.env.user.branch_ids
        branch = branch_ids.filtered(
            lambda branch: branch.company_id == company)
        if branch:
            self.branch_id = branch.ids[0]
        else:
            self.branch_id = False

    def _compute_team_id(self):
        res = super(Lead, self)._compute_team_id()
        print(res, 'yesss')
        return res
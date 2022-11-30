from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    agent_id = fields.Many2one('res.partner', 'Agent', domain="[('is_agent', '=', True)]")
    product_id = fields.Many2one('product.product', 'Product')
    branch_id = fields.Many2one("res.branch", string='Branch',
                                default=False, domain="[('company_id', '=', company_id)]"
                                # compute="_compute_branch"
                                )
    team_id = fields.Many2one(
        'crm.team', string='Sales Team', check_company=True, index=True, tracking=True,
        domain="[('branch_id', '=', branch_id), ('company_id', '=', company_id)]",
        ondelete="set null", readonly=False, default=False)
    user_id = fields.Many2one(
        'res.users', string='Salesperson',
        domain="['&', ('branch_id', '=', branch_id), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True, default=False)

    @api.onchange('agent_id')
    def onchange_agent(self):
        self.agent_id.is_agent = True

    # @api.depends('user_id', 'type')
    # def _compute_team_id(self):
    #     """ When changing the user, also set a team_id or restrict team id
    #     to the ones user_id is member of. """
    #     for lead in self:
    #         # setting user as void should not trigger a new team computation
    #         if not lead.user_id:
    #             continue
    #         user = lead.user_id
    #         if lead.team_id and user in (lead.team_id.member_ids | lead.team_id.user_id):
    #             continue
    #         team_domain = [('use_leads', '=', True)] if lead.type == 'lead' else [('use_opportunities', '=', True)]
    #         team = self.env['crm.team']._get_default_team_id(user_id=user.id, domain=team_domain)
    #         lead.team_id = team.id
    #         print('yesss')
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
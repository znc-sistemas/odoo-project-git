from openerp import fields, models


class ProjectGit(models.Model):

    _inherit = "res.users"

    git_username = fields.Char("GIT Username", size=50)

ProjectGit()

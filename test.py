"""
This module contains the action_confirm method for sale orders.
"""

import logging
from odoo import _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def action_confirm(self):
    """
    Confirm draft and sent sale orders for partners associated with the current records.
    """
    if not self:
        return True

    partners = self.mapped("partner_id")
    if not partners:
        raise UserError(_("No associated partners found. Please select records with valid partners."))

    draft_orders = self.env["sale.order"].search(
        [("partner_id", "in", partners.ids), ("state", "in", ["draft", "sent"])]
    )

    if not draft_orders:
        raise UserError(_("No unconfirmed sale orders found for the associated partners."))

    draft_orders.action_confirm()
    _logger.info("Confirmed %s sale orders.", len(draft_orders))

    return True

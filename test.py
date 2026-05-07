"""
This module contains the action_confirm method for sale orders.
"""

import logging
from odoo import _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def action_confirm(self):
    """
    Confirm draft sale orders for partners associated with the current records.
    """
    if not self:
        return True

    partners = self.mapped("partner_id")
    if not partners:
        raise UserError(_("No associated partners found."))

    draft_orders = self.env["sale.order"].search(
        [("partner_id", "in", partners.ids), ("state", "=", "draft")]
    )

    if not draft_orders:
        raise UserError(_("No draft sale orders found for the associated partners."))

    draft_orders.action_confirm()
    order_names = draft_orders.filtered("name").mapped("name")
    _logger.info("Confirmed sale orders: %s", ", ".join(order_names))

    return True

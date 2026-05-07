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

    # Validate that all records have an associated partner
    records_without_partner = self.filtered(lambda r: not r.partner_id)
    if records_without_partner:
        raise UserError(_("All selected records must have an associated partner."))

    partners = self.mapped("partner_id")
    if not partners:
        raise UserError(_("No valid partners found for the selected records."))

    draft_orders = self.env["sale.order"].search([
        ("partner_id", "in", partners.ids),
        ("state", "in", ["draft", "sent"])
    ])

    if not draft_orders:
        raise UserError(_("No unconfirmed sale orders found for the associated partners."))

    draft_orders.action_confirm()

    _logger.info("Successfully confirmed %d sale order(s) for %d partner(s).", len(draft_orders), len(partners))

    return True

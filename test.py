"""
This module contains the action_confirm method for sale orders.
"""

import logging

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """
        Confirm draft and sent sale orders for partners associated with the current records.
        """
        if not self:
            return True

        invalid_state_orders = self.filtered_domain([('state', 'not in', ['draft', 'sent'])])
        if invalid_state_orders:
            raise UserError(_("Only draft and sent orders can be confirmed."))

        skip_related = self.env.context.get('skip_related_confirmation')
        partners = False

        if not skip_related:
            # Validate that all records have an associated partner
            # Use filtered_domain instead of filtered lambda for better performance
            orders_without_partner = self.filtered_domain([('partner_id', '=', False)])
            if orders_without_partner:
                raise UserError(_("All selected records must have an associated partner."))

            partners = self.mapped('partner_id')

        res = super().action_confirm()

        if partners:
            self._confirm_related_orders(partners)

        return res

    def _confirm_related_orders(self, partners):
        """
        Confirm related draft and sent sale orders for the given partners.
        """
        # Fetch unconfirmed sale orders for these partners
        # Excluding 'self' to avoid an infinite recursion loop
        related_orders = self.search([
            ('partner_id', 'in', partners.ids),
            ('state', 'in', ['draft', 'sent']),
            ('id', 'not in', self.ids)
        ])

        if related_orders:
            # Confirm the other orders found
            related_orders.with_context(skip_related_confirmation=True).action_confirm()
            _logger.info(
                "Successfully confirmed %d additional sale order(s) for %d partner(s).",
                len(related_orders),
                len(partners)
            )

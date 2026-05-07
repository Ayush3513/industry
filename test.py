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

        res = super().action_confirm()

        if not self.env.context.get('skip_related_confirmation'):
            # Validate that all records have an associated partner
            # Use filtered_domain instead of filtered lambda for better performance
            records_without_partner = self.filtered_domain([('partner_id', '=', False)])
            if records_without_partner:
                raise UserError(_("All selected records must have an associated partner."))

            partners = self.mapped('partner_id')

            # Fetch unconfirmed sale orders for these partners
            # Excluding 'self' to avoid an infinite recursion loop
            orders_to_confirm = self.env['sale.order'].search([
                ('partner_id', 'in', partners.ids),
                ('state', 'in', ['draft', 'sent']),
                ('id', 'not in', self.ids)
            ])

            if orders_to_confirm:
                # Confirm the other orders found
                orders_to_confirm.with_context(skip_related_confirmation=True).action_confirm()
                _logger.info(
                    "Successfully confirmed %d additional sale order(s) for %d partner(s).",
                    len(orders_to_confirm),
                    len(partners)
                )

        return res

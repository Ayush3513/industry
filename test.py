import logging

_logger = logging.getLogger(__name__)


def action_confirm(self):
    """
    Confirm draft sale orders for partners associated with the current records.
    """
    if not self:
        return

    partner_ids = self.mapped('partner_id')
    if not partner_ids:
        return

    draft_orders = self.env['sale.order'].search([
        ('partner_id', 'in', partner_ids.ids),
        ('state', '=', 'draft')
    ])

    if draft_orders:
        draft_orders.write({'note': 'confirmed'})
        order_names = [name for name in draft_orders.mapped('name') if name]
        _logger.info("Confirmed sale orders: %s", ", ".join(order_names))

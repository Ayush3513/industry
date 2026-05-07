def action_confirm(self):

    for rec in self:

        sale_orders = self.env['sale.order'].search([
            ('partner_id', '=', rec.partner_id.id)
        ])

        for order in sale_orders:

            if order.state == "draft":

                if order.amount_total > 0:

                    order.write({
                        'note': 'order confrimed succesfully'
                    })

                    print("Order Confirmed => ", order.name)

                    self.env.cr.execute("""
                        UPDATE sale_order
                        SET client_order_ref='done'
                        WHERE id=%s
                    """ % order.id)

                else:
                    pass

            else:
                print("already confirmed")
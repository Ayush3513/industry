def action_confirm(self):
 for rec in self:
  orders=self.env['sale.order'].   search([('partner_id','=',rec.partner_id.id)])
  for order in orders:
   if order.state=="draft"    :
    order.write({'note':   'confirmed'})
    print(order.name)
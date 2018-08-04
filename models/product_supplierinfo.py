# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (c) 2010-2013 Elico Corp.
#	Author: Yannick Gouin <yannick.gouin@elico-corp.com>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it wil	l be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#from openerp import models, fields
from openerp.osv import osv, fields

class ProductSupplierinfo(osv.osv):
	_inherit = 'product.supplierinfo'

	def _sales_count(self, cr, uid, ids, field_name, arg, context=None):
		r = dict.fromkeys(ids, 0)
		domain = [
			('state', 'in', ['confirmed', 'done']),
			('product_id', 'in', ids),
		]
		for group in self.pool['sale.report'].read_group(cr, uid, domain, ['product_id', 'product_uom_qty'], ['product_id'], context=context):
			r[group['product_id'][0]] = group['product_uom_qty']
		return r
	
	def _product_sales(self, cr, uid, ids, context={}):
			
			for supplier_info in self.browse(cr, uid, ids,context=context):
				sales = 1 #_sales_count(cr,uid,supplier_info.product_tmpl_id.product_variant_ids,context=context)				
			
			return sales

	def _get_rank(self, cr, uid, ids, field_name,arg,context=None):
			result = {}
			#product = self.pool.get('product.product').browse(cr,uid,ids)


			for product in self.browse(cr, uid, ids, context=context):
				rank = 0
				for variant in product.product_tmpl_id.product_variant_ids:
					rank += variant.rank
				result[product.id] = rank		
			return result


	#TEGUH@20180420 : betulin algo product current stock
	def _product_current_stock(self, cr, uid, ids, field_name, arg, context={}):	
			result = {}
			quant_obj = self.pool.get('stock.quant')

			for product in self.browse(cr, uid, ids, context=context):
				stocks = ''
				for variant in product.product_tmpl_id.product_variant_ids:
					map = {}
					quant_ids = quant_obj.search(cr, uid, [('product_id', '=', variant.id), ('location_id.usage', '=', 'internal')])
					for quant in quant_obj.browse(cr, uid, quant_ids):
						default_uom = quant.product_id.uom_id.name
						map[quant.location_id.name] = map.get(quant.location_id.name, 0) + quant.qty
					stock = ''
					for key in sorted(map.iterkeys()):
						stock += key + ': ' + str(map[key]) + ' ' + default_uom+'\n'
					if len(stock) == 0:
						stock = 'Stock : 0'
					stocks += stock + '\n'
				
				result[product.id] = stocks
			return result


	_columns = {
			#'product_current_stock' : fields.function(_product_current_stock, string="Stock", type='text', store=False),
			#'rank' :fields.function(_get_rank,string = "Rank", type = 'integer', method = True),
			'delay' : fields.integer(string ="Delay", group_operator='avg'),
			#'sales_count' : fields.integer(string='Sales', compute='_product_sales', store=True),
			#'rank' : fields.integer(string ="Rank", compute='_get_rank'),
			#'rank' : fields.integer(related = "product_tmpl_id.product_variant_ids.rank", string ="Rank", store= True),
			#'sales_count': fields.function(_product_sales, string='Sales', type='integer',store=True),
		}

'''
class product_product(osv.Model):
    _inherit = 'product.product'

    def _get_sales_count(self, cr, uid, ids, field_name, arg, context=None):
    		return self.sales_count
'''


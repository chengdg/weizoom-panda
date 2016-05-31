/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.datas:OrderDatasPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var OrderDatasPage = React.createClass({
	getInitialState: function() {
		return Store.getData();
	},

	onClickShip: function(event) {
		var productId = parseInt(event.target.getAttribute('data-product-id'));
		//Reactman.PageAction.showConfirm({
		//	target: event.target,
		//	title: '确认删除吗?',
		//	confirm: _.bind(function() {
		//		Action.deleteProduct(productId);
		//	}, this)
		//});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'name') {
			return (
				<a href={'/order/data/?id='+data.id}>{value}</a>
			)
		} else if (field === 'action') {
			return (
			<div>
				<a className="btn btn-link btn-xs" onClick={this.onClickShip} data-product-id={data.id}>发货</a>
			</div>
			);
		}else {
			return value;
		}
	},

	onConfirmFilter: function(data) {
		Action.filterOrders(data);
	},

	render:function(){
		var ordersResource = {
			resource: 'order.datas',
			data: {
				page: 1
			}
		};
		var typeOptions = [{
			text: '全部',
			value: -1
		}, {
			text: '待发货',
			value: '0'
		}, {
			text: '已发货',
			value: '1'
		}, {
			text: '已完成',
			value: '2'
		}];

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="订单编号:" name="order_id" match='~' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="订单状态:" name="status" options={typeOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormDateRangeInput label="下单时间:" name="order_create_at" match="[t]" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>

			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="批量发货" href="/order/data/" />
					<Reactman.TableActionButton text="导出" href="/order/data/" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={ordersResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
					<Reactman.TableColumn name="商品" field="product_name" />
					<Reactman.TableColumn name="单价/数量" field="product_price" />
					<Reactman.TableColumn name="收货人" field="ship_name" />
					<Reactman.TableColumn name="订单金额" field="total_purchase_price" />
					<Reactman.TableColumn name="订单状态" field="status" />
					<Reactman.TableColumn name="操作" field="action" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = OrderDatasPage;
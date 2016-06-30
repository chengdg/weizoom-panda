/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.yunying_orders_list:YunyingOrderDatasPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var YunyingOrderDatasPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	rowFormatter: function(field, value, data) {
		return value;
	},

	onConfirmFilter: function(data) {
		Action.filterOrders(data);
	},

	onExport: function(){
		Action.exportOrders();
	},

	render:function(){
		var ordersResource = {
			resource: 'order.yunying_orders_list',
			data: {
				page: 1,
				is_for_list: true
			}
		};
		var typeOptions = [{
			text: '全部',
			value: '-1'
		}, {
			text: '微众商城',
			value: '3394'
		}, {
			text: '微众家',
			value: '3621'
		}, {
			text: '微众妈妈',
			value: '3806'
		}, {
			text: '微众学生',
			value: '3807'
		}, {
			text: '微众白富美',
			value: '3808'
		}, {
			text: '微众俱乐部',
			value: '3936'
		}];

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="客户名称:" name="customer_name" match='=' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="商品名称:" name="product_name" match='=' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="来源商城:" name="from_mall" options={typeOptions} match="=" />
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
					<Reactman.TableActionButton text="导出发货文件" onClick={this.onExport}/>
				</Reactman.TableActionBar>
				<Reactman.Table resource={ordersResource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="订单编号" field="order_id" />
					<Reactman.TableColumn name="下单时间" field="order_create_at" />
					<Reactman.TableColumn name="订单金额" field="total_purchase_price" />
					<Reactman.TableColumn name="客户名称" field="customer_name" />
					<Reactman.TableColumn name="来源商城" field="from_mall" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = YunyingOrderDatasPage;
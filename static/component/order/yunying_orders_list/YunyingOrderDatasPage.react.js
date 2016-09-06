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

	componentDidMount: function () {
		Action.getAllSyncedSelfShops();
	},

	onChangeStore: function(event) {
		this.setState(Store.getData());
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	onConfirmFilter: function(data) {
		Action.filterOrders(data);
	},

	onExport: function(){
		Action.exportOrders();
	},
	rowFormatter: function(field, value, data) {
		if (field === 'orderId') {
			return (
				<div style={{textAlign:'left'}}>
					<a href={'/order/customer_order_detail/?id='+data.orderId} target="_blank">{data.orderId}</a>
				</div>
			)
		}else {
			return value;
		}
	},
	render:function(){
		var ordersResource = {
			resource: 'order.yunying_orders_list',
			data: {
				page: 1,
				is_for_list: true
			}
		};
		var orderStatusOptions = [{
			text: '全部',
			value: '-1'
		}, {
			text: '待发货',
			value: '3'
		}, {
			text: '已发货',
			value: '4'
		}, {
			text: '已完成',
			value: '5'
		}, {
			text: '退款中',
			value: '6'
		}, {
			text: '退款完成',
			value: '7'
		}, {
			text: '已取消',
			value: '1'
		}];
		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="客户名称:" name="customerName" match='=' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="商品名称:" name="productName" match='=' />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormInput label="订单号:" name="orderId" match='=' />
					</Reactman.FilterField>
				</Reactman.FilterRow>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormDateRangeInput label="下单时间:" name="orderCreateAt" match="[t]" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="来源商城:" name="fromMall" options={this.state.typeOptions} match="=" />
					</Reactman.FilterField>
					<Reactman.FilterField>
						<Reactman.FormSelect label="订单状态:" name="orderStatus" options={orderStatusOptions} match="=" />
					</Reactman.FilterField>
				</Reactman.FilterRow>
			</Reactman.FilterPanel>

			<Reactman.TablePanel>
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="导出发货文件" onClick={this.onExport}/>
				</Reactman.TableActionBar>
				<Reactman.Table resource={ordersResource} formatter={this.rowFormatter} pagination={true} ref="table">
					<Reactman.TableColumn name="订单编号" field="orderId" />
					<Reactman.TableColumn name="商品名称" field="productName" />
					<Reactman.TableColumn name="订单金额" field="totalPurchasePrice" />
					<Reactman.TableColumn name="运费" field="postage" />
					<Reactman.TableColumn name="订单状态" field="orderStatus" />
					<Reactman.TableColumn name="客户名称" field="customerName" />
					<Reactman.TableColumn name="来源商城" field="fromMall" />
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = YunyingOrderDatasPage;
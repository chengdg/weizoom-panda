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
		var typeOptions = [{
			text: '全部',
			value: '-1'
		}, {
			text: '微众商城',
			value: 'weizoom_shop'
		}, {
			text: '微众家',
			value: 'weizoom_jia'
		}, {
			text: '微众妈妈',
			value: 'weizoom_mama'
		}, {
			text: '微众学生',
			value: 'weizoom_xuesheng'
		}, {
			text: '微众白富美',
			value: 'weizoom_baifumei'
		}, {
			text: '微众俱乐部',
			value: 'weizoom_club'
		}, {
			text: '微众Life',
			value: 'weizoom_life'
		}, {
			text: '微众一家人',
			value: 'weizoom_yjr'
		}, {
			text: '惠惠来啦',
			value: 'weizoom_fulilaile'
		}, {
			text: '居委汇',
			value: 'weizoom_juweihui'
		}, {
			text: '微众中海',
			value: 'weizoom_zhonghai'
		}, {
			text: '微众club',
			value: 'weizoom_zoomjulebu'
		}, {
			text: '微众吃货',
			value: 'weizoom_chh'
		}, {
			text: '微众圈',
			value: 'weizoom_pengyouquan'
		}, {
			text: '少先队',
			value: 'weizoom_shxd'
		}, {
			text: '津美汇',
			value: 'weizoom_jinmeihui'
		}, {
			text: '微众便利店',
			value: 'weizoom_wzbld'
		}, {
			text: '微众佳人',
			value: 'weizoom_jiaren'
		}, {
			text: '微众良乡商城',
			value: 'weizoom_xiaoyuan'
		}, {
			text: '微众精英',
			value: 'weizoom_jy'
		}, {
			text: '爱尔康',
			value: 'weizoom_aierkang'
		}];
		if(W.is_ceshi){
			typeOptions.push({
				text: '开发测试',
				value: 'devceshi'
			});
			typeOptions.push({
				text: '财务测试',
				value: 'caiwuceshi'
			});
		}
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
						<Reactman.FormSelect label="来源商城:" name="fromMall" options={typeOptions} match="=" />
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
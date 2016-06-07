/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_orders_list:OrderDatasPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var ShipDialog = require('./ShipDialog.react');
require('./style.css')

var OrderDatasPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onClickShip: function(event) {
		var orderId = parseInt(event.target.getAttribute('data-order-id'));
		var order = this.refs.table.getData(orderId);
		Reactman.PageAction.showDialog({
			title: "发货信息",
			component: ShipDialog,
			data: {
				order: order
			},
			success: function(inputData, dialogState) {
				var order = inputData.order;
				console.log(dialogState);
				//var comment = dialogState.comment;
				//Action.updateProduct(product, 'comment', comment);
			}
		});
	},
	onChangeStore: function(event) {
		var filterOptions = Store.getData().filterOptions;
		this.refs.table.refresh(filterOptions);
	},

	getOrderProductsInfo: function(value,data){
		var _this = this;
		var product_infos = JSON.parse(data['product_infos']);
		var product_items = product_infos.map(function(product,index){
			if (value == 'product_name'){
				return (
					<span key={index}><img src={product["product_img"]} width="60px" height="60px"></img>{product["product_name"]}<br></br></span>
				)
			}else if (value == 'product_price'){
				return (
					<div key={index} style={{paddingLeft:'10px'}}>
						<div>{product['purchase_price']}</div>
						<div>({product['count']}件)</div>
					</div>
				)
			}
		})
		return product_items;
	},

	rowFormatter: function(field, value, data) {
		if (field === 'product_price') {
			var product_price = this.getOrderProductsInfo('product_price',data);
			return (
				<div>{product_price}</div>
			);
		}else if (field === 'action') {
			if(data.status === '待发货'){
				return (
					<div>
						<a className="btn btn-link btn-xs" onClick={this.onClickShip} data-order-id={data.order_id}>发货</a>
					</div>
				);
			}else if(data.status === '已发货'){
				return (
					<div className="orders-list-btn-group">
						<a className="btn btn-link btn-xs" onClick={this.onClickComplete} data-order-id={data.order_id}>标记完成</a>
						<a className="btn btn-link btn-xs" onClick={this.onClickChangeShip} data-order-id={data.order_id}>修改物流</a>
					</div>
				);
			}else{
				return value;
			}
		}else if (field === 'expand-row') {
			return (
				<div style={{textAlign:'left', padding:'5px'}}>
					<span>订单编号: <a href={'/order/customer_order_detail/?id='+data.order_id}>{data.order_id}</a></span>
					<span style={{paddingLeft:'100px'}}>下单时间: {data.order_create_at}</span>
				</div>
			)
		}else if (field === 'product_name') {
			var product_name = this.getOrderProductsInfo('product_name',data);
			return (
				<div>
					{product_name}
				</div>
			);
		} else {
			return value;
		}
	},

	onConfirmFilter: function(data) {
		Action.filterOrders(data);
	},

	render:function(){
		var ordersResource = {
			resource: 'order.customer_orders_list',
			data: {
				page: 1
			}
		};
		var typeOptions = [{
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
		}];

		return (
		<div className="mt15 xui-outline-datasPage">
			<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
				<Reactman.FilterRow>
					<Reactman.FilterField>
						<Reactman.FormInput label="订单编号:" name="order_id" match='=' />
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
					<Reactman.TableActionButton text="批量发货" />
					<Reactman.TableActionButton text="导出" />
				</Reactman.TableActionBar>
				<Reactman.Table resource={ordersResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
					<Reactman.TableColumn name="商品" field="product_name" />
					<Reactman.TableColumn name="单价/数量" field="product_price" />
					<Reactman.TableColumn name="收货人" field="ship_name" />
					<Reactman.TableColumn name="订单金额" field="total_purchase_price" />
					<Reactman.TableColumn name="订单状态" field="status" />
					<Reactman.TableColumn name="操作" field="action" width='60px'/>
				</Reactman.Table>
			</Reactman.TablePanel>
		</div>
		)
	}
})
module.exports = OrderDatasPage;
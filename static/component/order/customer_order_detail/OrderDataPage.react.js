/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_order_detail:OrderDataPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Store = require('./Store');
var Action = require('./Action');
var OrderLogistics = require('./OrderLogistics.react');
require('./style.css')

var OrderDataPage = React.createClass({
	getOrderProductsInfo: function(value,data){
		var _this = this;
		var products = JSON.parse(data['products']);
		var product_items = products.map(function(product,index){
			if (value == 'product_name'){
				return (
					<span className="product-item-info" key={index}>{product["product_name"]}<br></br></span>
				)
			}else if (value == 'unit_price/quantity'){
				return (
					<span key={index} className="product-item-info">{product["purchase_price"]}/({product["count"]}件)<br></br></span>
				)
			}
		})
		return product_items;
	},

	rowFormatter: function(field, value, data) {
		if(field === 'product_name'){
			var product = this.getOrderProductsInfo('product_name',data);
			return (
				<div>{product}</div>
			);
		}else if(field === 'unit_price/quantity'){
			var product = this.getOrderProductsInfo('unit_price/quantity',data);
			return (
				<div>{product}</div>
			);
		}else if(field === 'total_count'){
			return (
				<div style={{margin:'10px 0 0 10px'}}>{value}</div>
			);
		}else if(field === 'order_money'){
			Action.saveProduct(data);
			return (
				<div style={{margin:'10px 0 0 10px'}}>{value}</div>
			);
		}else {
			return value;
		}
	},

	render:function(){
		var order_id = W.order_id;
		var productsResource = {
			resource: 'order.customer_order_detail',
			data: {
				page: 1,
				order_id: order_id
			}
		};

		return (
			<div>
				<OrderStatus />
				<OrderLogistics />
				<div className="mt15 xui-product-productListPage">
					<Reactman.TablePanel>
						<Reactman.TableActionBar>
						</Reactman.TableActionBar>
						<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
							<Reactman.TableColumn name="商品" field="product_name" />
							<Reactman.TableColumn name="单价/数量" field="unit_price/quantity" />
							<Reactman.TableColumn name="商品件数" field="total_count" width='200px'/>
							<Reactman.TableColumn name="订单金额" field="order_money" width='200px'/>
						</Reactman.Table>
					</Reactman.TablePanel>
				</div>
			</div>
		)
	}
})

var OrderStatus = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			orde_datas: {}
		}
	},

	onChangeStore: function(event) {
		var orde_datas = Store.getData();
		this.setState({
			orde_datas: orde_datas
		})
	},

	render:function(){
		var orde_datas = this.state.orde_datas;
		var order_id = orde_datas['order_id']? orde_datas['order_id']: '';
		var order_status = orde_datas['order_status'];
		return (
			<div style={{background:'#FFF',marginTop:'10px', border:'1px solid #CCC',fontSize:'16px',height:'100px'}}>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span>订单编号:{order_id}</span>
					</div>
					<div style={{marginTop:'10px'}}>
						<span>订单状态:{order_status}</span>
					</div>
					<div style={{margin:'0 auto',width:'200px'}}>
						<button type="button" className="btn btn-primary" style={{width:'100px'}}>发货</button>
					</div>
				</div>
			</div>
		)
	}
})
module.exports = OrderDataPage;
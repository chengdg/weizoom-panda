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

var OutlineDataPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		debug(Store.getData());
		return Store.getData();
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		debug(value);
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	rowFormatter: function(field, value, data) {
		if(field === 'unit_price/quantity'){
			return(
				<span>{data["unit_price"]}/({data["quantity"]})</span>
			)
		} else {
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
							<Reactman.TableColumn name="商品件数" field="total_count" />
							<Reactman.TableColumn name="订单金额" field="order_money" />
						</Reactman.Table>
					</Reactman.TablePanel>
				</div>
			</div>
		)
	}
})

var OrderStatus = React.createClass({
	render:function(){
		return (
			<div style={{background:'#FFF',marginTop:'10px', border:'1px solid #CCC',fontSize:'16px',height:'100px'}}>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span>订单编号:20160427170520421</span>
					</div>
					<div style={{marginTop:'10px'}}>
						<span>订单状态:待发货</span>
					</div>
					<div style={{margin:'0 auto',width:'200px'}}>
						<button type="button" className="btn btn-primary" style={{width:'100px'}}>发货</button>
					</div>
				</div>
			</div>
		)
	}
})

var OrderLogistics = React.createClass({
	render:function(){
		return (
			<div style={{marginTop:'10px',fontSize:'16px',background:'#FFF',border:'1px solid #CCC'}}>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span className="inline-block">收货人:某某某</span>
						<span className="inline-block" style={{marginLeft:'130px'}}>收货人电话:13900000000</span>
					</div>
					<div>
						<span>买家留言:xxxxxxxxxxx</span>
					</div>
					<div style={{borderBottom: '1px solid #ECE9E9'}}>
						<span>收货地址:江苏省南京市秦淮区夫子庙</span>
					</div>
				</div>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span>物流公司名称:申通快递</span>
					</div>
					<div style={{marginBottom: '20px'}}>
						<span>运单号:20165456895786</span>
					</div>
					<div>
						<span>2015-05-26 22:11:28 由广东潮阳公司 发往 广东揭阳中转部</span>
					</div>
					<div>
						<span>2015-06-30 23:11:12 广东深圳罗湖中转部 正在进行 发包 扫描 </span>
					</div>
				</div>
			</div>
		)
	}
})
module.exports = OutlineDataPage;
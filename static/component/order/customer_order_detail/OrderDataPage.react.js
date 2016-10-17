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
var OrderProduct = require('./OrderProduct.react');
require('./style.css')

var OrderDataPage = React.createClass({
	getInitialState: function() {	
		return {
			orde_datas: Store.getData()
		}
	},

	render:function(){
		var orde_datas = this.state.orde_datas;
		return (
			<div>
				<OrderStatus ordeDatas={orde_datas}/>
				<OrderLogistics ordeDatas={orde_datas}/>
				<OrderProduct ordeDatas={orde_datas}/>
			</div>
		)
	}
})

var OrderStatus = React.createClass({
	render:function(){
		var orde_datas = this.props.ordeDatas;
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
					
				</div>
			</div>
		)
	}
})
module.exports = OrderDataPage;
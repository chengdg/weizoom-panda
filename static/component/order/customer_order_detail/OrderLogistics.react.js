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
require('./style.css')

var OrderLogistics = React.createClass({
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
		var ship_name = orde_datas['ship_name']?orde_datas['ship_name']:'';
		var ship_tel = orde_datas['ship_tel']?orde_datas['ship_tel']:'';
		var customer_message = orde_datas['customer_message']?orde_datas['customer_message']:'';
		var ship_address = orde_datas['ship_address']?orde_datas['ship_address']:'';
		var express_company_name = orde_datas['express_company_name']?orde_datas['express_company_name']:'';
		var express_number = orde_datas['express_number']?orde_datas['express_number']:'';
		var order_express_details = orde_datas['order_express_details']?orde_datas['order_express_details']:[];
		return (
			<div style={{marginTop:'10px',fontSize:'16px',background:'#FFF',border:'1px solid #CCC'}}>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span className="inline-block">收货人:{ship_name}</span>
						<span className="inline-block" style={{marginLeft:'130px'}}>收货人电话:{ship_tel}</span>
					</div>
					<div>
						<span>买家留言:{customer_message}</span>
					</div>
					<div style={{borderBottom: '1px solid #ECE9E9'}}>
						<span>收货地址:{ship_address}</span>
					</div>
				</div>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span>物流公司名称:{express_company_name}</span>
					</div>
					<div style={{marginBottom: '20px'}}>
						<span>运单号:{express_number}</span>
					</div>
					<ExpressMessage orderExpress={order_express_details}/>
				</div>
			</div>
		)
	}
})

var ExpressMessage = React.createClass({
	render:function(){
		var order_express_details = this.props.orderExpress.length>0?this.props.orderExpress:'';
		if(order_express_details){
			var order_express = JSON.parse(order_express_details).map(function(order_expres,index){
				<div key={index}>
					<span>order_expres['time'] order_expres['context']</span>
				</div>
			})
			return (
				<div>
					{order_express}
				</div>
			)
		}else{
			return(
				<div></div>
			)
		}
		
	}
})
module.exports = OrderLogistics;
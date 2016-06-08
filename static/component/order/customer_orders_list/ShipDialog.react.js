/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_orders_list:ShipDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var ShipDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var order_id = this.props.data.order_id;
		console.log(order_id);
		return {
			order_id: order_id
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState({
			ship_company: infomations['ship_company'],
			ship_number: infomations['ship_number'],
			shiper_name: infomations['shiper_name']
		})
	},

	onBeforeCloseDialog: function() {
		if (this.state.ship_company === '-1') {
			Reactman.PageAction.showHint('error', '请选择物流公司');
		} else {
			var order = this.props.data.order;
			console.log('this.state');
			console.log(this.state);
			//TODO 给接口传递发货的参数
			//Reactman.Resource.post({
			//	resource: 'outline.data_comment',
			//	data: {
			//		product_id: product.id,
			//		comment: this.state.comment
			//	},
			//	success: function() {
			//		this.closeDialog();
			//	},
			//	error: function() {
			//		Reactman.PageAction.showHint('error', '评论失败!');
			//	},
			//	scope: this
			//})
		}
	},

	render:function(){
		var options = [{
			text: '请选择物流公司',
			value: '-1'
		}, {
			text: '申通快递',
			value: '申通快递'
		},{
			text: 'EMS',
			value: 'EMS'
		},{
			text: '顺丰速运',
			value: '顺丰速运'
		},{
			text: '圆通速递',
			value: '圆通速递'
		},{
			text: '中通速递',
			value: '中通速递'
		},{
			text: '天天快递',
			value: '天天快递'
		},{
			text: '韵达快运',
			value: '韵达快运'
		},{
			text: '百世快递',
			value: '百世快递'
		},{
			text: '全峰快递',
			value: '全峰快递'
		},{
			text: '德邦物流',
			value: '德邦物流'
		},{
			text: '宅急送',
			value: '宅急送'
		},{
			text: '快捷速递',
			value: '快捷速递'
		},{
			text: '比利时邮政',
			value: '比利时邮政'
		},{
			text: '速尔快递',
			value: '速尔快递'
		},{
			text: '国通快递',
			value: '国通快递'
		},{
			text: '如风达',
			value: '如风达'
		},{
			text: '邮政包裹/平邮',
			value: '邮政包裹/平邮'
		}];
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormSelect label="物流公司:" name="ship_company" validate="require-notempty" value={this.state.ship_company} options={options} onChange={this.onChange}/>
					<Reactman.FormInput label="快递单号:"name="ship_number" validate="require-string" value={this.state.ship_number} onChange={this.onChange} />
					<Reactman.FormInput label="发货人:"name="shiper_name" placeholder="备注请用竖线隔开" value={this.state.shiper_name} onChange={this.onChange} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = ShipDialog;
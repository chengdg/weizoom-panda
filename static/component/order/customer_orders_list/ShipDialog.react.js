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
		var order = this.props.data.order;
		return {
			order: order
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		if (this.state.ship_company === '-1') {
			Reactman.PageAction.showHint('error', '请选择物流公司');
		} else {
			var order = this.props.data.order;
			console.log(this.state);
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
			value: '0'
		},{
			text: '圆通快递',
			value: '1'
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
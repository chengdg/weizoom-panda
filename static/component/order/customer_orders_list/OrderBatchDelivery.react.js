/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_orders_list:OrderBatchDelivery');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var OrderBatchDelivery = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {}
	},

	onChange: function(value, event) {
		debug(value);
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
		//var newState = {};
		//newState[property] = value;
		//this.setState(newState);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
		//var infomations = Store.getData();
		//console.log(infomations);
		//this.setState({
		//	ship_company: infomations['ship_company'],
		//	ship_number: infomations['ship_number'],
		//	shiper_name: infomations['shiper_name']
		//})
	},

	onBeforeCloseDialog: function() {
		console.log(this.state.documents);
		if (!this.state.documents) {
			Reactman.PageAction.showHint('error', '请上传文件');
		} else {
			console.log('this.state');
			console.log(this.state);
			//TODO 给接口传递批量发货的参数
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
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<p>请编辑发货表格，只保留三个字段：订单编号、物流公司、快递单号。</p>
				<fieldset>
					<Reactman.FormFileUploader label="文件:" name="documents" value={this.state.documents} onChange={this.onChange} max={1} />
					<p>文件格式规范：</p>
					<img src='/static/img/express_name.jpg'></img>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = OrderBatchDelivery;
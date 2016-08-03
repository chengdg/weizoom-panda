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
		return Store.getData();
	},

	onChange: function(value, event) {
		debug(value);
		var property = event.target.getAttribute('name');
		Action.updateShip(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onBeforeCloseDialog: function() {
		if (!this.state.documents[0]) {
			Reactman.PageAction.showHint('error', '请上传文件');
		} else {
			console.log('================');
			console.log(this.state.documents[0].path);
			Reactman.Resource.post({
				resource: 'order.order_batch_delivery',
				data: {
					document_path: this.state.documents[0].path
				},
				success: function() {
					this.closeDialog();
					_.delay(function() {
						Reactman.PageAction.showHint('success', '批量发货成功');
					}, 500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
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
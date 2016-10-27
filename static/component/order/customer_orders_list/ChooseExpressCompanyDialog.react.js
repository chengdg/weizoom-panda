/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var ChooseExpressStore = require('./ChooseExpressStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var ChooseExpressCompanyDialog = Reactman.createDialog({
	getInitialState: function() {
		ChooseExpressStore.addListener(this.onChangeStore);
		return ChooseExpressStore.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateExpressCompany(property, value);
	},

	onChangeStore: function(){
		this.setState(ChooseExpressStore.getData());
	},

	onBeforeCloseDialog: function() {
		var orderIds = this.props.data.orderIds;
		var expressId = this.state.expressName;
		if(expressId==-1){
			Reactman.PageAction.showHint('error', '请先选择快递公司!');
			return false;
		}
		if(expressId!=-1){
			Reactman.Resource.get({
				resource: 'order.print_eorder',
				data: {
					order_ids: orderIds,
					express_id: expressId
				},
				success: function(res) {
					this.closeDialog();
					_.delay(function(){
						Dispatcher.dispatch({
							actionType: Constant.ORDER_CUSTOMER_ORDER_LIST_PRINT_ORDER,
							data: res
						});
					},10)
					
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}
	},

	render: function(){
		var optionsForExpress = this.state.optionsForExpress;
		return (
			<div style={{height: '120px'}}>
				<Reactman.FormSelect label="快递公司" name="expressName" value={this.state.expressName} options={optionsForExpress} onChange={this.onChange} />
			</div>
		)
	}
})
module.exports = ChooseExpressCompanyDialog;
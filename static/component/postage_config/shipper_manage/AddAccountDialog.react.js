/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.shipper_manage:AddCatalogDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

// var AccountTableStore = require('./AccountTableStore');
var DialogStore = require('./DialogStore');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogDialog = Reactman.createDialog({
	getInitialState: function() {
		DialogStore.addListener(this.onChangeStore);
		return DialogStore.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateData(property, value);
	},

	onChangeStore: function(){
		this.setState(DialogStore.getData());
	},

	onBeforeCloseDialog: function() {
		var expressId = this.state.expressId;
		if(expressId!=-1){
			Reactman.Resource.post({
				resource: 'postage_config.express_bill',
				data: {
					express_id: expressId,
					express_name: this.state.expressName,
					customer_name: this.state.customerName,
					customer_pwd: this.state.customerPwd,
					logistics_number: this.state.logisticsNumber,
					remark: this.state.remark,
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '修改成功!');
					},500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}else{
			Reactman.Resource.put({
				resource: 'postage_config.express_bill',
				data: {
					express_name: this.state.expressName,
					customer_name: this.state.customerName,
					customer_pwd: this.state.customerPwd,
					logistics_number: this.state.logisticsNumber,
					remark: this.state.remark,
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '添加成功!');
					},500);
					Action.clearData();
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
					<fieldset>
						<Reactman.FormInput type="text" label="快递公司:" name="expressName" validate="require-notempty" value={this.state.expressName} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="CustomerName:" name="customerName" validate="require-notempty" placeholder="商户代码/编号/ID，此信息由快递网点开通" value={this.state.customerName} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="CustomerPwd:" name="customerPwd" validate="require-notempty" placeholder="客户密码/密钥，此信息由快递网点开通" value={this.state.customerPwd} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="物流月结号:" name="logisticsNumber" validate="" value={this.state.logisticsNumber} onChange={this.onChange} />
						<Reactman.FormText type="text" label="备注:" name="remark" value={this.state.remark} onChange={this.onChange} inDialog={true} width={300} height={200}/>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddCatalogDialog;
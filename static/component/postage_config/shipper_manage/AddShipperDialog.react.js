/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.shipper_manage:AddCatalogDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

// var ShipperTableStore = require('./ShipperTableStore');
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

	onSelectArea: function(selectedIds, selectedDatas) {
		if(selectedIds==undefined){
			return;
		}
        if(selectedIds.length == 0){
            Reactman.PageAction.showHint('error', '您需要选择地区！');
            return;
        }
        Action.updateArea(selectedIds);
	},

	onBeforeCloseDialog: function() {
		console.log(this.state.shipperId);
		var shipperId = this.state.shipperId;
		if(shipperId!=-1){
			Reactman.Resource.post({
				resource: 'postage_config.shipper',
				data: {
					shipper_id: shipperId,
					shipper_name: this.state.shipperName,
					address: this.state.address,
					postcode: this.state.postcode,
					tel_number: this.state.telNumber,
					company_name: this.state.companyName,
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
				resource: 'postage_config.shipper',
				data: {
					shipper_name: this.state.shipperName,
					address: this.state.address,
					postcode: this.state.postcode,
					tel_number: this.state.telNumber,
					company_name: this.state.companyName,
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
						<Reactman.FormInput type="text" label="发货人:" name="shipperName" validate="require-notempty" value={this.state.shipperName} onChange={this.onChange} />
						
						<Reactman.FormInput type="text" label="详细地址:" name="address" validate="require-notempty" placeholder="街道楼号详细地址" value={this.state.address} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="邮政编码:" name="postcode" validate="" value={this.state.postcode} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="发货人手机号:" name="telNumber" validate="require-notempty" value={this.state.telNumber} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="单位名称:" name="companyName" validate="" value={this.state.companyName} onChange={this.onChange} />
						<Reactman.FormText type="text" label="备注:" name="remark" value={this.state.remark} onChange={this.onChange} inDialog={true} width={300} height={200}/>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddCatalogDialog;
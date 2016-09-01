/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var W = Reactman.W;

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'selfUserName': '',
			'remark': '',
			'isSync': ''
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateSelfShopDialog(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onBeforeCloseDialog: function() {
		console.log(this.state);
		if (this.state.selfUserName == '') {
			Reactman.PageAction.showHint('error', '请选择自营平台');
		} else {
			//给接口传递发货信息的参数
			Reactman.Resource.put({
				resource: 'self_shop.manage',
				data: {
					self_user_name: this.state.selfUserName,
					remark: this.state.remark,
					is_sync: this.state.isSync
				},
				success: function(action) {
					console.log(action,"===========");
					Reactman.PageAction.showHint('success', '添加自营平台成功');
					_.delay(function() {
							W.gotoPage('/self_shop/manage/');
						}, 500);
					// this.closeDialog();
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', '添加自营平台失败');
				},
				scope: this
			})
		}
	},

	render:function(){
		var typeOptions = [{
	        text: '平台1',
	        value: 'aaaa'
    	}];
		var optionsForSync = [{
	        text: '批量同步已有的商品',
	        value: 'isSync'
    	}];
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormSelect label="选择平台:" name="selfUserName" options={typeOptions} value={this.state.selfUserName} onChange={this.onChange}/>
						<Reactman.FormText label="备注说明:" name="remark" value={this.state.remark} onChange={this.onChange} width={300} height={150}/>
						<Reactman.FormCheckbox label="" name="isSync" value={this.state.isSync} options={optionsForSync} onChange={this.onChange} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddSelfShopDialog;
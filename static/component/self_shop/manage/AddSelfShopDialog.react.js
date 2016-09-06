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
		var options = this.props.data.options;
		var selfUserName = ''
		if(options.length > 0){
			selfUserName = options[0]['value']
		}
		return {
			selfUserName: selfUserName,
			remark: '',
			isSync: '',
			options: options
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState(Store.getData());
	},

	onBeforeCloseDialog: function() {
		if (this.state.selfUserName == '') {
			Reactman.PageAction.showHint('error', '请选择自营平台');
		} else {
			var selfShopName = $('#selfUserName').find("option:selected").text();
			//添加自营平台
			Reactman.Resource.put({
				resource: 'self_shop.manage',
				data: {
					self_shop_name: selfShopName,
					weapp_user_id: this.state.selfUserName, 
					remark: this.state.remark,
					is_sync: this.state.isSync.length > 0 ? 'is_sync': ''
				},
				success: function(action) {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '添加自营平台成功');
					},500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}
	},

	render:function(){
		var optionsForSync = [{
			text: '批量同步已有的商品',
			value: 'isSync'
		}];
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormSelect label="选择平台:" name="selfUserName" value={this.state.selfUserName} options={this.state.options} onChange={this.onChange}/>
						<Reactman.FormText label="备注说明:" name="remark" value={this.state.remark} onChange={this.onChange} width={300} height={150}/>
						<Reactman.FormCheckbox label="" name="isSync" value={this.state.isSync} options={optionsForSync} onChange={this.onChange} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddSelfShopDialog;
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
			'self_user_name': '',
			'rebate_value': '',
			'remark': '',
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addRebateValue(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onBeforeCloseDialog: function() {
		if (this.state.self_user_name == '') {
			Reactman.PageAction.showHint('error', '请选择自营平台');
		} else {
			//给接口传递发货信息的参数
			var selfUserName = this.state.self_user_name;
			var rebateValue = this.state.rebate_value;
			var remark = this.state.remark;
			console.log(selfUserName,rebateValue,remark,'========');
			Reactman.Resource.put({
				resource: 'self_shop.manage',
				data: {
					self_user_name: selfUserName,
					rebate_value: rebateValue,
					remark: remark
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
			text: '',
			value: ''
		},{
			text: '微众商城',
			value: 'weizoom_shop'
		}, {
			text: '微众家',
			value: 'weizoom_jia'
		}, {
			text: '微众妈妈',
			value: 'weizoom_mama'
		}, {
			text: '微众学生',
			value: 'weizoom_xuesheng'
		}, {
			text: '微众白富美',
			value: 'weizoom_baifumei'
		}, {
			text: '微众俱乐部',
			value: 'weizoom_club'
		}, {
			text: '微众Life',
			value: 'weizoom_life'
		}, {
			text: '微众一家人',
			value: 'weizoom_yjr'
		}, {
			text: '惠惠来啦',
			value: 'weizoom_fulilaile'
		}];
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormSelect label="选择平台:" name="self_user_name" options={typeOptions} value={this.state.self_user_name} onChange={this.onChange}/>
						<div className="rebate_tips">提示：扣点基础表示该平台与商品管理系统约定的额外扣点设置。如某客户标准扣点5%，微众家的扣点基数是2，则该客户商品同步到微众家后按照10%的扣点来计算出商品采购价（即结算价）。</div>
						<Reactman.FormInput label="扣点基数:" type="text" name="rebate_value" value={this.state.rebate_value} onChange={this.onChange} validate="require-float" />
						<Reactman.FormText label="备注:" name="remark" value={this.state.remark} onChange={this.onChange} width={300} height={150}/>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddSelfShopDialog;
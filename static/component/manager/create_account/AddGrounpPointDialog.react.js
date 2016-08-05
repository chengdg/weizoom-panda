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

var AddGrounpPointDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'self_user_name': ''
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateAccount(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onBeforeCloseDialog: function(){
		var _this = this;
		var selfUserNames = this.state.self_user_names;
		var is_true = false;
		_.each(selfUserNames, function(userNames){
			if(userNames.self_user_name == _this.state.self_user_name){
				is_true = true;
			}
		})

		if(is_true){
			Reactman.PageAction.showHint('error', '该自营平台已选,请重新选择!');
			return;
		}
		
		if (this.state.self_user_name == '') {
			Reactman.PageAction.showHint('error', '请选择自营平台');
		} else {
			Action.addSelfShop(this.state.self_user_name);
			_.delay(function(){
				_this.closeDialog();
			},200)
		}
	},

	render:function(){
		var typeOptions = [{
			text: '请选择自营平台',
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
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddGrounpPointDialog;
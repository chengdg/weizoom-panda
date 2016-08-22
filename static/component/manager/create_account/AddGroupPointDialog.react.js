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

var AddGroupPointDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'selfUserName': ''
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
		var selfUserNames = this.state.selfUserNames;
		var isChecked = false;
		_.each(selfUserNames, function(userNames){
			if(userNames.selfUserName == _this.state.selfUserName){
				isChecked = true;
			}
		})

		if(isChecked){
			Reactman.PageAction.showHint('error', '该自营平台已选,请重新选择!');
			return;
		}
		
		if (this.state.selfUserName == '') {
			Reactman.PageAction.showHint('error', '请选择自营平台');
		} else {
			Action.addSelfShop(this.state.selfUserName);
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
						<Reactman.FormSelect label="选择平台:" name="selfUserName" options={typeOptions} value={this.state.selfUserName} onChange={this.onChange}/>				
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddGroupPointDialog;
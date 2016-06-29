/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.create_account:AccountCreatePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AccountCreatePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		debug(value);
		var property = event.target.getAttribute('name');
		if(property == 'account_type'){
			if(!W.is_edit){
				Action.updateAccount(property, value);
			}
		}else{
			Action.updateAccount(property, value);
		}
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onSubmit: function() {
		Action.saveAccount(Store.getData());
	},
	render:function(){
		var optionsForAccountType = [{
			text: '体验客户',
			value: '1'
		}, {
			text: '代理商',
			value: '2'
		}, {
			text: '运营',
			value: '3'
		}];
		
		var disabled = W.is_edit ? 'disabled' : '';
		if(W.is_edit){
			var label_name = '修改密码:';
			var validate = "";
		}else{
			var label_name = '登录密码:';
			var validate = "require-notempty";
		}
		
		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<legend className="pl10 pt10 pb10">账号信息</legend>
					<Reactman.FormRadio label="账号类型:" name="account_type" value={this.state.account_type} options={optionsForAccountType} onChange={this.onChange} />
					<Reactman.FormInput label="账号名称:" name="name" validate="require-string" placeholder="" value={this.state.name} onChange={this.onChange} />
					<Reactman.FormInput label="登录账号:" readonly={disabled} name="username" validate="require-notempty" placeholder="" value={this.state.username} onChange={this.onChange} />
					<Reactman.FormInput label={label_name} type="password" name="password" validate={validate} placeholder="" value={this.state.password} onChange={this.onChange} />
					<Reactman.FormText label="备注:" name="note" placeholder="" value={this.state.note} inDialog={true} width={320} height={200} onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<Reactman.FormSubmit onClick={this.onSubmit} text="保 存"/>
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = AccountCreatePage;
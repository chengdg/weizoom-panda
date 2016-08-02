/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:business.manager:BusinessDetailPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var BusinessDetailPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},
	
	componentDidMount: function () {
		Action.selectCatalog();
	},
	
	onChange: function(value, event) {
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
			text: '合作客户',
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
					<div>
						<AccountInfo onChange = {this.onChange}
							company_name = {this.state.company_name}
							name = {this.state.name}
							// company_type = {this.state.company_type}
							purchase_method = {this.state.purchase_method}
							points = {this.state.points}
							contacter = {this.state.contacter}
							phone = {this.state.phone}
							valid_time_from = {this.state.valid_time_from}
							valid_time_to = {this.state.valid_time_to}
							Type = {this.state.account_type}
							options_for_type = {this.state.options_for_type}
						/>
					</div>
					<Reactman.FormInput label="登录名:" readonly={disabled} name="username" validate="require-notempty" placeholder="" value={this.state.username} onChange={this.onChange} />
					<Reactman.FormInput label={label_name} type="password" name="password" validate={validate} placeholder="" value={this.state.password} onChange={this.onChange} />
					<Reactman.FormText label="备注:" name="note" value={this.state.note} inDialog={true} width={320} height={200} onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<Reactman.FormSubmit onClick={this.onSubmit} text="保 存"/>
				</fieldset>
			</form>
		</div>
		)
	}
});

var AccountInfo = React.createClass({
	render: function() {
		var account_type = this.props.Type;
		var optionsForPurchaseMethod = [{
			text: '固定底价',
			value: '1'
		}, {
			text: '零售价返点',
			value: '2'
		}, {
			text: '以货抵款',
			value: '3'
		}];
		
		if (account_type == '1'){
			return(
				<div>
					<Reactman.FormInput label="公司名称:" type="text" name="company_name" value={this.props.company_name} onChange={this.props.onChange} />
					<Reactman.FormInput label="店铺名称:" type="text" name="name" validate="require-notempty" placeholder="建议填写为客户公司简称，将在微众平台手机端展示给用户" value={this.props.name} onChange={this.props.onChange} />
					<Reactman.FormRadio label="采购方式:" name="purchase_method" value={this.props.purchase_method} options={optionsForPurchaseMethod} onChange={this.props.onChange} />
					<div>
						<PurchaseMethod onChange = {this.props.onChange}
							points = {this.props.points}
							Type = {this.props.purchase_method}
						/>
					</div>
					<Reactman.FormInput label="联系人:" type="text" name="contacter" value={this.props.contacter} onChange={this.props.onChange} />
					<Reactman.FormInput label="手机号:" type="text" name="phone" value={this.props.phone} onChange={this.props.onChange} />
					<div className="account-create-valid-time">
						<Reactman.FormDateTimeInput label="有效期:" name="valid_time_from" validate="require-notempty" value={this.props.valid_time_from} readOnly onChange={this.props.onChange} />
						<Reactman.FormDateTimeInput label="至:" name="valid_time_to" value={this.props.valid_time_to} readOnly onChange={this.props.onChange} />
					</div>
				</div>
			)
		}else {
			return(
				<div>
					<Reactman.FormInput label="账号名称:" type="text" name="name" validate="require-string" placeholder="" value={this.props.name} onChange={this.props.onChange} />
				</div>
			)
		}
	}
});
var PurchaseMethod = React.createClass({
	render: function() {
		var type = this.props.Type;
		if (type == '2'){
			return(
				<div className="account-create-purchase-method">
					<Reactman.FormInput label="零售价返点:" type="text" name="points" validate="require-notempty" value={this.props.points} onChange={this.props.onChange} />
					<span className="money_note">%</span>
				</div>
			)
		}else {
			return(
				<div></div>
			)
		}
	}
});
module.exports = BusinessDetailPage;
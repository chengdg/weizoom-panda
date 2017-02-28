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
var AddGroupPointDialog = require('./AddGroupPointDialog.react');
var PurchaseMethod = require('./PurchaseMethod.react');
require('./style.css');

var AccountCreatePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var account = Store.getData();
		
		if(W.is_edit){
			Action.getCompanyInfoFromAxe(account.companyName);
		}
		return Store.getData();
	},
	
	componentDidMount: function () {
		Action.selectCatalog();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		if(property == 'companyName'){
			Action.getCompanyInfoFromAxe(value);
		}
		if(property == 'companyNameOption'){ //选择公司名称时自动填充【公司名称】、【联系人】、【手机号】字段
			var companyName = $(event.target).find("option:selected").text();
			var contacter = value.split('/')[0];
			var phone = value.split('/')[1];
			if(companyName != '请选择已有公司'){
				Action.updateAccount('companyName', companyName);
				Action.updateAccount('contacter', contacter);
				Action.updateAccount('phone', phone);
			}
		}
		if(property == 'accountType'){
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
		var account = Store.getData();
		var accountType = parseInt(account.accountType);
		var purchaseMethod = parseInt(account.purchaseMethod);
		var reg = /^(0|[1-9]|[1-9]\d|99)$/;
		var regPhone = /^0{0,1}(13[0-9]|15[0-9]|17[0-9]|18[0-9])[0-9]{8}$/g;
		var regUsername = /^[0-9a-zA-Z]*$/g;
		var regServiceTel = /^[0-9 -]+$/;
		var regServiceQQ = /^[0-9]*$/;

		if(accountType == 1 && purchaseMethod == 2 && account.hasOwnProperty('points') && account.points.length > 0){
			if(!reg.test(account.points.trim())){
				Reactman.PageAction.showHint('error', '零售价返点数字需在1-99之间的整数');
				return;
			}
		}
		if(accountType == 1 && (!account.hasOwnProperty('validTimeFrom') || !account.hasOwnProperty('validTimeTo'))){
			Reactman.PageAction.showHint('error', '请选择有效期截止日期!');
			return;
		}
		if(accountType == 1 && ((account.hasOwnProperty('validTimeFrom') && account.validTimeFrom.length <= 0) 
			|| (account.hasOwnProperty('validTimeTo') && account.validTimeTo.length <= 0))){
			Reactman.PageAction.showHint('error', '请选择有效期截止日期!');
			return;
		}
		if(accountType == 1 && account.hasOwnProperty('validTimeFrom') && account.hasOwnProperty('validTimeTo') && (account.validTimeFrom > account.validTimeTo)){
			Reactman.PageAction.showHint('error', '有效期开始日期不能大于截止日期,请重新输入!');
			return;
		}
		if(accountType == 1 && account.hasOwnProperty('phone') && account.phone.length > 0){
			if(!regPhone.test(account.phone.trim())){
				Reactman.PageAction.showHint('error', '请填写合法的手机号码');
				return;
			}
		}
		if(accountType == 1 && account.hasOwnProperty('contacter') && account.contacter.length > 0){
			if(account.contacter.length > 10){
				Reactman.PageAction.showHint('error', '联系人最多10个字符');
				return;
			}
		}
		if(!regUsername.test(account.username.trim())){
			Reactman.PageAction.showHint('error', '登录名请填写英文字母或数字');
			return;
		}
		if(accountType ==1 && account.companyType.length <= 0){
			Reactman.PageAction.showHint('error', '请选择经营类目');
			return;
		}

		if(accountType == 1 && account.companyName != $('#companyNameOption').find("option:selected").text()){
			Reactman.PageAction.showHint('error', '请选择公司名称');
			return;
		}

		if((account.customerServiceTel.length>0 && !regServiceTel.test(account.customerServiceTel)) || account.customerServiceTel.length>20){
			Reactman.PageAction.showHint('error', '请输入有效的客服联系号码');
			return;
		}
		if((account.customerServiceQQFirst.length>0 && !regServiceQQ.test(account.customerServiceQQFirst)) || account.customerServiceQQFirst.length>20){
			Reactman.PageAction.showHint('error', '请输入有效的客服QQ号码');
			return;
		}
		if((account.customerServiceQQFirst.length>0 && !regServiceQQ.test(account.customerServiceQQSecond)) || account.customerServiceQQFirst.length>20){
			Reactman.PageAction.showHint('error', '请输入有效的客服QQ号码');
			return;
		}

		Action.saveAccount(Store.getData());
	},
	render:function(){
		var optionsForAccountType = [{
			text: '合作客户',
			value: '1'
		}, 
		// {
		// 	text: '代理商',
		// 	value: '2'
		// }, 
		{
			text: '运营',
			value: '3'
		}];

		var disabled = W.is_edit ? 'disabled' : '';
		if(W.is_edit){
			var labelName = '修改密码:';
			var validate = "";
		}else{
			var labelName = '登录密码:';
			var validate = "require-notempty";
		}
		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<legend className="pl10 pt10 pb10">账号信息</legend>
					<Reactman.FormRadio label="账号类型:" name="accountType" value={this.state.accountType} options={optionsForAccountType} onChange={this.onChange} />
					<div>
						<AccountInfo onChange = {this.onChange}
							companyName = {this.state.companyName}
							name = {this.state.name}
							companyType = {this.state.companyType}
							purchaseMethod = {this.state.purchaseMethod}
							points = {this.state.points}
							contacter = {this.state.contacter}
							phone = {this.state.phone}
							validTimeFrom = {this.state.validTimeFrom}
							validTimeTo = {this.state.validTimeTo}
							Type = {this.state.accountType}
							optionsForType = {this.state.optionsForType}
							optionsForCompanyName = {this.state.optionsForCompanyName}
							companyNameOption = {this.state.companyNameOption}
							selfUserNames = {this.state.selfUserNames}
							maxProduct = {this.state.maxProduct}
							settlementPeriod = {this.state.settlementPeriod}
						/>
					</div>
					<Reactman.FormInput label="登录名:" readonly={disabled} name="username" validate="require-notempty" placeholder="" value={this.state.username} onChange={this.onChange} />
					<Reactman.FormInput label={labelName} type="password" name="password" validate={validate} placeholder="" value={this.state.password} onChange={this.onChange} />
					<Reactman.FormText label="备注:" name="note" value={this.state.note} inDialog={true} width={320} height={200} onChange={this.onChange} />
					<CustomerService onChange = {this.onChange} Type = {this.state.accountType} customerServiceTel = {this.state.customerServiceTel} customerServiceQQFirst = {this.state.customerServiceQQFirst} customerServiceQQSecond = {this.state.customerServiceQQSecond}/>
				</fieldset>
				<fieldset>
					<Reactman.FormSubmit onClick={this.onSubmit} text="保 存"/>
				</fieldset>
			</form>
		</div>
		)
	}
});

var CustomerService = React.createClass({
	render: function(){
		var accountType = this.props.Type;
		if(accountType == '1'){
			return(
				<div>
					<div style={{margin:'30px 0px 15px 70px', color:'#000'}}>客户后台显示的在线客服联系方式</div>
					<Reactman.FormInput label="客服电话:" name="customerServiceTel" placeholder="" value={this.props.customerServiceTel} onChange={this.props.onChange} />
					<Reactman.FormInput label="客服qq-1:" name="customerServiceQQFirst" placeholder="" value={this.props.customerServiceQQFirst} onChange={this.props.onChange} />
					<Reactman.FormInput label="客服qq-2:" name="customerServiceQQSecond" placeholder="" value={this.props.customerServiceQQSecond} onChange={this.props.onChange} />
				</div>
			)
		}else{
			return(
				<div></div>
			)
		}
	}
});

var AccountInfo = React.createClass({
	render: function() {
		var accountType = this.props.Type;
		var optionsForPurchaseMethod = [{
			text: '固定底价',
			value: '1'
		}, {
			text: '零售价返点',
			value: '2'
		}, {
			text: '高佣直采',
			value: '4'
		}];
		var optionsForSettlementPeriod =  [{
			text: '自然月',
			value: '1'
		}, {
			text: '15天',
			value: '2'
		}, {
			text: '自然周',
			value: '3'
		}];
		
		if(accountType == '1'){
			return(
				<div>
					<Reactman.FormInput label="公司名称:" validate="require-notempty" type="text" name="companyName" value={this.props.companyName} onChange={this.props.onChange} />
					<Reactman.FormSelect label="" name="companyNameOption" value={this.props.companyNameOption} options={this.props.optionsForCompanyName } onChange={this.props.onChange} />
					<Reactman.FormInput label="店铺名称:" type="text" name="name" validate="require-notempty" placeholder="建议填写为客户公司简称，将在微众平台手机端展示给用户" value={this.props.name} onChange={this.props.onChange} />
                    <Reactman.FormRadio label="采购方式:" name="purchaseMethod" value={this.props.purchaseMethod} options={optionsForPurchaseMethod} onChange={this.props.onChange} />
					<div>
						<PurchaseMethod onChange = {this.props.onChange}
							points = {this.props.points}
							Type = {this.props.purchaseMethod}
						/>
					</div>
                    <Reactman.FormRadio label="结算账期:" name="settlementPeriod" value={this.props.settlementPeriod} options={optionsForSettlementPeriod} onChange={this.props.onChange} />
                    <Reactman.FormCheckbox label="经营类目:" name="companyType" value={this.props.companyType} options={this.props.optionsForType} onChange={this.props.onChange} />
					<Reactman.FormInput label="商品个数上限:" type="text" validate="require-int" name="maxProduct" value={this.props.maxProduct} onChange={this.props.onChange} />
					<Reactman.FormInput label="联系人:" type="text" name="contacter" value={this.props.contacter} onChange={this.props.onChange} />
					<Reactman.FormInput label="手机号:" type="text" name="phone" value={this.props.phone} onChange={this.props.onChange} />
					<div className="account-create-valid-time">
						<Reactman.FormDateTimeInput label="有效期:" name="validTimeFrom" validate="require-notempty" value={this.props.validTimeFrom} readOnly onChange={this.props.onChange} />
						<Reactman.FormDateTimeInput label="至:" name="validTimeTo" value={this.props.validTimeTo} readOnly onChange={this.props.onChange} />
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
module.exports = AccountCreatePage;
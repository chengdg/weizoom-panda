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
		var account = Store.getData();
		var account_type = parseInt(account.account_type);
		var purchase_method = parseInt(account.purchase_method);
		var reg = /^(0|[1-9]|[1-9]\d|99)$/;
		// var reg_phone = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
		var reg_phone = /^0{0,1}(13[0-9]|15[0-9]|17[0-9]|18[0-9])[0-9]{8}$/g;
		var reg_username = /^[0-9a-zA-Z]*$/g;

		if(account_type ==1 && purchase_method == 2 &&account.hasOwnProperty('points') && account.points.length>0){
			if((parseFloat(account.points.trim())==0) || !reg.test(account.points.trim())){
				Reactman.PageAction.showHint('error', '零售价返点数字需在1-99之间的整数');
				return;
			}
		}
		if(account_type ==1 && (!account.hasOwnProperty('valid_time_from') || !account.hasOwnProperty('valid_time_to'))){
			Reactman.PageAction.showHint('error', '请选择有效期截止日期!');
			return;
		}
		if(account_type ==1 && ((account.hasOwnProperty('valid_time_from') && account.valid_time_from.length<=0) 
			|| (account.hasOwnProperty('valid_time_to')&& account.valid_time_to.length<=0))){
			Reactman.PageAction.showHint('error', '请选择有效期截止日期!');
			return;
		}
		if(account_type ==1 && account.hasOwnProperty('valid_time_from') && account.hasOwnProperty('valid_time_to') && (account.valid_time_from>account.valid_time_to)){
			Reactman.PageAction.showHint('error', '有效期开始日期不能大于截止日期,请重新输入!');
			return;
		}
		if(account_type ==1 && account.hasOwnProperty('phone') && account.phone.length>0){
			if(!reg_phone.test(account.phone.trim())){
				Reactman.PageAction.showHint('error', '请填写合法的手机号码');
				return;
			}
		}
		if(account_type ==1 && account.hasOwnProperty('contacter') && account.contacter.length>0){
			if(account.contacter.length>10){
				Reactman.PageAction.showHint('error', '联系人最多10个字符');
				return;
			}
		}
		if(!reg_username.test(account.username.trim())){
			Reactman.PageAction.showHint('error', '登录名请填写英文字母或数字');
			return;
		}
		if(account_type ==1 && account.company_type.length<=0){
			Reactman.PageAction.showHint('error', '请选择经营类目');
			return;
		}
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
							company_type = {this.state.company_type}
							purchase_method = {this.state.purchase_method}
							points = {this.state.points}
							contacter = {this.state.contacter}
							phone = {this.state.phone}
							valid_time_from = {this.state.valid_time_from}
							valid_time_to = {this.state.valid_time_to}
							Type = {this.state.account_type}
							options_for_type = {this.state.options_for_type}
							selfUserNames={this.state.self_user_names}
							max_product={this.state.max_product}

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
                    <Reactman.FormCheckbox label="经营类目:" name="company_type" value={this.props.company_type} options={this.props.options_for_type} onChange={this.props.onChange} />
					<Reactman.FormRadio label="采购方式:" name="purchase_method" value={this.props.purchase_method} options={optionsForPurchaseMethod} onChange={this.props.onChange} />
					<div>
						<PurchaseMethod onChange = {this.props.onChange}
							points = {this.props.points}
							Type = {this.props.purchase_method}
						/>
					</div>
					<Reactman.FormInput label="最多上传商品数:" type="text" validate="require-int" name="max_product" value={this.props.max_product} onChange={this.props.onChange} />
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
// var PurchaseMethod = React.createClass({
// 	getInitialState: function() {
// 		Store.addListener(this.onChangeStore);
// 		return Store.getData();
// 	},
	
// 	onChangeStore: function() {
// 		this.setState(Store.getData());
// 	},

// 	onChangeValue: function(index, value, event){
// 		var property = event.target.getAttribute('name');
// 		console.log(index,value, property);
// 		Action.updateRebates(index, property, value);
// 	},

// 	addGrounpPoints: function(){
// 		Reactman.PageAction.showDialog({
// 			title: "添加自营平台",
// 			component: AddGrounpPointDialog,
// 			data: {},
// 			success: function(inputData, dialogState) {
// 				console.log("success");
// 			}
// 		});
// 	},

// 	addRebateDialog: function(){
// 		var rebates = this.state.rebates;
// 		console.log(rebates.length)
// 		if(rebates.length>2){
// 			Reactman.PageAction.showHint('error', '最多添加三个条件!');
// 			return;
// 		}
// 		Action.addRebateDialog();
// 	},

// 	deleteRebateValue: function(index){
// 		Action.deleteRebateValue(index);
// 	},

// 	render: function() {
// 		var type = this.props.Type;
// 		if (type == '2'){
// 			return(
// 				<div>
// 				<div className="account-create-purchase-method">
// 					<Reactman.FormInput label="零售扣点:" type="text" name="points" validate="require-notempty" value={this.props.points} onChange={this.props.onChange} />
// 					<span className="money_note">%</span>
// 					<span className="add-grounp-points">
// 						<a href="javascript:void(0);" onClick={this.addGrounpPoints}>增加团购扣点</a>
// 					</span>
// 				</div>
// 				<div><GrounpPointsDialog /></div>
// 				</div>
// 			)
// 		}if(type == '3'){
// 			var rebates = this.state.rebates;
// 			var _this = this;
// 			console.log(rebates);
// 			var rebate_dialog = '';
// 			if(rebates.length>0){
// 				rebate_dialog = rebates.map(function(rebate, index){
// 					return(
// 						<div className="rebates-dialog" key={index}>
// 							<span>周期</span>
// 							<Reactman.FormDateTimeInput label="" name="validate_from_condition" value={rebate.validate_from_condition} readOnly onChange={_this.onChangeValue.bind(_this,index)} />
// 							<span style={{marginLeft:'70px'}}>至</span>
// 							<Reactman.FormDateTimeInput label="" name="validate_to_condition" value={rebate.validate_to_condition} readOnly onChange={_this.onChangeValue.bind(_this,index)} />
// 							<span style={{display:'inline-block',marginLeft:'70px'}}>且金额不大于</span>
// 							<Reactman.FormInput label="" type="text" name="order_money_condition" value={rebate.order_money_condition} onChange={_this.onChangeValue.bind(_this,index)} />
// 							<span>元时,返点比例为</span>
// 							<Reactman.FormInput label="" type="text" name="rebate_proport_condition" value={rebate.rebate_proport_condition} onChange={_this.onChangeValue.bind(_this,index)} />
// 							<span>否则,将按</span>
// 							<Reactman.FormInput label="" type="text" name="default_rebate_proport_condition" value={rebate.default_rebate_proport_condition} onChange={_this.onChangeValue.bind(_this,index)} />
// 							<span>%基础扣点结算。</span>
// 							<a className="rebate-close" href="javascript:void(0);" onClick={_this.deleteRebateValue.bind(_this,index)} title="删除">x</a>
// 						</div>
// 					)
// 				})
// 			}
// 			return(
// 				<div>
// 					<div className="profilts-dialog" style={{display:'inline-block'}}>
// 						<span style={{display:'inline-block'}}>首月(商品上架后30天含内),且金额不大于</span>
// 						<Reactman.FormInput label="" type="text" name="order_money" value={this.state.order_money} onChange={this.props.onChange} />
// 						<span>元时,返点比例为</span>
// 						<Reactman.FormInput label="" type="text" name="rebate_proport" value={this.state.rebate_proport} onChange={this.props.onChange} />
// 						<span>否则,将按</span>
// 						<Reactman.FormInput label="" type="text" name="default_rebate_proport" value={this.state.default_rebate_proport} onChange={this.props.onChange} />
// 						<span>%基础扣点结算。</span>
// 					</div>
// 					<button type="button" className="btn btn-primary" style={{marginLeft:'10px'}} onClick={this.addRebateDialog}>+添加</button>
// 					{rebate_dialog}
// 				</div>
// 			)
// 		}else {
// 			return(
// 				<div></div>
// 			)
// 		}
// 	}
// });

// var GrounpPointsDialog = React.createClass({
// 	getInitialState: function() {
// 		Store.addListener(this.onChangeStore);
// 		return Store.getData();
// 	},
	
// 	onChangeStore: function() {
// 		this.setState(Store.getData());
// 	},

// 	onChange: function(value, event) {
// 		var property = event.target.getAttribute('name');
// 		console.log(property, value)
// 		Action.updateAccount(property, value);
// 	},

// 	deleteSelfShop: function(index){
// 		Action.deleteSelfShop(index);
// 	},

// 	render: function() {
// 		var SELF_SHOP2TEXT = {
// 			'weizoom_jia': '微众家',
// 			'weizoom_mama': '微众妈妈',
// 			'weizoom_xuesheng': '微众学生',
// 			'weizoom_baifumei': '微众白富美',
// 			'weizoom_shop': '微众商城',
// 			'weizoom_club': '微众俱乐部',
// 			'weizoom_life': '微众Life',
// 			'weizoom_yjr': '微众一家人',
// 			'weizoom_fulilaile': '惠惠来啦'
// 		}
// 		var selfUserNames = this.state.self_user_names;
// 		var _this = this;
// 		if (selfUserNames.length>0){
// 			var selfShop = selfUserNames.map(function(selfUser,index){
// 				var selfUserName = selfUser.self_user_name;
// 				var userName = SELF_SHOP2TEXT[selfUser.self_user_name];
// 				return(
// 						<li key={index} style={{display:'inline-block',position:'relative'}}>
// 	                        <Reactman.FormInput label={userName} type="text" name={selfUserName+"_value"} onChange={_this.onChange} value={_this.state[selfUserName+"_value"]}/>
// 	                    	<span className="rebate-per">%</span>
// 	                    	<span className="xui-close" onClick={_this.deleteSelfShop.bind(_this,index)} title="删除">x</span>
// 	                    </li>
// 					)
// 			})
// 			return(
// 				<div className="self-user-dialog" style={{position:'relative'}}>
// 					<span style={{position:'absolute',left:'75px'}}>团购扣点</span>
// 					<ul className="self-user-shop-ul">
// 						{selfShop}
// 					</ul>
// 				</div>
// 			)
// 		}else {
// 			return(
// 				<div></div>
// 			)
// 		}
// 	}
// });
module.exports = AccountCreatePage;
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
var ProductModelList = require('./ProductModelList.react');

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
		if(property == 'apply_catalogs'){
			Action.getQualifications(this.state.id,value);
		}
		Action.updateAccount(property, value);
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onSubmit: function() {
		var data = Store.getData();
		var upload_business_qualifications = data.upload_business_qualifications;
		var is_upload = true;
		var reg_phone = /^0{0,1}(13[0-9]|15[0-9]|17[0-9]|18[0-9])[0-9]{8}$/g;
		var reg_number = /^[1-9]\d*(\.\d+)?$/;
		var reg_email = /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/;
		//校验
		if(data.hasOwnProperty('company_money') && data.company_money.length>0){
			if(!reg_number.test(data.company_money.trim())){
				Reactman.PageAction.showHint('error', '请填写正确的注册资本');
				return;
			}
		}
		if(data.hasOwnProperty('phone') && data.phone.length>0){
			if(!reg_phone.test(data.phone.trim())){
				Reactman.PageAction.showHint('error', '请填写正确的手机号');
				return;
			}
		}
		if(data.hasOwnProperty('e_mail') && data.e_mail.length>0){
			if(!reg_email.test(data.e_mail.trim())){
				Reactman.PageAction.showHint('error', '请填写正确的E-mail');
				return;
			}
		}
		if(data.business_license == ''){
			Reactman.PageAction.showHint('error', '请上传营业执照!');
			return;
		}
		if(data.tax_registration_certificate == ''){
			Reactman.PageAction.showHint('error', '请上传税务登记证!');
			return;
		}
		if(data.organization_code_certificate == ''){
			Reactman.PageAction.showHint('error', '请上传组织机构代码证!');
			return;
		}
		if(data.account_opening_license == ''){
			Reactman.PageAction.showHint('error', '请上传开户许可证!');
			return;
		}
		upload_business_qualifications.map(function(upload_business_qualification,index){
			if(upload_business_qualification.img == ''){
				is_upload = false;
				Reactman.PageAction.showHint('error', '请上传' + upload_business_qualification.qualification_name);
				return;
			}
		});
		if(!is_upload){
			return;
		}
		Action.saveAccount(Store.getData());
	},

	render:function(){
		var optionsForAccountType = [{
			text: '厂家直销',
			value: '1'
		}, {
			text: '代理/贸易/分销',
			value: '2'
		}];
		return (
		<div className="xui-outlineData-page xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<legend className="pl10 pt10 pb10">基本信息</legend>
					<Reactman.FormRadio label="企业类型:" name="company_type" value={this.state.company_type} options={optionsForAccountType} onChange={this.onChange} />
					<Reactman.FormInput label="公司名称:" name="company_name" validate="require-notempty" value={this.state.company_name} onChange={this.onChange} />
					<div className="account-create-purchase-method">
						<Reactman.FormInput label="注册资本:" name="company_money" value={this.state.company_money} onChange={this.onChange} />
						<span className="money_note">万元</span>
					</div>
					<Reactman.FormInput label="法人代表:" name="legal_representative" value={this.state.legal_representative} onChange={this.onChange} />
					<Reactman.FormInput label="联系人:" name="contacter" validate="require-notempty" value={this.state.contacter} onChange={this.onChange} />
					<Reactman.FormInput label="手机号:" name="phone" validate="require-notempty" value={this.state.phone} onChange={this.onChange} />
					<Reactman.FormInput label="E-mail:" name="e_mail" value={this.state.e_mail} onChange={this.onChange} />
					<Reactman.FormInput label="微信/QQ:" name="we_chat_and_qq" value={this.state.we_chat_and_qq} onChange={this.onChange} />
					<Reactman.FormInput label="公司所在地:" name="company_location" validate="require-notempty" value={this.state.company_location} onChange={this.onChange} />
					<Reactman.FormInput label="详细地址:" name="address" validate="require-notempty" value={this.state.address} onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<legend className="pl10 pt10 pb10">基本资质</legend>
					<Reactman.FormImageUploader label="营业执照:" name="business_license" value={this.state.business_license} onChange={this.onChange} max={1} />
					<Reactman.FormDateTimeInput label="营业执照有效期:" validate="require-notempty" name="business_license_time" value={this.state.business_license_time} onChange={this.onChange} />
					<Reactman.FormImageUploader label="税务登记证:" name="tax_registration_certificate" value={this.state.tax_registration_certificate} onChange={this.onChange} max={1} />
					<Reactman.FormDateTimeInput label="税务登记证有效期:" validate="require-notempty" name="tax_registration_certificate_time" value={this.state.tax_registration_certificate_time} onChange={this.onChange} />
					<Reactman.FormImageUploader label="组织机构代码证:" name="organization_code_certificate" value={this.state.organization_code_certificate} onChange={this.onChange} max={1} />
					<Reactman.FormDateTimeInput label="组织机构代码证有效期:" validate="require-notempty" name="organization_code_certificate_time" value={this.state.organization_code_certificate_time} onChange={this.onChange} />
					<Reactman.FormImageUploader label="开户许可证:" name="account_opening_license" value={this.state.account_opening_license} onChange={this.onChange} max={1} />
					<Reactman.FormDateTimeInput label="开户许可证有效期:" validate="require-notempty" name="account_opening_license_time" value={this.state.account_opening_license_time} onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<legend className="pl10 pt10 pb10">入驻类目及特殊资质</legend>
					<Reactman.FormCheckbox label="申请类目:" name="apply_catalogs" value={this.state.apply_catalogs} options={this.state.options_for_type} onChange={this.onChange} />
					<ProductModelList name='models' value={this.state.upload_business_qualifications} onChange={this.onChange} />
				</fieldset>
				<fieldset>
					<Reactman.FormSubmit onClick={this.onSubmit} text="保 存"/>
				</fieldset>
			</form>
		</div>
		)
	}
});
module.exports = BusinessDetailPage;
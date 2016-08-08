/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:freight_service.service:ServicePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var ServicePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var preSaleTel = W.pre_sale_tel=='-1'?'':W.pre_sale_tel;
		var afterSaleTel = W.after_sale_tel=='-1'?'':W.after_sale_tel;
		return {
			'pre_sale_tel': preSaleTel,
			'after_sale_tel': afterSaleTel
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addSalePhone(property, value);
	},


	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onSubmit: function(){
		var preSaleTel = this.state.pre_sale_tel;
		var afterSaleTel = this.state.after_sale_tel;
		var regTel = /^0\d{2,3}-?\d{7,8}$/;
		var regMobile = /^1\d{10}$/;
		if(!regTel.test(preSaleTel) && !regMobile.test(preSaleTel)){
			Reactman.PageAction.showHint('error', '请输入正确的电话号码！');
			return
		}
		if(!regTel.test(afterSaleTel) && !regMobile.test(afterSaleTel)){
			Reactman.PageAction.showHint('error', '请输入正确的电话号码！');
			return
		}
		Action.saveSalePhone(preSaleTel, afterSaleTel);
	},

	render:function(){
		return (
			<div className="xui-newProduct-page xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset style={{paddingTop:'20px'}}>
						<Reactman.FormInput label="售前电话:" type="text" name="pre_sale_tel" value={this.state.pre_sale_tel} onChange={this.onChange} />
						<Reactman.FormInput label="售后电话:" type="text" name="after_sale_tel" value={this.state.after_sale_tel} onChange={this.onChange} />
					</fieldset>
					<fieldset style={{position:'relative'}} className="save-btn">
						<Reactman.FormSubmit onClick={this.onSubmit} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = ServicePage;
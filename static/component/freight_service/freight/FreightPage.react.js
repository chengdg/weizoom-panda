/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:freight_service.freight:FreightPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var FreightPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var freeFreightMoney = W.free_freight_money=='-1'?'':W.free_freight_money;
		var needFreightMoney = W.need_freight_money=='-1'?'0':W.need_freight_money;
		return {
			'free_freight_money': freeFreightMoney,
			'need_freight_money': needFreightMoney
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.setFreightValue(property, value);
	},

	onSubmit: function(){
		var freeFreightMoney = this.state.free_freight_money;
		var needFreightMoney = this.state.need_freight_money;
		var reg = /^\+?[0-9][0-9]*$/;
		var reg_2 = /^\+?[1-9][0-9]*$/;
		if(freeFreightMoney.length>0 && !reg_2.test(freeFreightMoney)){
			Reactman.PageAction.showHint('error', '请输入大于或等于0的整数!');
			return;
		}
		if(!reg.test(needFreightMoney)){
			Reactman.PageAction.showHint('error', '请输入大于0的整数!');
			return;
		}
		Action.saveSalePhone(freeFreightMoney,needFreightMoney);
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	render:function(){
		return (
			<div className="xui-newProduct-page xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset style={{paddingTop:'20px'}}>
						<span style={{display:'inline-block'}}>全店满</span>
						<Reactman.FormInput label="" type="text" name="free_freight_money" value={this.state.free_freight_money} onChange={this.onChange} />
						<span style={{marginLeft:'20px'}}>元包邮，否则收取统一运费</span>
						<Reactman.FormInput label="" type="text" name="need_freight_money" value={this.state.need_freight_money} onChange={this.onChange} validate="require-int"/>
						<span style={{display:'inline-block',marginLeft:'22px'}}>元</span>
					</fieldset>
					<fieldset style={{position:'relative'}} className="save-btn">
						<Reactman.FormSubmit onClick={this.onSubmit} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = FreightPage;
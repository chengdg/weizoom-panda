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
		var needFreightMoney = W.need_freight_money=='-1'?'':W.need_freight_money;
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
						<Reactman.FormInput label="全店满消费免运费(元)" type="text" name="free_freight_money" value={this.state.free_freight_money} onChange={this.onChange} validate="require-float"/>
						<Reactman.FormInput label="否则收取统一运费(元)" type="text" name="need_freight_money" value={this.state.need_freight_money} onChange={this.onChange} validate="require-float"/>
					</fieldset>
					<fieldset style={{position:'relative'}}>
						<Reactman.FormSubmit onClick={this.onSubmit} />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = FreightPage;
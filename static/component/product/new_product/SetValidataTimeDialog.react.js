/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:SetValidataTimeDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./SetValidataTime.css');

var SetValidataTimeDialog = Reactman.createDialog({

	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		console.log(property, value);
		Action.updateProduct(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	cancleValidTime: function(modelId){
		Action.cancleValidTime(modelId);
		console.log(modelId);
		this.closeDialog();
	},
	
	render:function(){
		var modelId = this.props.data.modelId;
		return (
			<div className="valid-time">
				<Reactman.FormDateTimeInput label="有效期:" name={"valid_time_from_"+modelId} value={this.state["valid_time_from_"+modelId]} readOnly onChange={this.onChange} />
				<Reactman.FormDateTimeInput label="" name={"valid_time_to_"+modelId} value={this.state["valid_time_to_"+modelId]} readOnly onChange={this.onChange} />
				<a href="javascript:void(0);" className="btn btn-success fr ml100"><span onClick={this.cancleValidTime.bind(this,modelId)}>取消</span></a>
			</div>
		)
	}
})

module.exports = SetValidataTimeDialog;
/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:lookProductModelDetail');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var lookProductModelDetail = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	render: function() {
		var _this = this;
		var model_values = this.state.model_values;
		var model_names = this.state.model_names;

		var model_value_tr = model_values.map(function(model,index){
			var td = model.propertyValues.map(function(value,index){
				return(
					<td key={index}>{value.name}</td>
				)
			})

			return(
				<tr key={index} ref={model.modelId}>
					{td}
					<td>
						{_this.state["clear_price_"+model.modelId]}
					</td>
					<td>
						{_this.state["product_weight_"+model.modelId]}
					</td>
					<td>
						{_this.state["product_store_"+model.modelId]}
					</td>
				</tr>
			)

		})
		var th = model_names.map(function(name,index){
			return(
				<th key={index}>{name.name}</th>
			)
		})
		return(
			<div>
				<div>
					<table className="table table-bordered" style={{margin:'0 auto',width:'80%',marginBottom:'10px'}}>
						<thead>
							<tr>
								{th}
								<th>结算价格(元)</th>
								<th>重量(Kg)</th>
								<th>库存</th>
							</tr>
						</thead>
						<tbody>
						{model_value_tr}
						</tbody>
					</table>
				</div>
			</div>
		)
	}
});
module.exports = lookProductModelDetail;
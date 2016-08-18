/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data:ProductModelList');

var React = require('react');
var ReactDOM = require('react-dom');

var ProductModel = require('./ProductModel.react');
var Action = require('./Action');

var ProductModelList = React.createClass({
	getInitialState: function() {
		return {
			'models': this.props.value
		}
	},

	onChangeModel: function(value, event) {
		var model = this.state.models[value.index];
		this.callChangeHandler();
	},

	callChangeHandler: function() {
		var event = {target: ReactDOM.findDOMNode(this)}
		
		if (this.props.onChange) {
			this.props.onChange(this.state.models, event);
		}
	},

	render:function(){
		var models = this.props.value;
		var cModels = '';
		if (models) {
			var _this = this;
			cModels = models.map(function(model, index) {
				return (
					<ProductModel model={model} index={index} key={index} onChange={_this.onChangeModel} />
				)
			});
		}

		return (
		<div name={this.props.name}>
			{cModels}
		</div>
		)
	}
})
module.exports = ProductModelList;
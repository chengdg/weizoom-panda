/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:outline.data:ProductModel');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;

var Action = require('./Action');
var Constant = require('./Constant')

var ProductModel = React.createClass({
	getInitialState: function() {
		var model = this.props.model;
		return {
			index: this.props.index,
			name: model.name
		};
	},

	onChange: function(id, value,event) {
		var property = event.target.getAttribute('name');
		var models = this.props.models;
		Action.updateCatalog(property, value,  models, this.props.index);
	},

	onClickDelete: function(event) {
		if (this.props.onDelete) {
			this.props.onDelete(this.props.index);
		}
	},

	render:function(){
		var model = this.props.model;
		return (
			<div>
				<FormInput label="资质名称:" type="text" name='name' validate="require-string" placeholder="" value={model.name} onChange={this.onChange.bind(this,model.id)} />
				<a className="btn btn-default ml20" style={{'verticalAlign':'top'}} onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></a>
			</div>
		)
	}
})
module.exports = ProductModel;
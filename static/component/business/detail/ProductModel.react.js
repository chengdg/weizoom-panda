/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:business.detail:ProductModel');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Action = require('./Action');
var Constant = require('./Constant')

var ProductModel = React.createClass({
	getInitialState: function() {
		var model = this.props.model;
		return {
			index: this.props.index,
			qualification_name: model.qualification_name,
			qualification_time: model.qualification_time,
			qualification_id: model.qualification_id,
			img: model.img
		};
	},

	onChange: function(id, value, event) {
		var property = event.target.getAttribute('name');
		var model = this.props.model;
		Action.updateCatalog(property, value,  model, id);
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
				<Reactman.FormImageUploader label={model.qualification_name} name="img" value={model.img} onChange={this.onChange.bind(this,model.qualification_id)} max={1} />
				<Reactman.FormDateTimeInput label='有效期:' name="qualification_time" value={model.qualification_time} onChange={this.onChange.bind(this,model.qualification_id)} />
			</div>
		)
	}
})
module.exports = ProductModel;
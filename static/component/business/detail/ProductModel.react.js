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

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		this.state[property] = value;

		if (this.props.onChange) {
			this.props.onChange(this.state, event);
		}
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
				<Reactman.FormImageUploader label={model.qualification_name} name="name" value={model.img} onChange={this.onChange} max={1} />
				<Reactman.FormDateTimeInput label='有效期:' name="business_license_time" value={model.qualification_time} onChange={this.onChange} />
			</div>
		)
	}
})
module.exports = ProductModel;
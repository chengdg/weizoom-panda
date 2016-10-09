/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:NewConfigPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var DefaultPostagePage = require('./DefaultPostagePage.react');
var SpecialPostagePage = require('./SpecialPostagePage.react');
var FreePostagePage = require('./FreePostagePage.react');
require('./style.css');
var W = Reactman.W;

var NewConfigPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function() {
		this.setState(Store.getData());
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	render:function(){
		return (
			<div>
				<div className="xui-formPage">
					<form className="form-horizontal mt15 pt30">
						<Reactman.FormInput label="模板名称:" type="text" name="product_name" value={this.state.product_name} onChange={this.onChange} placeholder="最多30个字" />
						<div className="pl90">运送方式：除特殊地区外，其余地区的运费采用“默认运费”</div>
					</form>
				</div>
				<div className="mt15 xui-postageConfig-postageListPage">
					<DefaultPostagePage />
					<SpecialPostagePage />
					<FreePostagePage />
				</div>
			</div>
		)
	}
});

module.exports = NewConfigPage;
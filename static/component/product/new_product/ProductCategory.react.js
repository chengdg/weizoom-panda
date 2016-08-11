/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:ProductModelInfo');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var AddProductModelDialog = require('./AddProductModelDialog.react');
var AddProductCategoryDialog = require('./AddProductCategoryDialog.react');
var SetValidataTimeDialog = require('./SetValidataTimeDialog.react');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./ProductModelInfo.css');

var ProductCategory = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(){
		console.log(Store.getData())
		this.setState(Store.getData());

	},

	addProductCatelog: function(){
		Reactman.PageAction.showDialog({
			title: "添加类目",
			component: AddProductCategoryDialog,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},



	render: function() {
		return(
		    <div style={{paddingLeft:'180px',marginBottom:'10px'}}>
		        <a  className="btn btn-success mr40 xa-submit xui-fontBold" onClick={this.addProductCategory}>选择类目</a>
		    </div>
		)
	}
});
module.exports = ProductCategory;
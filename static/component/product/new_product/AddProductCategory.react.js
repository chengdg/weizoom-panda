/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:AddProductModelDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./modelDialogStyle.css');
require('./CategoryStyle.css');

var AddProductCategory = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {

		};
	},

	onChange: function(value, event) {

	},

	onChangeStore: function(){
		this.setState({
			first_levels: Store.getCategory()['first_levels'],
			second_levels: Store.getCategory()['second_levels'],
		});
	},

	chooseProductModelValue: function(value_id){
	},

	saveModelValue: function(){
	},


	render:function(){
	    var first_levels = this.state.first_levels;
		var second_levels = this.state.second_levels;
	    var first_levels_list = '暂无分类';

		var second_level_list = '暂无分类';
	    return(

			<div className="mt15 xui-product-productListPage">
				<ul className='category-ul'>
					{first_levels_list}
				</ul>
				<div className="erow"><div id="demo"></div></div>
				<ul className='category-ul' style={{marginLeft:'0px'}}>
					{second_level_list}
				</ul>

			</div>
			)
	}
})
module.exports = AddProductCategory;
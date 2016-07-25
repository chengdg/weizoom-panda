/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:AddProductCategoryDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./CategoryStyle.css');

var AddProductCategoryDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'first_levels': Store.getCategory().first_levels,
			'second_levels': Store.getCategory().second_levels
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		console.log(Store.getCategory(),"====444==");
		this.setState({
			first_levels: Store.getCategory()['first_levels'],
			second_levels: Store.getCategory()['second_levels']
		});
	},

	chooseSecondLevel: function(first_id){
		console.log(first_id)
		Action.chooseSecondLevel(first_id);
	},

	render:function(){
		var first_levels = this.state.first_levels;
		var _this = this;
		console.log(first_levels,"====3333===");
		var second_levels = this.state.second_levels;
		var first_levels_list = '';
		var second_level_list = '';
		if(first_levels){
			first_levels_list = first_levels.map(function(first_level,index){
				var style = {};
				style['style'] = {}
				if(first_level.is_choose==1){
					style['style'] = {background: '#AAD7FD'};
				}
				return(
						<li key={index} style={style['style']}>
							<a href='javascript:void(0);' style={{color:'#FFF'}} onClick={_this.chooseSecondLevel.bind(null,first_level.id)}>{first_level.name}</a>
						</li>
					)
				});
		}
		if(second_levels){
			second_level_list = second_levels.map(function(second_level,index){
				return(
					<li key={index} style={{color:'#FFF'}}>
						<a href='javascript:void(0);' style={{color:'#FFF'}}>{second_level.name}</a>
					</li>
				)
			});
		}
		
		
		return (
			<div className="mt15 xui-product-productListPage">
				<ul className='category-ul'>
					{first_levels_list}
				</ul>
				<ul className='category-ul'>
					{second_level_list}
				</ul>
			</div>
		)
	}
})
module.exports = AddProductCategoryDialog;
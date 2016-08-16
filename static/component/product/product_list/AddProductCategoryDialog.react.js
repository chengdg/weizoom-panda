/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:AddProductCategoryDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./CategoryStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./CategoryStyle.css');

var AddProductCategoryDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'first_levels': Store.getCategory().first_levels,
			'second_levels': Store.getCategory().second_levels,
			'second_id': Store.getCategory().second_id
		};
	},

	onChangeStore: function(){
		this.setState({
			first_levels: Store.getCategory()['first_levels'],
			second_levels: Store.getCategory()['second_levels'],
			second_id: Store.getCategory()['second_id']
		});
	},

	changeSecondLevel: function(first_id){
		console.log(first_id)
		Action.changeSecondLevel(first_id);
	},

	chooseSecondLevel: function(second_id){
		console.log(second_id)
		Action.chooseSecondLevel(second_id);
	},

	addProduct: function(){
		var second_id = this.state.second_id;
		if(second_id==0){
			Reactman.PageAction.showHint('error', '请选择商品分类！');
			return;
		}
		W.gotoPage('/product/new_product/?second_level_id='+second_id);
	},

	render:function(){
		var first_levels = this.state.first_levels;
		var _this = this;
		var second_levels = this.state.second_levels;
		var first_levels_list = '暂无分类';
		var second_level_list = '暂无分类';
		if(first_levels){
			first_levels_list = first_levels.map(function(first_level,index){
				var bgStyle = {};
				bgStyle['bg_style'] = {}
				bgStyle['c_style'] = {}
				if(first_level.is_choose==1){
					bgStyle['bg_style'] = {background: 'rgba(40, 147, 224, 0.77)'};
					bgStyle['c_style'] = {color:'#FFF'};
				}else{
					bgStyle['c_style'] = {color:'#000'};
				}
				return(
						<li key={index} style={bgStyle['bg_style']}>
							<a href='javascript:void(0);' style={bgStyle['c_style']} onClick={_this.changeSecondLevel.bind(null,first_level.id)}>{first_level.name}</a>
						</li>
					)
				});
		}
		if(second_levels){
			second_level_list = second_levels.map(function(second_level,index){
				var bgStyle = {};
				bgStyle['bg_style'] = {}
				bgStyle['c_style'] = {}
				if(second_level.is_choose==1){
					bgStyle['bg_style'] = {background: 'rgba(40, 147, 224, 0.77)'};
					bgStyle['c_style'] = {color:'#FFF'};
				}else{
					bgStyle['c_style'] = {color:'#000'};
				}
				return(
					<li key={index} style={bgStyle['bg_style']}>
						<a href='javascript:void(0);' style={bgStyle['c_style']} onClick={_this.chooseSecondLevel.bind(null,second_level.id)}>{second_level.name}</a>
					</li>
				)
			});
		}
		
		
		return (
			<div className="mt15 xui-product-productListPage">
				<ul className='category-ul'>
					{first_levels_list}
				</ul>
				<div className="erow"><div id="demo"></div></div>
				<ul className='category-ul' style={{marginLeft:'0px'}}>
					{second_level_list}
				</ul>
				<a href="javascript:void(0);" className="btn btn-success edit-product" onClick={this.addProduct}>下一步，编辑商品</a>
			</div>
		)
	}
})
module.exports = AddProductCategoryDialog;
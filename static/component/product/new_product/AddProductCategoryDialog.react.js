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
			'first_levels': Store.getData().first_levels,
			'second_levels': Store.getData().second_levels,
			'second_id': Store.getData().second_id
		};
	},

	onChangeStore: function(){
		this.setState({
			first_levels: Store.getData()['first_levels'],
			second_levels: Store.getData()['second_levels'],
			second_id: Store.getData()['second_id']
		});
	},

	changeSecondLevel: function(first_id){
		Action.changeSecondLevel(first_id);
	},

	chooseSecondLevel: function(second_id){
		Action.chooseSecondLevel(second_id);
	},

	saveCatalog: function(firstLevelName, secondLevelName){
		var _this = this;
		var catalogName = firstLevelName + '--' + secondLevelName;
		var secondId = this.state.second_id;
		if(secondId==0){
			Reactman.PageAction.showHint('error', '请选择商品分类！');
			return;
		}
		Action.saveChooseCatalog(catalogName);
		_.delay(function(){
			_this.closeDialog();
		},200)
	},

	cancleCatalog: function(){
		Action.cancleChooseCatalog();
	},

	render:function(){
		var firstLevels = this.state.first_levels;
		var _this = this;
		var second_levels = this.state.second_levels;
		var firstLevelsList = '暂无分类';
		var secondLevelList = '暂无分类';
		var firstLevelName = '';
		var secondLevelName = '';
		if(firstLevels){
			firstLevelsList = firstLevels.map(function(first_level,index){
				var bgStyle = {};
				bgStyle['bg_style'] = {}
				bgStyle['c_style'] = {}
				if(first_level.is_choose==1){
					firstLevelName = first_level.name;
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
			secondLevelList = second_levels.map(function(second_level,index){
				var bgStyle = {};
				bgStyle['bg_style'] = {}
				bgStyle['c_style'] = {}
				if(second_level.is_choose==1){
					secondLevelName = second_level.name;
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
			<div className="mt15" style={{paddingLeft: '35px'}}>
				<ul className='category-ul'>
					{firstLevelsList}
				</ul>
				<div className="erow"><div id="demo"></div></div>
				<ul className='category-ul' style={{marginLeft:'0px'}}>
					{secondLevelList}
				</ul>
				<a href="javascript:void(0);" className="btn btn-success mt20 mb20" style={{marginLeft:'190px'}} onClick={this.saveCatalog.bind(this,firstLevelName,secondLevelName)}><span>确定</span></a>
				<a href="javascript:void(0);" className="btn btn-success mt20 mb20" style={{marginLeft:'50px'}} onClick={this.cancleCatalog}><span>取消</span></a>
			</div>
		)
	}
})
module.exports = AddProductCategoryDialog;
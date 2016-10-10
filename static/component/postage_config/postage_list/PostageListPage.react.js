/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.postage_list:PostageListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var PostageListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	addPostageTemplate: function(){
		W.gotoPage('/postage_config/new_config/');
	},

	render:function(){
		var postages = W.postages;
		var postageId = this.state.postageId;
		var tableList = JSON.parse(postages).map(function(postage, index){
			//判断是否为默认
			var isUsed = postage.isUsed;
			if(postageId != 0) {
				isUsed = postageId==postage.postageId? true: false;
			}

			return(
				<div key={index}><TableListPage postageId={postage.postageId} hasSpecialConfig={postage.hasSpecialConfig} hasFreeConfig={postage.hasFreeConfig} isUsed={isUsed}/></div>
			)
		})

		return (
			<div className="mt15 xui-postageConfig-postageListPage">
				{tableList}
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="添加新模板" icon="plus" onClick={this.addPostageTemplate}/>
				</Reactman.TableActionBar>
			</div>
		)
	}
})

var TableListPage = React.createClass({
	getInitialState: function() {
		return ({});
	},

	setHasUsed: function(postageId) {
		Action.setHasUsed(postageId);
	},

	deletePostage: function(postageId, event) {
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: '确定删除么?',
			confirm: _.bind(function() {
				Action.deletePostage(postageId);
			}, this)
		});
	},

	updatePostage: function(postageId){
		W.gotoPage('/postage_config/new_config/?postage_id='+postageId);
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" target="_blank" >编辑</a>
					<a className="btn btn-link btn-xs" target="_blank" >删除</a>
				</div>
			);
		}else {
			return value;
		}
	},

	render:function(){
		var postageId = this.props.postageId;
		var hasSpecialConfig = this.props.hasSpecialConfig;
		var hasFreeConfig = this.props.hasFreeConfig;

		var title = '';
		var isUsed = this.props.isUsed;
		title = hasSpecialConfig? title+'特殊商品模板': '默认模板';
		title = hasFreeConfig? title+'(已设置包邮条件)': title;
		var setBtn = isUsed? <a style={{color:'red', marginLeft:'10px'}}>(默认)</a>: <a href="javascript:void(0);" style={{marginLeft:'10px'}} onClick={this.setHasUsed.bind(this, postageId)}>设为默认</a>;

		var productsResource = {
			resource: 'postage_config.postage_list',
			data: {
				page: 1,
				postage_id: postageId
			}
		};

		return (
			<div>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<div className="xui-set-title">{title}{setBtn}</div>
						<div className="xui-modify-delete-btn">
							<a href="javascript:void(0);" className="ml10 mr10" onClick={this.updatePostage.bind(this, postageId)}>修改</a>
							<span>|</span>
							<a href="javascript:void(0);" className="ml10" onClick={this.deletePostage.bind(this, postageId)}>删除</a>
						</div>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="运送方式" field="postageMethod" />
						<Reactman.TableColumn name="运送到" field="postageDestination" />
						<Reactman.TableColumn name="首重(kg)" field="firstWeight" />
						<Reactman.TableColumn name="运费(元)" field="firstWeightPrice" />
						<Reactman.TableColumn name="续重(kg)" field="addedWeight" />
						<Reactman.TableColumn name="续费(元)" field="addedWeightPrice" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})

module.exports = PostageListPage;
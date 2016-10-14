/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.postage_list:TableListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var TableListPage = React.createClass({
	getInitialState: function() {
		return ({});
	},

	setHasUsed: function(postageId) {
		Action.setHasUsed(postageId);
	},

	deletePostage: function(postageId, event) {
		var isUsed = this.props.isUsed;
		var postageTemplateCount = this.props.postageTemplateCount;
		if(postageTemplateCount == 1){
			Reactman.PageAction.showHint('error', '操作失败，模板至少保留一个 !');
			return;
		}

		if(isUsed){
			Reactman.PageAction.showHint('error', '操作失败，默认模板无法删除，请先将其他模板设为默认 !');
			return;
		}

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
		if (field === 'postageDestination') {
			return (
				<div className="xui-destination" title={value}>{value}</div>
			);
		}else {
			return value;
		}
	},

	render:function(){
		var postageId = this.props.postageId;
		var hasSpecialConfig = this.props.hasSpecialConfig;
		var hasFreeConfig = this.props.hasFreeConfig;

		var title = this.props.postageName;
		var isUsed = this.props.isUsed;
		// title = hasSpecialConfig? title+'特殊商品模板': '默认模板';
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
						<Reactman.TableColumn name="运送到" field="postageDestination" width="300"/>
						<Reactman.TableColumn name="首重(kg)" field="firstWeight" />
						<Reactman.TableColumn name="运费(元)" field="firstWeightPrice" />
						<Reactman.TableColumn name="续重(kg)" field="addedWeight" />
						<Reactman.TableColumn name="续费(元)" field="addedWeightPrice" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})

module.exports = TableListPage;
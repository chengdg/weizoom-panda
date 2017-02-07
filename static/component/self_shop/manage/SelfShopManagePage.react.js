/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:self_shop.manage:SelfShopManagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var AddSelfShopDialog = require('./AddSelfShopDialog.react');
require('./style.css');
var W = Reactman.W;

var SelfShopManagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function() {
		this.setState(Store.getData());
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	addSelfShop:function(){
		Reactman.Resource.get({
			resource: 'self_shop.get_all_unsynced_self_shops',
			data: {
				status:'new'
			},
			success: function(data) {
				var options = data.rows;
				Reactman.PageAction.showDialog({
					title: "添加自营平台",
					component: AddSelfShopDialog,
					data: {
						options: options,
						selfInfo:{},
						curModel: 'put'
					},
					success: function() {
						Action.updateSelfShopDialog();
					}
				});
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			},
			scope: this
		})
	},
	updateSelfInfo:function(selfInfo){
		Reactman.Resource.get({
			resource: 'self_shop.get_all_unsynced_self_shops',
			data: {
				status:'all'
			},
			success: function(data) {
				var options = data.rows;
				Reactman.PageAction.showDialog({
					title: "添加自营平台",
					component: AddSelfShopDialog,
					data: {
						options: options,
						selfInfo:selfInfo,
						curModel: 'post'
					},
					success: function() {
						Action.updateSelfShopDialog();
					}
				});
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			},
			scope: this
		})
	},

	//同步自营平台现有商品
	chooseSyncSelfShopProduct: function(userName){
		Action.syncSelfShopProduct(userName);
	},
		
	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			if(data.isSynced){
				return (
					<div>
						<a className="btn btn-link btn-xs ml15" onClick={this.updateSelfInfo.bind(this,data)}>修改</a>
					</div>
				);
			}else{
				return (
					<div>
						<a className="btn btn-link btn-xs" onClick={this.chooseSyncSelfShopProduct.bind(this,data['userName'])}>批量同步</a>
						<a className="btn btn-link btn-xs ml15" onClick={this.updateSelfInfo.bind(this,data)}>修改</a>
					</div>
				);
			}
		}else if(field === 'settlementType'){
			var settlementTypeName = ['固定扣点','毛利分成','固定底价']
			var curSettlementTypeName = settlementTypeName[data['settlementType']-1]
			return (
					<div>
						{curSettlementTypeName}
					</div>
				);
		}else if(field === 'splitRatio'){
			if (data['settlementType'] == 2){
				return (
					<div>
						X*{data['splitRatio']}%
					</div>
				);
			}else if(data['settlementType'] == 1){
				return (
					<div>
						0%
					</div>
				);
			}else{
				return (
					<div>
						{data['splitRatio']}%
					</div>
				);
			}
			
		}else{
			return value;
		}
	},
	render:function(){
		var productsResource = {
			resource: 'self_shop.manage',
			data: {
				page: 1
			}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加自营平台" icon="plus" onClick={this.addSelfShop}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="平台名称" field="selfShopName" width="200px"/>
						<Reactman.TableColumn name="user_name" field="userName" />
						<Reactman.TableColumn name="结算类型" field="settlementType" />
						<Reactman.TableColumn name="分成比例" field="splitRatio" />
						<Reactman.TableColumn name="操作" field="action" width="300px"/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = SelfShopManagePage;
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
	},

	addSelfShop:function(){
		Reactman.PageAction.showDialog({
			title: "添加自营平台",
			component: AddSelfShopDialog,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			if(data.isSynced){
				return (
					<div>已同步</div>
				);
			}else{
				return (
					<div>
						<a className="btn btn-link btn-xs">批量同步现有商品</a>
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
						<Reactman.TableColumn name="操作" field="action" width="100px"/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = SelfShopManagePage;
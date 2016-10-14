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

var PostageConfigManagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function() {
		this.setState(Store.getData());
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	addPostageConfig:function(){
		W.gotoPage('/postage_config/new_template');
	},

	//同步自营平台现有商品
	chooseSyncSelfShopProduct: function(userName){
		Action.syncSelfShopProduct(userName);
	},

	rowFormatter: function(field, value, data) {

	},
	render:function(){
		var productsResource = {
			resource: 'postage_config.template',
			data: {
				page: 1
			}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加运费模板" icon="plus" onClick={this.addPostageConfig}/>
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
module.exports = PostageConfigManagePage;
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
		return ({});
	},

	onChangeStore: function() {
		this.setState(Store.getData());
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	addPostageTemplate: function(){
		W.gotoPage('/postage_config/new_config/');
	},

	render:function(){
		var productsResource = {
			resource: 'postage_config.postage_list',
			data: {
				page: 1
			}
		};
		var postages = W.postages;
		console.log(JSON.parse(postages),"=========");
		var tableList = JSON.parse(postages).map(function(postage, index){
			console.log(postage,"-------")
			return(
				<div key={index}><TableListPage postageId={postage.postage_id} /></div>
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
		Store.addListener(this.onChangeStore);
		return ({});
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
		var productsResource = {
			resource: 'postage_config.postage_list',
			data: {
				page: 1,
			}
		};
		console.log("--ss------");
		return (
			<div>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<div>默认模板（已设置包邮条件）</div>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="运送方式" field="postage_method" />
						<Reactman.TableColumn name="运送到" field="postage_destination" />
						<Reactman.TableColumn name="首重(kg)" field="postage_weight" />
						<Reactman.TableColumn name="运费(元)" field="postage_price" />
						<Reactman.TableColumn name="续重(kg)" field="over_weight" />
						<Reactman.TableColumn name="续费(kg)" field="over_price" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})

module.exports = PostageListPage;
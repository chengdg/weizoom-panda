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

var TableListPage = require('./TableListPage.react');
var QQOnlineService = require('../.././qq_online/online/QQOnlineService.react');

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
		var serviceTel = W.serviceTel;
		var serviceQQFirst = W.serviceQQFirst;
		var serviceQQSecond = W.serviceQQSecond;
		var postageId = this.state.postageId;
		var postageTemplateCount = JSON.parse(postages).length;
		var tableList = JSON.parse(postages).map(function(postage, index){
			//判断是否为默认
			var isUsed = postage.isUsed;
			if(postageId != 0) {
				isUsed = postageId==postage.postageId? true: false;
			}

			return(
				<div key={index}>
					<TableListPage 
						postageId={postage.postageId} 
						postageName={postage.postageName} 
						hasSpecialConfig={postage.hasSpecialConfig} 
						hasFreeConfig={postage.hasFreeConfig} 
						postageTemplateCount={postageTemplateCount}
						isUsed={isUsed} />
				</div>
			)
		})

		return (
			<div className="mt15 xui-postageConfig-postageListPage">
				<div> <QQOnlineService serviceQQFirst={serviceQQFirst} serviceQQSecond={serviceQQSecond} serviceTel={serviceTel}/></div>
				{tableList}
				<Reactman.TableActionBar>
					<Reactman.TableActionButton text="添加新模板" icon="plus" onClick={this.addPostageTemplate}/>
				</Reactman.TableActionBar>
			</div>
		)
	}
})

module.exports = PostageListPage;
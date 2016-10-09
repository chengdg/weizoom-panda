/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:NewConfigPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var DefaultPostagePage = require('./DefaultPostagePage.react');
var SpecialPostagePage = require('./SpecialPostagePage.react');
var FreePostagePage = require('./FreePostagePage.react');
var DefaultPostageStore = require('./DefaultPostageStore');
var SpecialPostageStore = require('./SpecialPostageStore');
var FreePostageStore = require('./FreePostageStore');

require('./style.css');
var W = Reactman.W;

var NewConfigPage = React.createClass({
	getInitialState: function() {
		return ({});
	},

	savePostage: function(){
		var defaultData = DefaultPostageStore.getData();
		var specialData = SpecialPostageStore.getData();
		var freeData = FreePostageStore.getData();
		console.log(defaultData,specialData,freeData,"++++++++");
	},

	render:function(){
		return (
			<div>
				<div className="xui-formPage">
					<form className="form-horizontal mt15 pt30">
						<Reactman.FormInput label="模板名称:" type="text" name="product_name" value={this.state.product_name} onChange={this.onChange} placeholder="最多30个字" />
						<div className="pl90">运送方式：除特殊地区外，其余地区的运费采用“默认运费”</div>
					</form>
				</div>
				<div className="mt15 xui-postageConfig-postageListPage">
					<DefaultPostagePage />
					<SpecialPostagePage />
					<FreePostagePage />
				</div>
				<div className="pl90 mt15">
					<a className="btn btn-success mr40 xa-submit xui-fontBold" style={{width:'100px'}} href="javascript:void(0);" onClick={this.savePostage}>保存</a>
				</div>
			</div>
		)
	}
});

module.exports = NewConfigPage;
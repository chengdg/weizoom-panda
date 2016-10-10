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
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateConfig(property, value);
	},

	savePostage: function(){
		var data = {}
		var configData = Store.getData();
		var defaultData = DefaultPostageStore.getData();
		var specialData = SpecialPostageStore.getData();
		var freeData = FreePostageStore.getData();
		data = _.extend(configData, defaultData);
		if(specialData.hasSpecialPostage[0] == '1'){
			data = _.extend(data, specialData);
		}
		if(freeData.hasFreePostage[0] == '1'){
			data = _.extend(data, freeData);
		}
		console.log(data,"==========");
		Action.savePostage(data);
	},

	render:function(){
		return (
			<div>
				<div className="xui-formPage">
					<form className="form-horizontal mt15 pt30">
						<Reactman.FormInput label="模板名称:" type="text" name="postageName" value={this.state.postageName} onChange={this.onChange} validate="require-string" />
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
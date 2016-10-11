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
		var data = {};
		var is_upass = true;
		var configData = Store.getData();
		var defaultData = DefaultPostageStore.getData();
		var specialData = SpecialPostageStore.getData();
		var freeData = FreePostageStore.getData();
		data = _.extend(configData, defaultData);
		
		if(specialData.hasSpecialPostage[0] == '1'){
			_.each(specialData.specialPostages, function(postages){
				is_upass = postages['addedWeight'] == ''? false : is_upass;
				is_upass = postages['addedWeightPrice'] == ''? false : is_upass;
				is_upass = postages['firstWeight'] == ''? false : is_upass;
				is_upass = postages['firstWeightPrice'] == ''? false : is_upass;
			});
			data = _.extend(data, specialData);
		}else{
			data['hasSpecialPostage'] = false;
		}

		if(freeData.hasFreePostage[0] == '1'){
			_.each(freeData.freePostages, function(postages){
				is_upass = postages['conditionValue'] == ''? false : true;
				is_upass = postages['conditionValue'] == ''? false : true;
			});
			data = _.extend(data, freeData);
		}else{
			data['hasFreePostage'] = false;
		}
		console.log(is_upass,"==========");
		if(!is_upass){
			Reactman.PageAction.showHint('error', '请填写输入框！');
		}
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
				<div className="pl90 mt15 xui-submit-btn">
					<Reactman.FormSubmit onClick={this.savePostage} />
				</div>
			</div>
		)
	}
});

module.exports = NewConfigPage;
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

	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateConfig(property, value);
	},

	savePostage: function() {
		var data = {};
		var isUpass = true;//是否为空
		var isValidate = true;//是否是两位小数
		var isDestination = true;//地区是否为空
		var input_reg = /^(0|([1-9]\d*))(\.\d{1,2})?$/;
		var configData = Store.getData();
		var defaultData = DefaultPostageStore.getData();
		var specialData = SpecialPostageStore.getData();
		var freeData = FreePostageStore.getData();
		data = _.extend(configData, defaultData);
		
		if(specialData.hasSpecialPostage[0] == '1') {
			_.each(specialData.specialPostages, function(postages) {
				isUpass = postages['addedWeight'] == ''? false : isUpass;
				isUpass = postages['addedWeightPrice'] == ''? false : isUpass;
				isUpass = postages['firstWeight'] == ''? false : isUpass;
				isUpass = postages['firstWeightPrice'] == ''? false : isUpass;

				isValidate = input_reg.test(postages['addedWeight']) == false? false: isValidate;
				isValidate = input_reg.test(postages['addedWeightPrice']) == false? false: isValidate;
				isValidate = input_reg.test(postages['firstWeight']) == false? false: isValidate;
				isValidate = input_reg.test(postages['firstWeightPrice']) == false? false: isValidate;

				isDestination = postages['selectedIds'].length == 0? false : isDestination;
			});
			data = _.extend(data, specialData);
		}else{
			data['hasSpecialPostage'] = false;
		}

		if(freeData.hasFreePostage[0] == '1') {
			_.each(freeData.freePostages, function(postages) {
				isUpass = postages['conditionValue'] == ''? false : true;
				isValidate = input_reg.test(postages['conditionValue']) == false? false: isValidate;
				isDestination = postages['selectedIds'].length == 0? false : isDestination;
			});
			data = _.extend(data, freeData);
		}else {
			data['hasFreePostage'] = false;
		}

		if(!isUpass) {
			Reactman.PageAction.showHint('error', '请填写输入框 !');
			return;
		}

		if(!isValidate) {
			Reactman.PageAction.showHint('error', '格式不正确，请输入3.14或5这样的数字 !');
			return;
		}

		if(!isDestination) {
			Reactman.PageAction.showHint('error', '请选择区域 !');
			return;
		}

		Action.savePostage(data);
	},

	render:function() {
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
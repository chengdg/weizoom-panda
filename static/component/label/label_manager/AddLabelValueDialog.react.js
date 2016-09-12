/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:label.label_manager:AddLabelValueDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddLabelValueDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'images': [],
			'labelValue': '',
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		// Action.addProductModelValue(property, value);
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	onSubmit: function(){
		var _this = this;
		var labelId = this.props.data.labelId;
		var labelValue = this.state.labelValue;
		if(labelValue.length == 0){
			Reactman.PageAction.showHint('error', '最多上传一张图片!');
			return;
		}
		console.log(labelId,labelValue,"=======");
		Action.saveLabelValue(labelId,labelValue);
		setTimeout(function() {
		 	_this.closeDialog();
		}, 500);
	},

	onBeforeCloseDialog: function() {
		var labelValue = this.state.labelValue;
		var labelId = this.props.data.labelId;
		var _this = this;
		if (labelValue.length == 0) {
			Reactman.PageAction.showHint('error', '不能关闭对话框');
		} else {
			Reactman.Resource.put({
				resource: 'label.label_value',
				data: {
					label_id: labelId,
					label_value: labelValue
				},
				success: function() {
					Reactman.PageAction.showHint('success', '添加成功');
					setTimeout(function() {
					 	_this.closeDialog();
					}, 500);
				},
				error: function() {
					Reactman.PageAction.showHint('error', '评论失败!');
				},
				scope: this
			})
		}
	},

	render:function(){
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormInput label="名称:" type="text" name="labelValue" value={this.state.labelValue} onChange={this.onChange} validate="require-string" />
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddLabelValueDialog;
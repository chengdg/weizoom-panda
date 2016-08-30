/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_updated:UnPassDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var _ = require('underscore');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./UnPassDialog.css')

var UnPassDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var productId = this.props.data.product_id;
		return {
			product_id: productId,
			reasons: Store.getData().reasons,
			custom_reason: ''
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateReason(property, value);
	},

	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState({
			reasons: infomations['reasons'],
			custom_reason: infomations['custom_reason']
		})
	},

	chooseUnpassReason: function(event){
		var reason = event.target.getAttribute('data-reason');
		Action.chooseUnpassReason(reason);
	},

	cancleChecked: function(){
		this.setState({
			reasons: [],
			custom_reason: ''
		})
		this.closeDialog();
	},

	refused: function() {
		var _this = this;
		var reasons = this.state.reasons;
		var productId = this.state.product_id;
		var custom_reason = this.state.custom_reason;//自定义原因
		if(custom_reason.length>0 && reasons.length>0){
			reasons.push(custom_reason);
			reasons = reasons.join(',');
		}else if(custom_reason.length>0){
			reasons = custom_reason;
		}else{
			reasons = reasons.join(',');
		}
		if(reasons.length==0){
			Reactman.PageAction.showHint('error', '请添加驳回原因!');
			return;
		}
		Action.refused(productId, reasons);
		_.delay(function(){
			_this.closeDialog();
		},500)
		// Reactman.Resource.post({
		// 	resource: 'product.product_updated',
		// 	data: {
		// 		reasons: reasons,
		// 		product_id: productId
		// 	},
		// 	success: function() {
		// 		this.closeDialog();
		// 		_.delay(function(){
		// 			Reactman.PageAction.showHint('success', '驳回成功');
		// 		},500);
		// 	},
		// 	error: function(data) {
		// 		Reactman.PageAction.showHint('error', data.errMsg);
		// 	},
		// 	scope: this
		// })
	},

	render:function(){
		var reasons = this.state.reasons;
		var firstReason = {};
		var secondReason = {};
		var thridReason = {}

		for (var i = 0; i < reasons.length; i++) {
			if (reasons[i] === '资质不全') {
				firstReason = {background: '#009DD9', color:'#FFF'};
			}
			if (reasons[i] === '投诉率较高') {
				secondReason = {background: '#009DD9', color:'#FFF'};
			}
			if (reasons[i] === '商品信息不清晰') {
				thridReason = {background: '#009DD9', color:'#FFF'};
			}
		}

		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<ul className='xui-un-pass-reasons'>
							<li className="xi-un-pass-reason" style={firstReason} data-reason="资质不全" onClick={this.chooseUnpassReason}>资质不全</li>
							<li className="xi-un-pass-reason" style={secondReason} data-reason="投诉率较高" onClick={this.chooseUnpassReason}>投诉率较高</li>
							<li className="xi-un-pass-reason" style={thridReason} data-reason="商品信息不清晰" onClick={this.chooseUnpassReason}>商品信息不清晰</li>
						</ul>
						<Reactman.FormText label="" type="text" name="custom_reason" value={this.state.custom_reason} onChange={this.onChange} autoFocus={true} inDialog={true} width={380} height={200} />
						<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'190px', managerTop:'20px'}} onClick={this.refused}><span>确定</span></a>
						<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'50px', managerTop:'20px'}} onClick={this.cancleChecked}><span>取消</span></a>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = UnPassDialog;
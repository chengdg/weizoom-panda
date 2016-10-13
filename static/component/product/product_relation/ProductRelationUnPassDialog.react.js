/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_updated:UnPassDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var _ = require('underscore');

var ProductRelationUnPassDialogStore = require('./ProductRelationUnPassDialogStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./ProductRelationUnPassDialog.css')

var ProductRelationUnPassDialog = Reactman.createDialog({
	getInitialState: function() {
		ProductRelationUnPassDialogStore.addListener(this.onChangeStore);
		var productId = this.props.data.product_id;
		return {
			product_id: productId,
			reasons: ProductRelationUnPassDialogStore.getData().reasons,
			custom_reason: ''
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateRejectReason(property, value);
	},

	onChangeStore: function(){
		var infomations = ProductRelationUnPassDialogStore.getData();
		this.setState({
			reasons: infomations['reasons'],
			custom_reason: infomations['custom_reason']
		})
	},

	chooseRejectUnpassReason: function(event){
		var reason = event.target.getAttribute('data-reason');
		Action.chooseRejectUnpassReason(reason);
	},

	cancleChecked: function(){
		Action.cancleCheckedUnpassReason();
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
	},

	render:function(){
		var reasons = this.state.reasons;
		var firstReason = {};
		console.log(reasons);
		for (var i = 0; i < reasons.length; i++) {
			if (reasons[i] === '商品名称不规范，标准格式：品牌名+商品名+包装规格') {
				firstReason = {background: '#009DD9', color:'#FFF'};
			}
		}

		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<ul className='xui-unpass-reasons'>
							<li className="xi-unpass-reason" style={firstReason} data-reason="商品名称不规范，标准格式：品牌名+商品名+包装规格" onClick={this.chooseRejectUnpassReason}>商品名称不规范，标准格式：品牌名+商品名+包装规格</li>
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
module.exports = ProductRelationUnPassDialog;
/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var RevokeSelfShopStore = require('./RevokeSelfShopStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./RevokeSelfShop.css');

var RevokeSyncSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		RevokeSelfShopStore.addListener(this.onChangeStore);
		var productId = this.props.data.product_id;
		return {
			product_id: productId,
			reasons: RevokeSelfShopStore.getData().reasons,
			customReason: ''
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateReason(property, value);
	},

	onChangeStore: function(){
		var infomations = RevokeSelfShopStore.getData();
		this.setState({
			reasons: infomations['reasons'],
			customReason: infomations['customReason']
		})
	},

	productRelation: function(product_ids) {
		var selectSelfShop = this.state.select_self_shop;
		var productId = this.props.data.product_id;
		var productData = [{
			'weizoom_self': selectSelfShop.join(','),//选择的商城
			'product_ids': product_ids//商品id
		}]
		Action.relationFromWeapp(JSON.stringify(productData));
	},

	chooseUnpassReason: function(event){
		var reason = event.target.getAttribute('data-reason');
		Action.chooseUnpassReason(reason);
	},

	cancleChecked: function(){
		Action.cancleChooseReason();
		this.closeDialog();
	},

	refused: function() {
		var _this = this;
		var reasons = this.state.reasons;
		var customReason = this.state.customReason;//自定义原因
		var productStatus = this.props.data.productStatus

		if(customReason.length>10){
			Reactman.PageAction.showHint('error', '自定义原因最多输入10个字,请重新输入!');
			return;
		}
		
		if(customReason.length>0 && reasons.length>0){
			reasons.push(customReason);
			reasons = reasons.join(',');
		}else if(customReason.length>0){
			reasons = customReason;
		}else{
			reasons = reasons.join(',');
		}

		if(reasons.length==0){
			Reactman.PageAction.showHint('error', '请添加驳回原因!');
			return;
		}

		var productId = this.props.data.product_id;
		var productData = [{
			'weizoom_self': '',//选择的商城
			'product_ids': productId,//商品id
			'revoke_reasons': reasons,
			'product_status': productStatus
		}]

		Action.revokeProduct(JSON.stringify(productData));
		_.delay(function(){
			_this.closeDialog();
		},500)
	},

	render: function(){
		var reasons = this.state.reasons;
		var firstReason = {};
		var secondReason = {};
		var thridReason = {}

		for (var i = 0; i < reasons.length; i++) {
			if (reasons[i] === '已过季') {
				firstReason = {background: '#009DD9', color:'#FFF'};
			}
			if (reasons[i] === '供应商停止合作') {
				secondReason = {background: '#009DD9', color:'#FFF'};
			}
			if (reasons[i] === '315黑名单商品') {
				thridReason = {background: '#009DD9', color:'#FFF'};
			}
		}

		return (
			<div className="xui-formPage">
				<div>请标记商品停售的原因:</div>
				<form className="form-horizontal mt15">
					<fieldset>
						<ul className='xui-un-pass-reasons'>
							<li className="xi-un-pass-reason" style={firstReason} data-reason="已过季" onClick={this.chooseUnpassReason}>已过季</li>
							<li className="xi-un-pass-reason" style={secondReason} data-reason="供应商停止合作" onClick={this.chooseUnpassReason}>供应商停止合作</li>
							<li className="xi-un-pass-reason" style={thridReason} data-reason="315黑名单商品" onClick={this.chooseUnpassReason}>315黑名单商品</li>
						</ul>
						<Reactman.FormText label="" type="text" name="customReason" value={this.state.customReason} onChange={this.onChange} placeholder="自定义,10字以内" autoFocus={true} inDialog={true} width={380} height={50} />
						<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'190px', managerTop:'20px'}} onClick={this.refused}><span>确定</span></a>
						<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'50px', managerTop:'20px'}} onClick={this.cancleChecked}><span>取消</span></a>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = RevokeSyncSelfShopDialog;
/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var W = Reactman.W;

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		var options = this.props.data.options;
		var selfInfo = this.props.data.selfInfo;
		var selfUserName = selfInfo.selfShopId || '-1'
		var remark = selfInfo.remark || ''
		var isSync = selfInfo.isSynced ? ['isSync'] :''
		var settlementType = selfInfo.settlementType || 1
		var corpAccount = selfInfo.corpAccount || 1
		var splitRatio = selfInfo.splitRatio || 0
		var riskMoney = selfInfo.riskMoney || 0
		var curModel = this.props.data.curModel;
		var oldWeappUserId = selfInfo.selfShopId
		return {
			selfUserName: selfUserName,
			remark: remark,
			isSync: isSync,
			options: options,
			settlementType : settlementType.toString(),
			splitRatio:splitRatio,
			riskMoney:riskMoney,
			curModel:curModel,
			corpAccount : corpAccount
		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onBeforeCloseDialog: function() {
		if (this.state.selfUserName == '-1') {
			Reactman.PageAction.showHint('error', '请选择自营平台');
		} else {
			var selfShopName = $('#selfUserName').find("option:selected").text();
			//添加自营平台
			if(this.state.curModel =='put'){
				Reactman.Resource.put({
					resource: 'self_shop.manage',
					data: {
						self_shop_name: selfShopName,
						weapp_user_id: this.state.selfUserName, 
						remark: this.state.remark,
						settlement_type: this.state.settlementType,
						corp_account: this.state.corpAccount,
						split_atio: this.state.splitRatio,
						risk_money: this.state.riskMoney,
						is_sync: this.state.isSync.length > 0 ? 'is_sync': ''
					},
					success: function(action) {
						this.closeDialog();
						_.delay(function(){
							Reactman.PageAction.showHint('success', '添加自营平台成功');
						},500);
					},
					error: function(data) {
						Reactman.PageAction.showHint('error', data.errMsg);
					},
					scope: this
				})
			}else{
				Reactman.Resource.post({
					resource: 'self_shop.manage',
					data: {
						self_shop_name: selfShopName,
						weapp_user_id: this.state.selfUserName, 
						remark: this.state.remark,
						settlement_type: this.state.settlementType,
						corp_account: this.state.corpAccount,
						split_atio: this.state.splitRatio,
						risk_money: this.state.riskMoney,
						is_sync: this.state.isSync.length > 0 ? 'is_sync': '',
					},
					success: function(action) {
						this.closeDialog();
						_.delay(function(){
							Reactman.PageAction.showHint('success', '修改自营平台成功');
						},500);
					},
					error: function(data) {
						Reactman.PageAction.showHint('error', data.errMsg);
					},
					scope: this
				})
			}
			
		}
	},

	render:function(){
		var selectable = this.state.curModel == 'put'?true:false
		var optionsForSync = [{
			text: '批量同步已有的商品',
			value: 'isSync',
			selectable: selectable
		}];
		var optionsForsettlementType = [{
			text: '固定扣点',
			value: '1'
		}, {
			text: '毛利分成',
			value: '2'
		}, {
			text: '固定底价',
			value: '3'
		}];
		if(this.state.settlementType == '1'){
			var splitRatioName = '扣点比例:'
		}else if(this.state.settlementType == '2'){
			var splitRatioName = '分成比例:'
		}else{
			var splitRatioName = '同时批量加价:'
		}
		var disabled =this.state.curModel == 'put'?'':'disabled'

		var optionsForcompany = [{
			text: '北京微众文化传媒有限公司',
			value: '1'
		}, {
			text: '北京微众文化传媒有限公司',
			value: '2'
		}, {
			text: '北京微众文化传媒有限公司',
			value: '3'
		}, {
			text: '北京微众文化传媒有限公司',
			value: '4'
		}, {
			text: '北京微众精选电子商务有限公司',
			value: '5'
		}, {
			text: '北京微众中海企业孵化器有限公司',
			value: '6'
		}, {
			text: '北京微众英才电子商务有限公司',
			value: '7'
		}];

		var optionsForaccount = [{
			text: '20000028368800010843909',
			value: '1'
		}, {
			text: '20000028368800009669199',
			value: '2'
		}, {
			text: '20000028368800012875903',
			value: '3'
		}, {
			text: '321190100100179840',
			value: '4'
		}, {
			text: '3211 9010 0100 1973 25',
			value: '5'
		}, {
			text: '11050163510000000014',
			value: '6'
		}, {
			text: '20000032109300011190749',
			value: '7'
		}];

		var optionsForbank = [{
			text: '北京银行清华园支行 ',
			value: '1'
		}, {
			text: '北京银行中关村科技园区支行',
			value: '2'
		}, {
			text: '北京银行友谊支行 ',
			value: '3'
		}, {
			text: '兴业银行股份有限公司北京花园路支行',
			value: '4'
		}, {
			text: '兴业银行股份有限公司北京花园路支行',
			value: '5'
		}, {
			text: '中国建设银行北京中关村南大街支行',
			value: '6'
		}, {
			text: '北京银行友谊支行 ',
			value: '7'
		}];
   
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormSelect label="选择平台:" name="selfUserName" disabled ={disabled} value={this.state.selfUserName} options={this.state.options} onChange={this.onChange}/>
						<div className="account-create-settlement-ype">
							<Reactman.FormRadio label="结算类型:" name="settlementType" value={this.state.settlementType} options={optionsForsettlementType} onChange={this.onChange} />
						</div>
						<div className="account-create-purchase-method">
							<Reactman.FormInput label={splitRatioName} name="splitRatio" value={this.state.splitRatio} onChange={this.onChange} />
							<span className="moneyNote">%</span>
						</div>
						<div className="account-create-purchase-method">
							<Reactman.FormInput label="风险金额:" name="riskMoney" value={this.state.riskMoney} onChange={this.onChange} />
							<span className="moneyNote">元</span>
						</div>
						<Reactman.FormText label="备注说明:" name="remark" value={this.state.remark} onChange={this.onChange} width={300} height={150}/>
						<Reactman.FormCheckbox label="" name="isSync" value={this.state.isSync} options={optionsForSync} onChange={this.onChange} />
					</fieldset>
				</form>
				<legend className="pl10 pt10 pb10">收款账户</legend>
				<form className="form-horizontal mt15">
					<fieldset>
						<Reactman.FormSelect label="公司名称:" name="corpAccount" value={this.state.corpAccount} options={optionsForcompany} onChange={this.onChange} />
						<Reactman.FormSelect label="开户行:" name="corpAccount" value={this.state.corpAccount} options={optionsForaccount} onChange={this.onChange} />
						<Reactman.FormSelect label="账户:" name="corpAccount" value={this.state.corpAccount} options={optionsForbank} onChange={this.onChange} />
					</fieldset>		
				</form>
			</div>
		)
	}
})
module.exports = AddSelfShopDialog;
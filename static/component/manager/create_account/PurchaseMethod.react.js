/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.create_account:AccountCreatePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var AddGroupPointDialog = require('./AddGroupPointDialog.react');
var GroupPointsDialog = require('./GroupPointsDialog.react');
require('./style.css');

var PurchaseMethod = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},
	
	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChangeValue: function(index, value, event){
		var property = event.target.getAttribute('name');
		Action.updateRebates(index, property, value);
	},

	addGrounpPoints: function(){
		Reactman.PageAction.showDialog({
			title: "添加自营平台",
			component: AddGroupPointDialog,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	addRebateDialog: function(){
		var rebates = this.state.rebates;
		console.log(rebates.length)
		if(rebates.length > 2){
			Reactman.PageAction.showHint('error', '最多添加三个条件!');
			return;
		}
		Action.addRebateDialog();
	},

	deleteRebateValue: function(index){
		Action.deleteRebateValue(index);
	},

	render: function() {
		var type = this.props.Type;
		if (type == '2'){
			// 注释代码 请勿删除
			// return(
			// 	<div>
			// 		<div className="account-create-purchase-method">
			// 			<Reactman.FormInput label="零售扣点:" type="text" name="points" validate="require-notempty" value={this.props.points} onChange={this.props.onChange} />
			// 			<span className="money_note">%</span>
			// 			<span className="add-grounp-points">
			// 				<a href="javascript:void(0);" onClick={this.addGrounpPoints}>增加团购扣点</a>
			// 			</span>
			// 		</div>
			// 		<div><GroupPointsDialog /></div>
			// 	</div>
			// )
			return(
				<div className="account-create-purchase-method">
					<Reactman.FormInput label="零售扣点:" type="text" name="points" validate="require-notempty" value={this.props.points} onChange={this.props.onChange} />
					<span className="money_note">%</span>
				</div>
			)
		}if(type == '3'){
			var rebates = this.state.rebates;
			var _this = this;
			var rebateDialog = '';
			if(rebates.length > 0){
				rebateDialog = rebates.map(function(rebate, index){
					return(
						<div className="rebates-dialog" key={index}>
							<span>周期</span>
							<Reactman.FormDateTimeInput label="" name="validateFromCondition" value={rebate.validateFromCondition} readOnly onChange={_this.onChangeValue.bind(_this,index)} />
							<span style={{marginLeft:'70px'}}>至</span>
							<Reactman.FormDateTimeInput label="" name="validateToCondition" value={rebate.validateToCondition} readOnly onChange={_this.onChangeValue.bind(_this,index)} />
							<span style={{display:'inline-block',marginLeft:'70px'}}>或金额不大于</span>
							<Reactman.FormInput label="" type="text" name="orderMoneyCondition" value={rebate.orderMoneyCondition} onChange={_this.onChangeValue.bind(_this,index)} />
							<span>元前提下，返点比例为</span>
							<Reactman.FormInput label="" type="text" name="rebateProportCondition" value={rebate.rebateProportCondition} onChange={_this.onChangeValue.bind(_this,index)} />
							<span>%，否则，将按</span>
							<Reactman.FormInput label="" type="text" name="defaultRebateProportCondition" value={rebate.defaultRebateProportCondition} onChange={_this.onChangeValue.bind(_this,index)} />
							<span>%基础扣点结算。</span>
							<a className="rebate-close" href="javascript:void(0);" onClick={_this.deleteRebateValue.bind(_this,index)} title="删除">x</a>
						</div>
					)
				})
			}
			return(
				<div>
					<div className="profilts-dialog" style={{display:'inline-block'}}>
						<span style={{display:'inline-block'}}>首月(商品上架后30天含内)或金额不大于</span>
						<Reactman.FormInput label="" type="text" name="orderMoney" validate="require-positive-int" value={this.state.orderMoney} onChange={this.props.onChange} />
						<span>元前提下，返点比例为</span>
						<Reactman.FormInput label="" type="text" name="rebateProport" validate="require-percent" value={this.state.rebateProport} onChange={this.props.onChange} />
						<span>%，否则，将按</span>
						<Reactman.FormInput label="" type="text" name="defaultRebateProport" validate="require-percent" value={this.state.defaultRebateProport} onChange={this.props.onChange} />
						<span>%基础扣点结算。</span>
					</div>
					{rebateDialog}
				</div>
			)
			// return(
			// 	<div>
			// 		<div className="profilts-dialog" style={{display:'inline-block'}}>
			// 			<span style={{display:'inline-block'}}>首月(商品上架后30天含内)或金额不大于</span>
			// 			<Reactman.FormInput label="" type="text" name="orderMoney" value={this.state.orderMoney} onChange={this.props.onChange} />
			// 			<span>元前提下，返点比例为</span>
			// 			<Reactman.FormInput label="" type="text" name="rebateProport" value={this.state.rebateProport} onChange={this.props.onChange} />
			// 			<span>%，否则，将按</span>
			// 			<Reactman.FormInput label="" type="text" name="defaultRebateProport" value={this.state.defaultRebateProport} onChange={this.props.onChange} />
			// 			<span>%基础扣点结算。</span>
			// 		</div>
			// 		<button type="button" className="btn btn-primary" style={{marginLeft:'10px'}} onClick={this.addRebateDialog}>+添加</button>
			// 		{rebate_dialog}
			// 	</div>
			// )
			return(
				<div></div>
			)
		}else {
			return(
				<div></div>
			)
		}
	}
});

module.exports = PurchaseMethod;
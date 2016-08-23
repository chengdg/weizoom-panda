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
		console.log(index,value, property);
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
		if(rebates.length>2){
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
			// 注释代码 请勿删除
			var rebates = this.state.rebates;
			var _this = this;
			var rebate_dialog = '';
			if(rebates.length>0){
				rebate_dialog = rebates.map(function(rebate, index){
					return(
						<div className="rebates-dialog" key={index}>
							<span>周期</span>
							<Reactman.FormDateTimeInput label="" name="validate_from_condition" value={rebate.validate_from_condition} readOnly onChange={_this.onChangeValue.bind(_this,index)} />
							<span style={{marginLeft:'70px'}}>至</span>
							<Reactman.FormDateTimeInput label="" name="validate_to_condition" value={rebate.validate_to_condition} readOnly onChange={_this.onChangeValue.bind(_this,index)} />
							<span style={{display:'inline-block',marginLeft:'70px'}}>或金额不大于</span>
							<Reactman.FormInput label="" type="text" name="order_money_condition" value={rebate.order_money_condition} onChange={_this.onChangeValue.bind(_this,index)} />
							<span>元前提下，返点比例为</span>
							<Reactman.FormInput label="" type="text" name="rebate_proport_condition" value={rebate.rebate_proport_condition} onChange={_this.onChangeValue.bind(_this,index)} />
							<span>%，否则，将按</span>
							<Reactman.FormInput label="" type="text" name="default_rebate_proport_condition" value={rebate.default_rebate_proport_condition} onChange={_this.onChangeValue.bind(_this,index)} />
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
						<Reactman.FormInput label="" type="text" name="order_money" validate="require-positive-int" value={this.state.order_money} onChange={this.props.onChange} />
						<span>元前提下，返点比例为</span>
						<Reactman.FormInput label="" type="text" name="rebate_proport" validate="require-percent" value={this.state.rebate_proport} onChange={this.props.onChange} />
						<span>%，否则，将按</span>
						<Reactman.FormInput label="" type="text" name="default_rebate_proport" validate="require-percent" value={this.state.default_rebate_proport} onChange={this.props.onChange} />
						<span>%基础扣点结算。</span>
					</div>
					{rebate_dialog}
				</div>
			)
			// return(
			// 	<div>
			// 		<div className="profilts-dialog" style={{display:'inline-block'}}>
			// 			<span style={{display:'inline-block'}}>首月(商品上架后30天含内)或金额不大于</span>
			// 			<Reactman.FormInput label="" type="text" name="order_money" value={this.state.order_money} onChange={this.props.onChange} />
			// 			<span>元前提下，返点比例为</span>
			// 			<Reactman.FormInput label="" type="text" name="rebate_proport" value={this.state.rebate_proport} onChange={this.props.onChange} />
			// 			<span>%，否则，将按</span>
			// 			<Reactman.FormInput label="" type="text" name="default_rebate_proport" value={this.state.default_rebate_proport} onChange={this.props.onChange} />
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
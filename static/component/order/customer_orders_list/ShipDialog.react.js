/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_orders_list:ShipDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var ShipDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var order_id = this.props.data.order_id;
		return {
			order_id: order_id
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onChangeStore: function(){
		var infomations = Store.getData();
		this.setState({
			ship_company: infomations['ship_company'],
			ship_number: infomations['ship_number'],
			shiper_name: infomations['shiper_name']
		})
	},

	onBeforeCloseDialog: function() {
		if (this.state.ship_company === '-1') {
			Reactman.PageAction.showHint('error', '请选择物流公司');
		} else {
			console.log('this.state');
			console.log(this.state);
			//给接口传递发货的参数
			Reactman.Resource.put({
				resource: 'order.order_ship_informations',
				data: {
					order_id: this.state.order_id,
					express_company_name: this.state.ship_company,
					express_number: this.state.ship_number,
					leader_name: this.state.shiper_name
				},
				success: function() {
					this.closeDialog();
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}
	},

	render:function(){
		var options = [{
			text: '请选择物流公司',
			value: '-1'
		}, {
			text: '申通快递',
			value: 'shentong'
		},{
			text: 'EMS',
			value: 'ems'
		},{
			text: '顺丰速运',
			value: 'shunfeng'
		},{
			text: '圆通速递',
			value: 'yuantong'
		},{
			text: '中通速递',
			value: 'zhongtong'
		},{
			text: '天天快递',
			value: 'tiantian'
		},{
			text: '韵达快运',
			value: 'yunda'
		},{
			text: '百世快递',
			value: 'huitongkuaidi'
		},{
			text: '全峰快递',
			value: 'quanfengkuaidi'
		},{
			text: '德邦物流',
			value: 'debangwuliu'
		},{
			text: '宅急送',
			value: 'zhaijisong'
		},{
			text: '快捷速递',
			value: 'kuaijiesudi'
		},{
			text: '比利时邮政',
			value: 'bpost'
		},{
			text: '速尔快递',
			value: 'suer'
		},{
			text: '国通快递',
			value: 'guotongkuaidi'
		},{
			text: '如风达',
			value: 'rufengda'
		},{
			text: '邮政包裹/平邮',
			value: 'youzhengguonei'
		}];
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15">
				<fieldset>
					<Reactman.FormSelect label="物流公司:" name="ship_company" validate="require-notempty" value={this.state.ship_company} options={options} onChange={this.onChange}/>
					<Reactman.FormInput label="快递单号:"name="ship_number" validate="require-string" value={this.state.ship_number} onChange={this.onChange} />
					<Reactman.FormInput label="发货人:"name="shiper_name" placeholder="备注请用竖线隔开" value={this.state.shiper_name} onChange={this.onChange} />
				</fieldset>
			</form>
		</div>
		)
	}
})
module.exports = ShipDialog;
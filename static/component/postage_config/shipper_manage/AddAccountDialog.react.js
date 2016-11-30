/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.shipper_manage:AddCatalogDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var DialogStore = require('./DialogStore');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogDialog = Reactman.createDialog({
	getInitialState: function() {
		DialogStore.addListener(this.onChangeStore);
		return DialogStore.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateData(property, value);
	},

	onChangeStore: function(){
		this.setState(DialogStore.getData());
	},

	onBeforeCloseDialog: function() {
		var expressId = this.state.expressId;
		var expressName = this.state.expressName;
		var customerName = this.state.customerName;
		var customerPwd = this.state.customerPwd;
		var monthcode = this.state.logisticsNumber;

		if(expressName == -1){
			Reactman.PageAction.showHint('error', '请选择物流公司 !');
			return;
		}

		if(expressName == 'zhongtong' || expressName == 'huitongkuaidi' || expressName=='yunda' 
			|| expressName=='shentong'|| expressName=='youshuwuliu'||expressName=='zhaijisong') {
			if(customerName == '' || customerPwd == ''){
				Reactman.PageAction.showHint('error', '请填写CustomerName、CustomerPwd !');
				return;
			}
		}

		if(expressName == 'yuantong' ) {
			if(customerName == '' || monthcode == ''){
				Reactman.PageAction.showHint('error', '请填写CustomerName、Monthcode !');
				return;
			}
		}

		if(expressName == 'debangwuliu' ) {
			if(customerName == ''){
				Reactman.PageAction.showHint('error', '请填写CustomerName !');
				return;
			}
		}

		if(expressId!=-1){
			Reactman.Resource.post({
				resource: 'postage_config.express_bill',
				data: {
					express_id: expressId,
					express_name: expressName,
					customer_name: customerName,
					customer_pwd: customerPwd,
					logistics_number: monthcode,
					remark: this.state.remark,
					sendsite: this.state.sendsite
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '修改成功!');
					},500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}else{
			Reactman.Resource.put({
				resource: 'postage_config.express_bill',
				data: {
					express_name: this.state.expressName,
					customer_name: this.state.customerName,
					customer_pwd: this.state.customerPwd,
					logistics_number: this.state.logisticsNumber,
					remark: this.state.remark,
					sendsite: this.state.sendsite
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '添加成功!');
					},500);
					Action.clearData();
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
		},{
			text: '圆通速递',
			value: 'yuantong'
		},{
			text: '中通速递',
			value: 'zhongtong'
		},{
			text: '申通快递',
			value: 'shentong'
		},{
			text: '韵达快运',
			value: 'yunda'
		},{
			text: '百世快递',
			value: 'huitongkuaidi'
		},{
			text: '顺丰速运',
			value: 'shunfeng'
		},{
			text: '德邦物流',
			value: 'debangwuliu'
		},{
			text: '宅急送',
			value: 'zhaijisong'
		},{
			text: '优速物流',
			value: 'youshuwuliu'
		},{
			text: '广东邮政',
			value: 'guangdongyouzheng'
		},{
			text: 'EMS',
			value: 'ems'
		},{
			text: 'ANE',
			value: 'anenngwuliu'
		},{
			text: '远成快运',
			value: 'yuanchengkuaiyun'
		}];
		return (
			<div className="xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset className="xui-express-account">
						<Reactman.FormSelect label="快递公司:" name="expressName" validate="require-notempty" value={this.state.expressName} options={options} onChange={this.onChange}/>
						<Reactman.FormInput type="text" label="CustomerName" name="customerName" placeholder="商户代码/编号/ID，此信息由快递网点开通" value={this.state.customerName} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="CustomerPwd" name="customerPwd" placeholder="客户密码/密钥，此信息由快递网点开通" value={this.state.customerPwd} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="monthcode" name="logisticsNumber" placeholder="密钥串/月结号，此信息由圆通/顺丰网点开通" value={this.state.logisticsNumber} onChange={this.onChange} />
						<Reactman.FormInput type="text" label="sendsite" name="sendsite" placeholder="网点名称" value={this.state.sendsite} onChange={this.onChange} />
						<Reactman.FormText type="text" label="备注:" name="remark" value={this.state.remark} onChange={this.onChange} inDialog={true} width={300} height={200}/>
					</fieldset>
				</form>
			</div>
		)
	}
})
module.exports = AddCatalogDialog;
/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var RevokeSyncSelfShopDialog = require('./RevokeSyncSelfShopDialog.react');
require('./style.css');

var ChooseSyncSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		Action.getAllSyncedSelfShops();
		return {
			select_self_shop: Store.getData()['selectSelfShop'],
			self_shop: []
		}
	},

	onChangeStore: function(){
		this.setState({
			select_self_shop: Store.getData()['selectSelfShop'],
			self_shop: Store.getData()['selfShop']
		});
	},

	ChooseSelfShop: function(value){
		Action.chooseSelfShop(value);
	},

	cancleChecked: function(){
		this.closeDialog();
	},

	chooseAllSelfShop: function(){
		Action.chooseAllSelfShop();
	},

	productRelation: function(product_ids) {
		var selectSelfShop = this.state.select_self_shop;
		var _this = this;
		if(selectSelfShop.length==0){
			Action.cancleChooseReason();
			_.delay(function(){
				Reactman.PageAction.showDialog({
					title: "全部停售",
					component: RevokeSyncSelfShopDialog,
					data: {
						product_id: String(product_ids),
						sync_type: 'single'
					},
					success: function(inputData, dialogState) {
						console.log("success");
					}
				});
			},100)
		}else{
			var productData = [{
				'weizoom_self': selectSelfShop.join(','),//选择的商城
				'product_ids': product_ids//商品id
			}]
			Action.relationFromWeapp(JSON.stringify(productData));
			_.delay(function(){
				_this.closeDialog();
			},500)
		}
	},

	render: function(){
		var _this = this;
		var productId = this.props.data.product_id;
		var syncType = this.props.data.sync_type;
		var selfShop = this.state.self_shop;
		var selectSelfShop = this.state.select_self_shop;
		var checked = this.state.select_self_shop.length==selfShop.length?'checked':null;

		var selfs = selfShop.map(function(self_shop,index){
			var value = self_shop.value;
			var bgStyle = {};
			bgStyle['style'] = {};

			var isTrue = false;
			for (var i = 0; i < selectSelfShop.length; i++) {
				if (selectSelfShop[i] === value) {
					isTrue = true;
				}
			}
			
			if(isTrue){
				bgStyle['style'] = {background: '#009DD9', color:'#FFF'};
			}
			return(
				<li key={index} style={bgStyle['style']} className="self-shop-li" onClick={_this.ChooseSelfShop.bind(_this,value)} title={self_shop.text}>{self_shop.text}</li>
			)
		})

		return (
			<div className="xui-formPage">
				<ul>
					{selfs}
				</ul>
				<span style={{display:'block',paddingLeft:'40px'}}>
					<input type="checkbox" checked={checked} className="checkbox" name="select" value="0" style={{display:'inline-block'}} onChange={this.chooseAllSelfShop}/>全选
				</span>
				<span className='cancle-relation-tips' style={{display:'none'}}>( 提示：取消平台勾选，商品将从该平台禁售不可见 )</span>	
				<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'190px'}} onClick={this.productRelation.bind(this,productId)}><span>确定</span></a>
				<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'50px'}} onClick={this.cancleChecked}><span>取消</span></a>
			</div>
		)
	}
})
module.exports = ChooseSyncSelfShopDialog;
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
require('./style.css');

var ChooseSyncSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var selfShop = [{
			'name': '微众白富美',
			'value': 'weizoom_baifumei'
		},{
			'name': '微众俱乐部',
			'value': 'weizoom_club'
		},{
			'name': '微众家',
			'value': 'weizoom_jia'
		},{
			'name': '微众妈妈',
			'value': 'weizoom_mama'
		},{
			'name': '微众商城',
			'value': 'weizoom_shop'
		},{
			'name': '微众学生',
			'value': 'weizoom_xuesheng'
		},{
			'name': '微众Life',
			'value': 'weizoom_life'
		},{
			'name': '微众一家人',
			'value': 'weizoom_yjr'
		},{
			'name': '惠惠来啦',
			'value': 'weizoom_fulilaile'
		},{
			'name': '居委汇',
			'value': 'weizoom_juweihui'
		},{
			'name': '微众中海',
			'value': 'weizoom_zhonghai'
		},{
			'name': '微众club',
			'value': 'weizoom_zoomjulebu'
		},{
			'name': '微众吃货',
			'value': 'weizoom_chh'
		},{
			'name': '微众圈',
			'value': 'weizoom_pengyouquan'
		},{
			'name': '少先队',
			'value': 'weizoom_shxd'
		},{
			'name': '津美汇',
			'value': 'weizoom_jinmeihui'
		},{
			'name': '微众便利店',
			'value': 'weizoom_wzbld'
		},{
			'name': '微众佳人',
			'value': 'weizoom_jiaren'
		},{
			'name': '微众良乡商城',
			'value': 'weizoom_xiaoyuan'
		},{
			'name': '微众精英',
			'value': 'weizoom_jy'
		}];
		return {
			select_self_shop: Store.getData()['selectSelfShop'],
			self_shop: selfShop
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		this.setState({
			select_self_shop: Store.getData()['selectSelfShop']
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
		var productData = [{
			'weizoom_self': selectSelfShop.join(','),//选择的商城
			'product_ids': product_ids//商品id
		}]
		Action.relationFromWeapp(JSON.stringify(productData));
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
				<li key={index} style={bgStyle['style']} className="self-shop-li" onClick={_this.ChooseSelfShop.bind(_this,value)}>{self_shop.name}</li>
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
/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_relation:ProductRelationDialog');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var ProductRelationDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var self_shop = this.props.data.self_shop;
		var product_id = this.props.data.product_id;
		return {
			self_shop: self_shop,
			product_id: product_id,
			relations: {}
		}
	},

	onChange: function(event) {
		var property = event.target.getAttribute('name');
		var value = event.target.value;
		Action.updateProductRelation(property, value);
	},

	onChangeStore: function(){
		var relations = Store.getData();
		var hasProp = false;  
		for (var prop in relations){  
			hasProp = true;  
			break;  
		}
		if(hasProp){
			this.setState({
				relations: relations
			})
		}
	},

	productRelationSave: function(){
		var relations = Store.getData();
		var hasProp = false;  
		for (var prop in relations){  
			hasProp = true;  
			break;  
		}
		if(!hasProp){
			Reactman.PageAction.showHint('error', "请输入关联的云商通商品ID");
			return;
		}
		Action.saveProductRelation(relations,this.state.product_id)
	},

	productRelationCancle: function(){
		this.closeDialog();
	},

	render:function(){
		var _this = this;
		var self_shop = this.state.self_shop.map(function(relation,index){
			var self_user_name = relation.self_user_name;
			var relations = _this.state.relations;
			var value = relations?(relations.hasOwnProperty(self_user_name)? relations[self_user_name]: ''): '';
			return(
				<div className="form-group self-shop-div" key={index}>
					<label className="col-sm-3 control-label self-shop-name">{relation.self_first_name}</label>
                    <div className="col-sm-7" style={{left:'40px'}}>
                        <input type="text" className="form-control" name={self_user_name} value={value} onChange={_this.onChange}/>
                    </div>
				</div>
			)
		});
		return (
			<div>
				<div className="product-relation-title">
					<span style={{paddingLeft: '30px'}}>自营商城名称</span>
					<span style={{position: 'absolute', right:'85px'}}>云商通商品ID</span>
				</div>
				<div style={{clear:'both'}}></div>
				{self_shop}
				<div className="relation-btn-div">
					<button type="button" className="btn btn-primary relation-btn" onClick={this.productRelationSave}>关联</button>
					<button type="button" className="btn btn-primary" onClick={this.productRelationCancle}>取消</button>
				</div>
			</div>
		)
	}
})
module.exports = ProductRelationDialog;
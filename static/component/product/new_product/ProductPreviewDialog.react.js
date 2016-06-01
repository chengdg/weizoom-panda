/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:ProductPreviewDialog');
var React = require('react');
var ReactDOM = require('react-dom');
var Action = require('./Action');
var Reactman = require('reactman');
require('./style.css');

var ProductPreviewDialog = Reactman.createDialog({

	getInitialState: function() {
		var product = this.props.data.product;
		return {
			product_name: product.product_name,
			images: product.images,
			promotion_title: product.promotion_title,
			product_price: product.product_price,
			remark: product.remark
		}
	},

	onBeforeCloseDialog: function(){
		this.closeDialog();
	},
	
	render:function(){
		var path = this.state.images[0].path;
		var img_count = this.state.images.length;
		var remark = this.state.remark;
		return (
			<div className="xui-formPage xui-product-preview-div">
				<div className="product-detail">
					<div style={{position:'relative'}}>
						<img className='product-image' src={path}/>
						<span className='product-image-count'>1/{img_count}</span>
					</div>
					<div className="product-name-price">
						<span className="product-collect-title">收藏</span>
						<span className="product-name">{this.state.product_name}</span>
						<span className="product-promotion-title">{this.state.promotion_title}</span>
						<span className="product-price">￥{this.state.product_price}</span>
					</div>
					<div className="product-choose">
						<span className='choose-count'>请选择</span>
						<ul className='product-count'>
							<li>-</li>
							<li>1</li>
							<li>+</li>
						</ul>
					</div>
					<div className="product-introduce">
						<span className="title">商品详情</span>
						<div className="product-content" dangerouslySetInnerHTML={{__html: this.state.remark}}></div>
					</div>
				</div>
			</div>
		)
	}
})

module.exports = ProductPreviewDialog;
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
			product_price: product.product_price
		}
	},
	
	render:function(){
		var path = this.state.images[0].path;
		return (
			<div className="xui-formPage">
				<div className="product-detail">
					<div><img className='product-image' src={path}/></div>
					<div className="product-name-price">
						<span className="product-name">{this.state.product_name}</span>
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
						<span className="title">商品介绍</span>
					</div>
				</div>
			</div>
		)
	}
})

module.exports = ProductPreviewDialog;
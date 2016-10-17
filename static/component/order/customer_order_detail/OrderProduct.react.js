/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_order_detail:OrderProduct');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Store = require('./Store');
var Action = require('./Action');
require('./style.css')

var OrderProduct = React.createClass({
	render:function(){
		var ordeDatas = this.props.ordeDatas;
		var productDatas = [];
		productDatas.push(ordeDatas);
		if(productDatas.length>0){
			var productTr = productDatas.map(function(productData, index){
				var products = JSON.parse(productData['products']);
				var productNames = products.map(function(product,index){
					var product_model_name = product['custom_models'];
					var model_name = ''
					if(product_model_name && product_model_name!='standard'){
						model_name = '规格:' + product_model_name;
					}
					return (
						<span className="product-item-info" key={index} style={{paddingTop:'5px'}}>
							<img className="product-img" src={product['product_img']}></img>
							<span className='product-name'>{product["product_name"]}</span>
							<span className='product-model-name'>{model_name}</span>
							<br></br>
						</span>
					)
				})

				var unitPrice = products.map(function(product,index){
					return (
						<span key={index} className="product-item-info">{product["origin_price"]}/({product["count"]}件)<br></br></span>
					)
				})

				return(
					<tr key={index}>
						<td>
							{productNames}
						</td>
						<td>
							{unitPrice}
						</td>
						<td>
							<div style={{margin:'20px 0 0 10px'}}>{productData.total_count}</div>
						</td>
						<td>
							<div style={{margin:'20px 0 0 10px'}}>{productData.origin_total_price}</div>
						</td>
						<td>
							<div style={{margin:'20px 0 0 10px'}}>{productData.postage}</div>
						</td>
					</tr>
				)
			});
		}
		
		return (
			<div className="form-horizontal mt15 pt20 pl90">
				<table className="table table-bordered">
					<thead>
						<tr>
							<th>商品</th>
							<th>单价/数量</th>
							<th>商品件数</th>
							<th>订单金额(元)</th>
							<th>运费(元)</th>
						</tr>
					</thead>
					<tbody>
						{productTr}
					</tbody>
				</table>
			</div>
		)
	}
})
module.exports = OrderProduct;
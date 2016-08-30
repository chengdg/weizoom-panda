/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:order.customer_order_detail:OrderDataPage');
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Store = require('./Store');
var Action = require('./Action');
var OrderLogistics = require('./OrderLogistics.react');
require('./style.css')

var OrderDataPage = React.createClass({
	getInitialState: function() {	
		return {
			orde_datas: ''
		}
	},

	onChangeStore: function(event) {
		var orde_datas = Store.getData();
		this.setState({
			orde_datas: orde_datas
		})
	},

	componentDidMount: function(){
		Action.saveProduct(W.order_id);
		Store.addListener(this.onChangeStore);
	},

	getOrderProductsInfo: function(value,data){
		var _this = this;
		var products = JSON.parse(data['products']);
		var product_items = products.map(function(product,index){
			if (value == 'product_name'){
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
			}else if (value == 'unit_price/quantity'){
				return (
					<span key={index} className="product-item-info">{product["purchase_price"]}/({product["count"]}件)<br></br></span>
				)
			}
		})
		return product_items;
	},

	rowFormatter: function(field, value, data) {
		if(field === 'product_name'){
			var product = this.getOrderProductsInfo('product_name',data);
			return (
				<div>{product}</div>
			);
			
		}else if(field === 'unit_price/quantity'){
			var product = this.getOrderProductsInfo('unit_price/quantity',data);
			return (
				<div>{product}</div>
			);
		}else if(field === 'total_count'){
			return (
				<div style={{margin:'20px 0 0 10px'}}>{value}(件)</div>
			);
		}else if(field === 'order_money'){
			return (
				<div style={{margin:'20px 0 0 10px'}}>{value}(元)</div>
			);
		}else if(field === 'postage'){
			return (
				<div style={{margin:'20px 0 0 10px'}}>{value}(元)</div>
			);
		}else{
			return value;
		}
	},

	render:function(){
		var order_id = W.order_id;
		var productsResource = {
			resource: 'order.customer_order_detail',
			data: {
				page: 1,
				order_id: order_id
			}
		};
		var orde_datas = this.state.orde_datas;
		if (orde_datas){
			return (
				<div>
					<OrderStatus ordeDatas={orde_datas}/>
					<OrderLogistics ordeDatas={orde_datas}/>
					<div className="mt15 xui-product-productListPage">
						<Reactman.TablePanel>
							<Reactman.TableActionBar>
							</Reactman.TableActionBar>
							<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
								<Reactman.TableColumn name="商品" field="product_name" />
								<Reactman.TableColumn name="单价/数量" field="unit_price/quantity" />
								<Reactman.TableColumn name="商品件数" field="total_count" width='200px'/>
								<Reactman.TableColumn name="订单金额" field="order_money" width='200px'/>
								<Reactman.TableColumn name="运费" field="postage" width='200px'/>
							</Reactman.Table>
						</Reactman.TablePanel>
					</div>
				</div>
			)
		}else{
			return (
				<div>
					<div className="mt15 xui-product-productListPage">
						<Reactman.TablePanel>
							<Reactman.TableActionBar>
							</Reactman.TableActionBar>
							<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
								<Reactman.TableColumn name="商品" field="product_name" />
								<Reactman.TableColumn name="单价/数量" field="unit_price/quantity" />
								<Reactman.TableColumn name="商品件数" field="total_count" width='200px'/>
								<Reactman.TableColumn name="订单金额" field="order_money" width='200px'/>
								<Reactman.TableColumn name="运费" field="postage" width='200px'/>
							</Reactman.Table>
						</Reactman.TablePanel>
					</div>
				</div>
			)
		}	
	}
})

var OrderStatus = React.createClass({
	render:function(){
		var orde_datas = this.props.ordeDatas;
		var order_id = orde_datas['order_id']? orde_datas['order_id']: '';
		var order_status = orde_datas['order_status'];
		return (
			<div style={{background:'#FFF',marginTop:'10px', border:'1px solid #CCC',fontSize:'16px',height:'100px'}}>
				<div style={{padding:'5px 20px'}}>
					<div>
						<span>订单编号:{order_id}</span>
					</div>
					<div style={{marginTop:'10px'}}>
						<span>订单状态:{order_status}</span>
					</div>
					
				</div>
			</div>
		)
	}
})
module.exports = OrderDataPage;
/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css')

var CustomerPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	showProduct:function(class_name){
		var display = document.getElementsByClassName(class_name)[0].style.display;
		if (display == 'none'){
			document.getElementsByClassName(class_name)[0].style.display = "block";
		}else{
			document.getElementsByClassName(class_name)[0].style.display = "none";
		}

	},

	rowFormatter: function(field, value, data) {
		if (field === 'expand-row') {
			var product_infos = data['fans_id'];
			if(product_infos==0){
				var products = product_infos.map(function(product,index){
				return(
						<div style={{backgroundColor: '#EFEFEF',height: '22px'}} key={index}>
							<div className="xui-expand-row-info" style={{float: 'left',paddingLeft:'15px'}}>{product.name} </div>
							<div className="xui-expand-row-info" style={{float: 'right',paddingRight:'200px'}}>上架时间:{product.time}</div>
							<div className="xui-expand-row-info" style={{float: 'right',paddingRight:'100px'}}>销量:{product.sales} </div>
						</div>
					)
				});
				return (
					<div className={class_name} style={{display:'none'}}>{products}</div>
				)
			}else{
				return (
					<div style={{backgroundColor: '#EFEFEF',height: '22px',display:'none'}}>
						<div style={{float: 'left',paddingLeft:'15px'}}></div>
					</div>
				)
			}
		}else if(field === 'fans'){
			return (
				<div>
					<span><img style={{width:'40px','height':'40px',borderRadius:'20px'}} src={data['fans_pic']}/></span>
					<span style={{marginLeft:'10px'}}>ID:{data['fans_id']}</span>
				</div>
			)
		}else if(field === 'purchase_index'){
			var percentage = data['purchase_index']+'%';
			return (
				<div className="xa-scales-div" title={percentage}>
					<div className="xa-scale-div" style={{width:data['purchase_index']}}>

					</div>
				</div>
			)
		}else if(field === 'diffusion_index'){
			var percentage = data['diffusion_index']+'%';
			return (
				<div className="xa-scales-div" title={percentage}>
					<div className="xa-scale-div" style={{width:data['diffusion_index']}}>

					</div>
				</div>
			)
		}else if(field === 'status'){
			var order_id = data['order_id'];
			var src = '';
			if(order_id != ''){
				src = '/order/customer_order_detail/?id='+order_id;
			}
			if(src != ''){
				return (
					<div>
						<a href={src} target="_blank">{value}</a>
					</div>
				)
			}else{
				return (
					<div>
						{value}
					</div>
				)
			}
			
		}else{
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	render:function(){
		var productsResource = {
			resource: 'fans.fans',
			data: {
				page: 1
			}
		};
		var optionsForStatus = [{
			text: '全部', value: '-1'
		},{
			text: '已妥投，未阅读', value: '0'
		},{
			text: '已阅读，未分享', value: '1'
		},{
			text: '已阅读，已分享', value: '2'
		},{
			text: '已下单', value: '3'
		},{
			text: '已下单，已推荐', value: '4'
		}];
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormSelect label="状态:" name="status" options={optionsForStatus} match="=" />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="投放日期" field="recommend_time" />
						<Reactman.TableColumn name="粉丝" field="fans" />
						<Reactman.TableColumn name="性别" field="sex" />
						<Reactman.TableColumn name="购买指数" field="purchase_index" width='150'/>
						<Reactman.TableColumn name="推荐传播指数" field="diffusion_index" width='150'/>
						<Reactman.TableColumn name="状态" field="status" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = CustomerPage;
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

var CustomerPage = React.createClass({
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
		}else{
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'fans.fans',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="状态:" name="weapp_name_query" match="=" />
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
						<Reactman.TableColumn name="购买指数" field="purchase_index" />
						<Reactman.TableColumn name="推荐传播指数" field="diffusion_index" />
						<Reactman.TableColumn name="状态" field="status" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = CustomerPage;
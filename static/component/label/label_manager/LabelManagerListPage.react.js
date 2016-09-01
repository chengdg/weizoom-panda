/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:label.label_manager:LabelManagerListPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
var AddLabelValueDialog = require('./AddLabelValueDialog.react');
require('./style.css');
var W = Reactman.W;

var LabelManagerListPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	deleteLabelProperty: function(labelId, event) {
		var title = '确定删除么?';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				Action.deleteLabelProperty(labelId);
			}, this)
		});
	},

	addLabelValue: function(labelId){
		Reactman.PageAction.showDialog({
			title: "添加标签",
			component: AddLabelValueDialog,
			data: {
				'labelId':labelId
			},
			success: function(inputData, dialogState) {
				Action.updateLabelValue();
			}
		});
	},

	addLabelProperty: function(){
		Action.addLabelProperty();
	},

	editProductModelName: function(id,ref){
		var name = this.refs.table.refs[ref].value;
		if(name.trim().length==0){
			Reactman.PageAction.showHint('error', '请输入分类名');
			return;
		}
		Action.updateLabelProperty(id,name);
	},

	deleteLabelValue: function(labelValueId){
		Action.deleteLabelValue(labelValueId);
	},

	onMouseOver: function(className){
		var divClose = this.refs.table.refs[className];
		ReactDOM.findDOMNode(divClose).style.display = "block";
	},

	onMouseOut: function(className){
		var divClose = this.refs.table.refs[className];
		ReactDOM.findDOMNode(divClose).style.display = "none";
	},

	rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" onClick={this.deleteLabelProperty.bind(this,data['id'])}>删除</a>
				</div>
			);
		} else if(field === 'labelValues') {
			var _this = this;
			var labelValues = data['labelValues'];
			var labelValueLi = '';

			if(labelValues.length> 0) {
				labelValueLi = JSON.parse(labelValues).map(function(value,index){
					var ref = 'value_' + value['label_value_id'];
					return(
						<li className="model-li" key={index}>
	                        <div className='xa-editLabelValues' onMouseOver={_this.onMouseOver.bind(null,ref)} onMouseOut={_this.onMouseOut.bind(null,ref)}>  
	                            <span title={value['name']}>{value["name"]}</span>  
	                        </div>
	                        <button className="xui-close xa-delete" ref={ref} type="button" style={{display: 'none'}} onMouseOver={_this.onMouseOver.bind(null,ref)} onMouseOut={_this.onMouseOut.bind(null,ref)}>
	                            <span onClick={_this.deleteLabelValue.bind(_this,value['label_value_id'])}>×</span>
	                        </button>
	                    </li>
					)
				})
			}

			return(
				<div>
					<ul className="xui-propertyValueList">
						{labelValueLi}
						<li className="model-li">
							<div className='xa-editLabelValues'>  
	                            <a href="javascript:void(0);" onClick={this.addLabelValue.bind(this,data['id'])}><img src="/static/img/panda_img/addProduct.png" style={{width:'32px',height:'32px'}}/></a>  
	                        </div>
						</li>
					</ul>
				</div>
			)

		}else if(field === 'labelName'){
			var labelName = data['labelName'];
			var ref = 'labelName_' + data['id'];
			if(labelName){
				return(
					<div>
						{labelName}
					</div>
				)
			}else{
				return(
					<div style={{lineHeight:'30px'}}>
						<input type="text" ref={ref} className="product-model-name" name="model_name" onBlur={this.editProductModelName.bind(null,data['id'],ref)} style={{border:'1px solid #18a689'}} placeholder="请输入分类名"/>
					</div>
				)
			}
		}else{
			return value;
		}
	},

	render:function(){
		var productsResource = {
			resource: 'label.label_manager',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-label-labelManagerListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加分类" icon="plus" onClick={this.addLabelProperty}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="分类" field="labelName" width="200px"/>
						<Reactman.TableColumn name="标签" field="labelValues" />
						<Reactman.TableColumn name="操作" field="action" width="100px"/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = LabelManagerListPage;
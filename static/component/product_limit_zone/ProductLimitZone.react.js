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
//var AddCatalogDialog = require('./AddCatalogDialog.react');
//var AddCatalogQualificationDialog = require('./AddCatalogQualificationDialog.react');
var AddLimitZoneTemplateDialog = require('./AddLimitZoneTemplateDialog.react');
//var AddLabelDialog = require('./AddLabelDialog.react');
var LimitZoneText = require('./LimitZoneText.react');
require('./style.css')

var ProductCatalogPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({
		});
	},

	onChangeStore: function(event) {
		var filterOptions = Store.getData();
		this.refs.table.refresh();
	},



	onAddTemplate: function(event){
	    var template_id = event.target.getAttribute('data-id');
	    var name = event.target.getAttribute('data-name');
		Reactman.PageAction.showDialog({
			title: "禁售/仅售模板",
			component: AddLimitZoneTemplateDialog,
			data: {
                id: template_id,
                name: name
			},
			success: function() {
			}
		});
	},

	onClickDelete: function(event) {
		var template_id = parseInt(event.target.getAttribute('data-id'));
		Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除吗?',
			confirm: _.bind(function() {
				Action.deleteLimitZone(template_id);
			}, this)
		});
	},

	onSelectArea:function(selectedIds,selectedDatas, event){
//	    console.log('+++++++++++++++++++++++++++++++')
//        console.log(event.props['data-name'])
        Action.updateLimitZoneTemplateInfo(selectedDatas, selectedIds, event);

	},
	
	rowFormatter: function(field, value, data) {

        if(field == 'action'){
            return (
                <div className="orders-list-btn-group">
					<a className="btn btn-primary" onClick={this.onAddTemplate}
					    data-id={data.id}
					    data-name={data.name} >修改</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-id={data.id}>删除</a>
				</div>
            )
        }
        if(field == 'zone_info'){

//            console.log(data)
//            console.log('+++++++++++++++++++++++++++++++')
            return (
                <div>
                    <div>

                        <LimitZoneText info={data.limit_zone_info_text}/>
                    </div>
                    <div>
                        <Reactman.ProvinceCitySelect
                            data-id={data.id}
					        data-name={data.name}
					        initSelectedIds={data.zone_list}
					        onSelect={this.onSelectArea}
					        resource="product.provinces_cities">
                            选择区域
                        </Reactman.ProvinceCitySelect>
                    </div>
                </div>
            )
        }
		return value;
	},
	render:function(){
		var catalogsResource = {
			resource: 'limit_zone.template_list',
			data: {}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加模板" icon="plus" onClick={this.onAddTemplate}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={catalogsResource} pagination={true} formatter={this.rowFormatter} expandRow={true} ref="table">
						<Reactman.TableColumn name="模板名称" field="name" width='250px'/>
						<Reactman.TableColumn name="地区" field="zone_info" />
						<Reactman.TableColumn name="操作" field="action" width='150px'/>
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductCatalogPage;
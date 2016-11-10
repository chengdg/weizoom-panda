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
var AddLimitZoneTemplateDialog = require('./AddLimitZoneTemplateDialog.react');
var LimitZoneText = require('./LimitZoneText.react');
var QQOnlineService = require('.././qq_online/online/QQOnlineService.react');

var ProductCatalogPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({
		});
	},

	onChangeStore: function(event) {
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
    onUpdateTemplate: function(event){
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

	onSelectArea:function(selectedIds,selectedDatas, event) {
//	    if(){
//
//	    }
//        console.log('===============================')
       console.log(selectedIds, selectedDatas)
        if(selectedIds.length == 0){
            Reactman.PageAction.showHint('error', '您需要选择地区！');
            return;
        }
        Action.updateLimitZoneTemplateInfo(selectedDatas, selectedIds, event);
//        console.log('=============================')
	},
	
	rowFormatter: function(field, value, data) {
        if(field == 'action'){
            return (
                <div className="orders-list-btn-group">
					<a className="btn btn-primary" onClick={this.onUpdateTemplate}
					    data-id={data.id}
					    data-name={data.name} >修改</a>
					<a className="btn btn-danger ml10" onClick={this.onClickDelete} data-id={data.id}>删除</a>
				</div>
            )
        }else if(field == 'zone_info') {
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
        }else {
			return value;
		}
	},

	render:function() {
		var catalogsResource = {
			resource: 'limit_zone.template_list',
			data: {}
		};

		var serviceTel = W.serviceTel;
		var serviceQQFirst = W.serviceQQFirst;
		var serviceQQSecond = W.serviceQQSecond;
		return (
			<div className="mt15 xui-product-productListPage">
				<div> <QQOnlineService serviceQQFirst={serviceQQFirst} serviceQQSecond={serviceQQSecond} serviceTel={serviceTel}/></div>
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
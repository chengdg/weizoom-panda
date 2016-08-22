/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var W = Reactman.W;

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var StationMessageList = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {

		};
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},
	onAddMessage: function(){
	    W.gotoPage('/message/message');
	},
    rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" target="_blank" href={'/message/message/?id='+data.id}>修改</a>
					<a className="btn btn-link btn-xs">删除</a>
				</div>
			);
		}else {
			return value;
		}
	},
	render:function(){
        var messagesResource = {
			resource: 'message.message_list',
			data: {
				page: 1
			}
		};
		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="标题:" name="title" match="=" />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar>
						<Reactman.TableActionButton text="添加站内信" icon="plus" onClick={this.onAddMessage}/>
					</Reactman.TableActionBar>
					<Reactman.Table resource={messagesResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="标题" field="title" />
						<Reactman.TableColumn name="创建时间" field="created_at" />
						<Reactman.TableColumn name="操作" field="action" />

					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = StationMessageList;
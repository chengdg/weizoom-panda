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

var StationMessageList = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData()
	},

	onChangeStore: function(){
		this.setState(Store.getData());
		this.refs.table.refresh(); 
	},

	onAddMessage: function(){
	    W.gotoPage('/message/message');
	},

	onClickDelete: function(event){
        var message_id = parseInt(event.target.getAttribute('data-id'));

        Reactman.PageAction.showConfirm({
			target: event.target,
			title: '确认删除该消息吗?',
			confirm: _.bind(function() {
				Action.deleteMessage(message_id);
			}, this)
		});
	},

    rowFormatter: function(field, value, data) {
		if (field === 'action') {
			return (
				<div>
					<a className="btn btn-link btn-xs" target="_blank" href={'/message/message/?id='+data.id}>修改</a>
					<a className="btn btn-link btn-xs" data-id={data.id} onClick={this.onClickDelete}>删除</a>
				</div>
			);
		}else {
			return value;
		}
	},

	render:function(){
//		console.log("=====");
        var messagesResource = {
			resource: 'message.message_list',
			data: {
				page: 1
			}
		};

		return (
			<div className="mt15 xui-stationMessage-StationMessageList">
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
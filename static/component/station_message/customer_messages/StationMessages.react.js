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

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

    rowFormatter: function(field, value, data) {
        if (data.status==0){
            var status = '(未读)';
        }else{
            var status = '';
        }
        if (data.status==0){
            if (field === 'title') {
                return (
                    <div className='bold_text'>
                        <a href='' className='href_color'>{status}{value}</a>

                    </div>
                );
		    }else{
		        return (
                    <div className='bold_text'>
                        {value}

                    </div>
                );
		    }

        }else{
            return (
                <div className='grey_text'>
                    {value}

                </div>
            );
        }

	},
	render:function(){
        var messagesResource = {
			resource: 'message.customer_messages',
			data: {
				page: 1
			}
		};
		return (
			<div className="mt15 xui-product-productListPage">

				<Reactman.TablePanel>
                    <Reactman.TableActionBar>
					</Reactman.TableActionBar>
					<Reactman.Table resource={messagesResource} formatter={this.rowFormatter} pagination={true} ref="table">
						<Reactman.TableColumn name="标题" field="title" />
						<Reactman.TableColumn name="创建时间" field="created_at" />

					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = StationMessageList;
<template>
	<v-app>
		<comments-header></comments-header>
		<v-content>
			<v-container fluid grid-list-lg>
                <v-layout class="ma-2">
                    <v-flex xs12 sm12 md4 lg3 xl2>
                        <v-select
                            v-model="slide_pk"
                            :items="slides"
                            :loading="slides_load"
                            item-text="name"
                            item-value="pk"
                            label="Slides"
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-flex>
                    <v-flex xs12 sm12 md4 lg3 xl2>
                        <v-select
                            v-model="message_type"
                            :items="message_types"
                            item-text="text"
                            item-value="value"
                            label="Type"
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-flex>
                    <v-flex xs12 sm12 md4 lg3 xl2>
                        <v-select
                            v-model="question_id"
                            :items="question_ids"
                            item-text="text"
                            item-value="value"
                            label="Type"
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-flex>
                    <v-flex xs12 sm12 md4 lg3 xl2>
                        <div>
                            <div>{{filter_socket_status}}</div>
                            <div>{{comment_socket_status}}</div>
                        </div>
                    </v-flex>
                </v-layout>
                <v-layout class="custom-layout ma-3" row wrap>
                    <v-flex class="ma-1" xl6 lg6 md6 sm12 xs12 :key="comment_index" v-for="(comment, comment_index) in comments">
                        <span class="comment-span">{{comment.text}}</span>
                    </v-flex>
                </v-layout>
                <v-layout row wrap class = "ma-3">
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-progress-linear
                            :value="to_do_percentage"
                            rounded
                            color="pink"
                            height="14">
                        </v-progress-linear>
                    </v-flex>
                    <v-flex xl6 lg6 md6 sm12 xs12>
                        <h3><code>W</code> Previous Page</h3>
                        <h3><code>S</code> Next Page</h3>
                        <h3><code>A</code> Delete a Comment</h3>
                        <h3><code>D</code> Send a Comment</h3>
                    </v-flex>
                    <v-flex xl6 lg6 md6 sm12 xs12>
                        <h3>Comments to be Processed:{{to_do_comments}}</h3>
                        <h3>Comments Sent:{{comments_sent_num}}</h3>
                        <h3>Comments Deleted:{{comments_deleted_num}}</h3>
                        <h3>Total Comments:{{total_comments}}</h3>
                    </v-flex>
                </v-layout>
			</v-container>
		</v-content>
	</v-app>
</template>

<script>
import axios from 'axios'

import CommentsHeader from '../components/CommentsHeader'

  export default {
	data() {
		return {
            slides_load:true,
            slide_pk:undefined,
            message_type:0,
            message_types:[
                {text:"Comment",
                 value:0},
                {text:"Question",
                 value:1},
            ],
            question_id:0,
            question_ids:[{text:0, value:0}],
            slides:[],
            comments:[],
            filter_socket_open:false,
            comment_socket_open:false,
            comments_sent_num:0,
            comments_deleted_num:0,
            total_comments:0,
		}
	},
	components:{
		CommentsHeader,
	},
	watch: {
        slide_pk(val){
            if(val){
                this.initFilterSocket(val);
                this.initCommentSocket(val);
            }
        },
	},
	computed:{
        filter_socket_status(){
            return this.filter_socket_open ? "Filter Socket Connected" : "Filter Socket Disconnected";
        },
        comment_socket_status(){
            return this.comment_socket_open ? "Comment Socket Connected" : "Comment Socket Disconnected";
        },
        to_do_comments(){
            return this.total_comments - this.comments_sent_num - this.comments_deleted_num;
        },
        to_do_percentage(){
            if(this.total_comments > 0)
                return Math.ceil(100 * (1 - (this.to_do_comments) / this.total_comments));
            else
                return 100;
        }
	},
	methods: {
		goToHref(text){
			window.location.href = text;
        },
        keyLeft(){
            if(this.comment_socket_open && this.filter_socket_open && this.comments.length > 0){
                this.comments.splice(0,1);
                this.comments_deleted_num += 1;
            }
        },
        keyRight(){
            if(this.comment_socket_open && this.filter_socket_open && this.comments.length > 0){
                var tmp_comment = this.comments[0];
                this.commentSocket.send(JSON.stringify({
                    command:"send",
                    text:tmp_comment.text,
                    color:tmp_comment.color,
                    time:Date.now(),
                    message_type:tmp_comment.message_type,
                    question_id:this.question_id,
                    mode:tmp_comment.mode,
                    size:tmp_comment.size}));
                this.comments.splice(0,1);
                this.comments_sent_num += 1;
            }
        },
        keyUp(){
            if(this.comment_socket_open && this.filter_socket_open){
                this.commentSocket.send(JSON.stringify({
                    command:"question_page",
                    direction:"prev",}));
            }
        },
        keyDown(){
            if(this.comment_socket_open && this.filter_socket_open){
                this.commentSocket.send(JSON.stringify({
                    command:"question_page",
                    direction:"next",}));
            }
        },
        initSelect(val){
            for(let i = 1; i < val; i++){
                this.question_ids.push({
                    "text":i,
                    "value":i,
                });
            }
        },
        initFilterSocket(val){
            var ref = this;
            this.filterSocket = new ReconnectingWebSocket(this.ws_scheme + '://' + 
                window.location.host + "/ws/send_to_filter/");
            this.filterSocket.onopen = function(event){
                console.log("filter socket open");
                ref.filterSocket.send(JSON.stringify({
                    command:'join',
                    slide_pk:val,
                }));
            }
            this.filterSocket.onclose = function(e) {
                console.error('filter socket closed unexpectedly');
            };
            this.filterSocket.onmessage = function(comment) {
                var data = JSON.parse(comment.data);
                if(data.type=="join"){
                    ref.filter_socket_open = true;
                    console.log("Filter connected to " + data.slide_pk);
                }
                else if(data.type=="comment_unfiltered" && data.message_type==ref.message_type){
                    ref.comments.push(data);
                    ref.total_comments += 1;
                }
            };
        },
        initCommentSocket(val){
            var ref = this;
            this.commentSocket = new ReconnectingWebSocket(this.ws_scheme + '://' + 
                window.location.host + "/ws/send_to_comments/");
            this.commentSocket.onopen = function(event){
                console.log("comment socket open");
                ref.commentSocket.send(JSON.stringify({
                    command:'join',
                    slide_pk:val,
                }));
            }
            this.commentSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };
            this.commentSocket.onmessage = function(comment) {
                var data = JSON.parse(comment.data);
                if(data.type=="join"){
                    console.log("Comment connected to " + data.slide_pk);
                    ref.comment_socket_open = true;
                }
            };
        },
        getSlides(){
			axios.get('/comments/api/get_slides/',{params: {}}).then(response => {
                this.slides = response.data.slides;
                this.slides_load = false;
			});
		},
    },
    created(){
        var ref = this;
        document.onkeydown = function(e) {
            let key = window.event.keyCode;
            if(key == 65){
                ref.keyLeft();
            }
            else if(key == 87){
                ref.keyUp();
            }
            else if(key == 68){
                ref.keyRight();
            }
            else if(key == 83){
                ref.keyDown();
            }

        };
    },
	mounted(){
        this.initSelect(10);
        this.getSlides();
        this.ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	},
};
</script>

<style>
    .connected-span{
        width:7px;
        height: 15px;
        color:green;
    }

    .disconnected-span{
        width:7px;
        height: 15px;
        color:red;
    }

    .custom-layout{
        height: 300px;
        overflow-y: auto;
        border-radius: 7px;
        border-style: solid;
        border-width: thin;
        border-color: grey;
    }

    .comment-span{
        border-radius: 5px;
        padding: 10px;
        background-color: lavender;
    }

	@media (min-width: 1025px) {
		
	}


	@media (min-width: 768px) and (max-width: 1024px) {
		
	}

	@media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
		
	}


	@media (min-width: 10px) and (max-width: 767px) {
		.cus-headline-number{
			font-size: 1.3em;
		}

		.cus-headline-text{
			font-size: 1.3em;
			
		}

		.instructor-name{
			font-size:1.7em;
		}

		.instructor-topic{
			font-size:1.4em;
		}

		.v-breadcrumbs li{
		font-size:14px !important;
	}
	}

</style>
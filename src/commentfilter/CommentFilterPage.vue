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
                        <h3>Left Arrow: Delete a comment</h3>
                        <h3>Right Arrow: Send a comment</h3>
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
                    mode:tmp_comment.mode,
                    size:tmp_comment.size}));
                this.comments.splice(0,1);
                this.comments_sent_num += 1;
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
                else if(data.type=="comment_unfiltered"){
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
		getMyCourses(){
			axios.get('/courses/ajax/get_my_courses/',{params: {}}).then(response => {
				this.taking_courses = response.data.taking_courses;
				this.taken_courses = response.data.taken_courses;
				this.taken_courses_semester = this.seperateSemesters(this.taken_courses);
			});
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
            if(key == 37){
                ref.keyLeft();
            }
            else if(key == 39){
                ref.keyRight();
            }

        };
    },
	mounted(){
        this.getSlides();
        this.ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	},
};
</script>

<style>
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
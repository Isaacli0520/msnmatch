<template>
	<v-app>
		<comments-header></comments-header>
		<v-content>
			<v-container fluid grid-list-lg>
				<v-layout col wrap>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Mode</span>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-select
                            v-model="comment_mode"
                            :items="modes"
                            item-text="text"
                            item-value="mode"
                            label="Comment Modes"
                            hide-details
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Color</span>
                    </v-flex>
                    <v-flex>
                        <v-row class="ml-1">
                            <v-btn class="mt-1 mr-1 mb-1" @click="selectColor(color)" height="30" width="5" :color="color" :key="key_color" v-for="(color, key_color) in colors">
                                <v-icon color="teal darken-2" v-if="color == comment_color">fas fa-check</v-icon>
                            </v-btn>
                        </v-row>
                    </v-flex>
                    <!-- <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Size</span>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-btn-toggle
                            v-model="comment_size"
                            mandatory>
                        <v-btn height="30" width="10" :key="key_size" v-for="(size, key_size) in sizes">
                            {{size}}
                        </v-btn>
                        </v-btn-toggle>
                    </v-flex> -->
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Comment or Question</span>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-radio-group hide-details dense v-model="comment_type" mandatory>
                            <v-radio :label="type.text" :value="type.value" :key="type_index" v-for="(type, type_index) in types"></v-radio>
                        </v-radio-group>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Write Your Comment</span>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-textarea
                            v-model="comment_text"
                            auto-grow
                            outlined
                            :error-messages="comment_error_messages"
                            rows="5"
                            row-height="20"
                        ></v-textarea>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-row>
                            <v-spacer></v-spacer>
                            <v-btn outlined color="green" class="ma-2" :disabled="ws_connecting" right @click="sendComment()">Send</v-btn>
                        </v-row>
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
            colors:[
                '#FFFFFF','#000000','#FF0000','#FF69B4','#AA0000',
                '#FFFF00', 
                '#00FF00', '#00FFFF',
                '#0000FF', '#0000AA',
            ],
            sizes:[20, 28, 35],
            types:[
                {text:"Comment",
                 value:0,},
                {text:"Question",
                 value:1,}
            ],
            modes:[
                {"mode":1,
                 "text":"Top-anchored Scrolling"},
                {"mode":2,
                 "text":"Bottom-anchored Scrolling"},
                {"mode":4,
                 "text":"Bottom-anchored Static"},
                {"mode":5,
                 "text":"Top-anchored Static"},
                {"mode":6,
                 "text":"Top-anchored Reverse"},
            ],
            comment_type:0,
            comment_text:"",
            comment_color:"",
            comment_mode:1,
            comment_size:2,
            comment_error_messages:[],
            ws_connecting:true,
		}
	},
	components:{
		CommentsHeader,
	},
	watch: {
        comment_text(val){
            if(val != null){
                this.comment_error_messages = []
            }
        }
	},
	computed:{
	},
	methods: {
		goToHref(text){
			window.location.href = text;
		},
        selectColor(color){
            this.comment_color = color;
        },
        getActiveSlide(){
            axios.get('/comments/api/get_active_slide/',{params: {}}).then(response => {
                this.slide_pk = response.data.slide_pk;
                this.ws_connecting = false;
                this.initFilterSocket(this.slide_pk);
            });
        },
        initFilterSocket(slide_pk){
            var ref = this;
            this.filterSocket = new ReconnectingWebSocket(this.ws_scheme + '://' + 
                window.location.host + "/ws/send_to_filter/");
            this.filterSocket.onopen = function(val){
                console.log("Filter Socket Opened");
                ref.filterSocket.send(JSON.stringify({
                    command:'join',
                    slide_pk:slide_pk,
                }));
            }
            this.filterSocket.onclose = function(e) {
                ref.ws_connecting = true;
                console.error('Chat socket closed unexpectedly');
            };
            this.filterSocket.onmessage = function(comment) {
                var data = JSON.parse(comment.data);
                if(data.type=="join"){
                    ref.ws_connecting = false;
                    console.log("Connected to "+data.slide_pk);
                }
            };
            
        },
        sendComment(){
            if(this.comment_text.length == 0){
                this.comment_error_messages.push("You can't send an empty comment");
            }
            else if(this.comment_text.length > 50){
                this.comment_error_messages.push("Comment is toooo long TAT");
            }
            else{
                this.filterSocket.send(JSON.stringify({
                    command:"send",
                    text:this.comment_text,
                    color:this.comment_color,
                    mode:this.comment_mode,
                    message_type:this.comment_type,
                    time:Date.now(),
                    size:this.sizes[this.comment_size]}));
                this.$message({
                    message: 'Comment Sent',
                    type: 'success'
                });
                this.comment_text = "";
            }
        },
	},
	mounted(){
        this.comment_color = this.colors[0];
        this.ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        this.getActiveSlide();
	},
  };
</script>

<style>
    .v-input--selection-controls{
        margin-top: 0px !important;
    }

    .active-btn{
        border-color: rgb(112, 243, 236) !important;
        border-width: thick !important;
        border-style: solid !important;
    }

    .title-text{
        font-family: "Roboto", sans-serif;
        font-size: 1.6em;
        font-weight: 500;
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
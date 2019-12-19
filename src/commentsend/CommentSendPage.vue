<template>
	<v-app>
		<comments-header></comments-header>
		<v-content>
			<v-container fluid grid-list-lg>
				<v-layout col wrap>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Choose a Mode</span>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-radio-group v-model="comment_mode" mandatory>
                            <v-radio :label="mode.text" :value="mode.mode" :key="mode_index" v-for="(mode, mode_index) in modes"></v-radio>
                        </v-radio-group>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-divider></v-divider>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Choose a Color</span>
                    </v-flex>
                    <v-flex>
                        <v-row>
                            <v-btn class="ma-2" @click="selectColor(color)" :class="[color == comment_color ? 'custom-btn' : '']"  :height="30" :width="10" :color="color" :key="key_color" v-for="(color, key_color) in colors">
                            </v-btn>
                        </v-row>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-divider></v-divider>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <span class="title-text">Choose a Size</span>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-btn-toggle
                            v-model="comment_size"
                            mandatory
                        >
                        <v-btn :height="30" :width="10" :key="key_size" v-for="(size, key_size) in sizes">
                            {{size}}
                        </v-btn>
                        </v-btn-toggle>
                    </v-flex>
                    <v-flex xl12 lg12 md12 sm12 xs12>
                        <v-divider></v-divider>
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
                            <v-btn class="ma-2" right @click="sendComment()">Send</v-btn>
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
                 '#FF0000', '#AA0000', '#550000',
                 '#FFFF00', '#AAAA00', '#555500',
                 '#00FF00', '#00AA00', '#005500',
                 '#00FFFF', '#00AAAA', '#005555',
                 '#0000FF', '#0000AA', '#000055',
            ],
            sizes:[20, 28, 35],
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
            comment_text:"",
            comment_color:"",
            comment_mode:undefined,
            comment_size:undefined,
            comment_error_messages:[],
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
        sendComment(){
            if(this.comment_text.length == 0){
                this.comment_error_messages.push("You can't send an empty comment");
            }
            else{
                this.filterSocket.send(JSON.stringify({
                    command:"send",
                    text:this.comment_text,
                    color:this.comment_color,
                    mode:this.comment_mode,
                    time:Date.now(),
                    size:this.sizes[this.comment_size]}));
            }
        },
	},
	mounted(){
        this.comment_color = this.colors[0];
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        this.filterSocket = new ReconnectingWebSocket(ws_scheme + '://' + 
            window.location.host + "/ws/send_to_filter/");
        
        this.filterSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
        
	},
  };
</script>

<style>
    .custom-btn{
        border-color: white !important;
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
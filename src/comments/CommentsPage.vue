<template>
	<v-app>
		<v-content>
			<div style="top:0; left:0; bottom:0; right:0; width:100%; height:100%; position:absolute;">
				<div class = "abp" style="width:100%; height:100%;">
					<div id="my-comment-stage" style="height:100%; width:100%; padding:0;" class="container">
					<iframe 
						v-if="slide_url != undefined"
						:src="slide_url + 'embed?rm=minimal'"
						frameborder="0" width="100%" height="100%"
						style="z-index:-999;overflow:hidden;"
						allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"
					>
					</iframe>
					</div>
				</div>
			</div>
		</v-content>
	</v-app>
</template>

<script>
import axios from 'axios'

import CommentsHeader from '../components/CommentsHeader'

export default {
	data() {
		return {
			global_time: undefined,
			slide_url: undefined,
		}
	},
	components:{
		CommentsHeader,
	},
	watch: {
	},
	computed:{
		slide_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
		goToHref(text){
			window.location.href = text;
		},
		getURL(){
			axios.get('/comments/api/get_slide/',{params: {slide_pk:this.slide_pk}}).then(response => {
				this.slide_url = response.data.url;
			});
		},
	},
	mounted(){
		this.getURL();
        var ref = this;
        var CM = new CommentManager(document.getElementById('my-comment-stage'));
		CM.init();
        console.log('Start');
		// var danmakuList = [
		// 	{
		// 		"mode":1,
		// 		"text":"Hello World",
		// 		"stime":5000,
		// 		"size":25,
		// 		"color":0xffffff
        //     },
        //     {
		// 		"mode":1,
		// 		"text":"Hello World",
		// 		"stime":5000,
		// 		"size":20,
		// 		"color":0xf2ff2f
        //     },
        //     {
		// 		"mode":1,
		// 		"text":"Hello World",
		// 		"stime":5010,
		// 		"size":34,
		// 		"color":0xf2f3ff
        //     },
        //     {
		// 		"mode":4,
		// 		"text":"Hello World",
		// 		"stime":5020,
		// 		"size":25,
		// 		"color":0xffffff
		// 	},
		// 	{
		// 		"mode":1,
		// 		"text":"Hello World",
		// 		"stime":5050,
		// 		"size":25,
		// 		"color":0xff4ff3
		// 	},
		// ];
		// CM.load(danmakuList);

        CM.start();
        var iVal = -1;
        this.startTime = Date.now();
		if(iVal >= 0){
			clearInterval(iVal);
        }
        iVal = setInterval(function(){
			ref.global_time = Date.now() - ref.startTime;
			CM.time(ref.global_time);
        }, 100);

        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        this.commentSocket = new ReconnectingWebSocket(ws_scheme + '://' + 
            window.location.host + "/ws/send_to_comments/");
		
		this.commentSocket.send(JSON.stringify({
			command:'join',
			slide_pk:this.slide_pk,
		}));

		window.onbeforeunload = function() {
			ref.commentSocket.close();
		};

        this.commentSocket.onclose = function(e) {
            console.error('Comment socket closed unexpectedly');
        };
        this.commentSocket.onmessage = function(comment) {
			var data = JSON.parse(comment.data);
			if(data.type == 'join'){
				console.log("Connected to " + data.slide_pk)
			}
			else if(data.type == 'comment_filtered'){
				var tmp_comment = {
					"mode":data.mode,
					"text":data.text,
					"stime":data.time - ref.startTime + 1000,
					"size":data.size,
					"color":parseInt(data.color.replace(/^#/, ''), 16),
				};
				CM.insert(tmp_comment);
			}
        };
        
	},
  };
</script>

<style>
	.lala{
		height:20px;
		width:20px;
		background-color:red;
		z-index: 100000;
	}

    .cus-container{
        border: 0;
        display: block;
        margin: 0;
        overflow: hidden;
        position: absolute;
        z-index: 9999;
		bottom: 0;
		top: 0;
		left: 0;
		right: 0;
    }

	@media (min-width: 1025px) {
		
	}
	@media (min-width: 960px){
		.container{
			max-width:2000000px !important;
		}
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
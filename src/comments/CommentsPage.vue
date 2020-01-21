<template>
	<v-app>
		<v-content>
			<div style="top:0; left:0; bottom:0; right:0; width:100%; height:100%; position:absolute;">
				<div class = "abp" style="width:100%; height:100%;">
					<div id="my-comment-stage" style="height:100%; width:100%; padding:0;" class="container">
						<iframe 
							id="google-slide"
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
			<div class="question-div">
				<v-col v-if="!hide_question">
					<v-flex class="align-center justify-center ma-2" :key="i" v-for="(question, i) in questions[question_id]">
							<div class="question-span">{{ i + 1 }}. {{question.text}}</div>
					</v-flex>
				</v-col>
			</div>
		</v-content>
	</v-app>
</template>

<script>
import axios from 'axios'

export default {
	data() {
		return {
			question_icon: "fas fa-question",
			global_time: undefined,
			slide_url: undefined,
			hide_question:false,
			questions:[[]],
			question_id:0,
			word_bank:["6666", "awsl", "toxic", "Hello World!", "hhhh", "lol", "PHP is the best!!", "For the Horde!!", "For the Alliance!!", "Testing Testing~~"],
			colors:[
                '#FFFFFF','#000000',
                '#FF0000', '#AA0000', '#550000',
                '#FFFF00', '#AAAA00', '#555500',
                '#00FF00', '#00AA00', '#005500',
                '#00FFFF', '#00AAAA', '#005555',
                '#0000FF', '#0000AA', '#000055',
            ],
		}
	},
	computed:{
		slide_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
		initQuestion(val){
			this.questions = [[]]
			for(let i = 0;i < (val - 1); i++){
				this.questions.push([]);
			}
		},
		initCommentManager(test=false){
			var ref = this;
			this.CM = new CommentManager(document.getElementById('my-comment-stage'));
			this.CM.init();
			console.log('Comment Manager Init');
			var commentList = []
			let word_bank_len = this.word_bank.length;
			let color_len = this.colors.length;
			if(test){
				for(let i = 0; i < 100; i += 1){
					let tmp_mode = 3;
					while(tmp_mode == 3)
						tmp_mode = Math.floor(1 + Math.random()*5);
					commentList.push({
						"mode":tmp_mode,
						"text":this.word_bank[Math.floor(Math.random() * word_bank_len)],
						"stime":2000 + Math.random() * 7000,
						"size":Math.floor(25 + Math.random()*15),
						"color":parseInt(this.colors[Math.floor(Math.random() * color_len)].replace(/^#/, ''),16),
						// "color":parseInt(Math.floor(Math.random()*16777216), 16),
					})
				}
			}
			this.CM.load(commentList);
			this.CM.start();
			this.iVal = -1;
			this.startTime = Date.now();
			if(this.iVal >= 0){
				clearInterval(this.iVal);
			}
			this.iVal = setInterval(function(){
				ref.global_time = Date.now() - ref.startTime;
				ref.CM.time(ref.global_time);
			}, 100);
		},
		initCommentSocket(){
			var ref = this;
        	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
			this.commentSocket = new ReconnectingWebSocket(ws_scheme + '://' + 
				window.location.host + "/ws/send_to_comments/");
			window.onbeforeunload = function() {
				ref.commentSocket.close();
			};
			this.commentSocket.onopen = function(e) {
				console.log('Comment socket open, Connecting to Slide');
				ref.commentSocket.send(JSON.stringify({
					command:'join',
					slide_pk:ref.slide_pk,
				}));
			};
			this.commentSocket.onclose = function(e) {
				console.error('Comment socket closed unexpectedly');
			};
			this.commentSocket.onmessage = function(comment) {
				var data = JSON.parse(comment.data);
				if(data.type == 'join'){
					console.log("Connected to " + data.slide_pk)
				}
				else if(data.message_type == 1){
					ref.questions[data.question_id].push(data);
				}
				else if(data.type == 'comment_filtered'){
					ref.CM.insert({
						"mode":data.mode,
						"text":data.text,
						"stime":data.time - ref.startTime + 1000,
						"size":data.size,
						"color":parseInt(data.color.replace(/^#/, ''), 16),
					});
				}
				else if(data.type == 'question_command'){
					if (data.direction == 'next' && ref.question_id < ref.questions.length)
						ref.question_id += 1;
					else if (data.direction == 'prev' && ref.question_id > 0)
						ref.question_id -= 1;
				}
			};
		},
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
		this.initQuestion(10);
		if(!isNaN(this.slide_pk)){
			this.getURL();
			this.initCommentSocket();
			this.initCommentManager();
		}
	},
  };
</script>

<style>

	.question-div{
		z-index: 99999;
		margin: 0 auto;
		width: 65%;
		height: 100%;
		position: fixed;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		justify-content: center;
		display: flex;
		align-items: center;
	}

	.question-span{
		text-align:center;
		align-items: center;
		justify-content: center;
		font-size: 31px;
		color: #f6e6ec;
		padding: 8px;
		border-radius: 10px;
		font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
		/* background-color: rgb(246, 230, 236); */
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
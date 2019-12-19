<template>
	<v-app>
		<comments-header></comments-header>
		<v-content>
			<v-container fluid grid-list-lg>
				<div id="my-player" class="abp" style="width:100%; height:500px; background:#000;">
                    <div id="my-comment-stage" class="container"></div>
                </div>
                <div><span>{{global_time}}</span></div>
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
            taking_courses:[],
            global_time: undefined,
		}
	},
	components:{
		CommentsHeader,
	},
	watch: {

	},
	computed:{
	},
	methods: {
		goToHref(text){
			window.location.href = text;
		},
		getMyCourses(){
			axios.get('/courses/ajax/get_my_courses/',{params: {}}).then(response => {
				this.taking_courses = response.data.taking_courses;
				this.taken_courses = response.data.taken_courses;
				this.taken_courses_semester = this.seperateSemesters(this.taken_courses);
			});
		},
	},
	mounted(){
        var CM = new CommentManager(document.getElementById('my-comment-stage'));
		CM.init();
        console.log('Start');
		// var danmakuList = [
		// 	{
		// 		"mode":1,
		// 		"text":"Hello World",
		// 		"stime":0,
		// 		"size":25,
		// 		"color":0xffffff
		// 	}
		// ];
		// CM.load(danmakuList);

        CM.start();
        var iVal = -1;
        this.startTime = Date.now(); // 设定起始时间
		if(iVal >= 0){
			clearInterval(iVal); // 如果之前就有定时器，把它停掉
        }
        var ref = this;
        iVal = setInterval(function(){
			ref.global_time = Date.now() - ref.startTime; // 用起始时间和现在时间的差模拟播放
			CM.time(ref.global_time); // 通报播放时间
        }, 100);
        
        // var someDanmakuAObj = {
        //         "mode":1,
        //         "text":"Hello CommentCoreLibrary",
        //         "stime":Date.now()+ 1000 - ref.startTime,
        //         "size":30,
        //         "color":0xff0000
        //     };
        //     CM.insert(someDanmakuAObj);

        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        this.socketSocket = new ReconnectingWebSocket(ws_scheme + '://' + 
            window.location.host + "/ws/send_to_comments/");
        
        this.socketSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
        this.socketSocket.onmessage = function(comment) {
            var data = JSON.parse(comment.data);
            var tmp_comment = {
                "mode":data.mode,
                "text":data.text,
                "stime":data.time - ref.startTime + 100,
                "size":data.size,
                "color":parseInt(data.color.replace(/^#/, ''), 16),
            };
            console.log("comment received");
            console.log(tmp_comment);
            CM.insert(tmp_comment);
        };
        
	},
  };
</script>

<style>

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
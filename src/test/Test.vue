<template>
	<v-app>
		<v-content>
			<div id="my-player" class="abp" style="width:100%; height:300px; background:#000;">
                <div id="my-comment-stage" class="container"></div>
            </div>
            
            <!-- 当然可以放很多别的东西 -->
            <div class="controlbox">
                <h3>调试用绑定</h3>
                <p>这里提供了一些调试用的绑定，可以通过操作它们感受操控 CCL 的方法。打开 main.js 就可以看到实现这些方法的绑定函数。</p>
                <ul>
                    <li><a href="#" id="btnLoadTimeline">载入一个弹幕列表</a></li>
                    <li><a href="#" id="btnInsertTimeline">插入一个弹幕到弹幕列表</a></li>
                    <li><a href="#" id="btnTimer">启用/重置 定时器来告知播放器目前的播放位置</a> <span id="txPlayPos">0</span></li>
                </ul>
            </div>
		</v-content>
	</v-app>
</template>

<script>
import axios from 'axios'
import jquery from 'jquery'

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
		
	},
	mounted(){
        function $(element){
	// 获取 DOM 对象的短写，如果你在用 jQuery 也可以采用类似的方法
	return document.getElementById(element);
};

window.addEventListener('load', function(){
	// 在窗体载入完毕后再绑定
	var CM = new CommentManager($('my-comment-stage'));
	CM.init();
	
	// 先启用弹幕播放（之后可以停止）
	CM.start();
	
	// 绑定按钮们
	$('btnLoadTimeline').addEventListener('click', function(e){
		e.preventDefault(); // 抑制默认操作
		var danmakuTimeline = [
			{
				"mode":1,
				"text":"Hello World",
				"stime":0,
				"size":25,
				"color":0xffffff
			}
		];
		CM.load(danmakuTimeline);
	});
	
	$('btnInsertTimeline').addEventListener('click', function(e){
		e.preventDefault(); // 抑制默认操作
		var danmaku = {
			"mode":1,
			"text":"Hello CommentCoreLibrary",
			"stime":1000,
			"size":30,
			"color":0xff0000
		};
		CM.insert(danmaku);
	});
	
	var startTime = 0, iVal = -1;
	$('btnTimer').addEventListener('click', function(e){
		e.preventDefault(); // 抑制默认操作
		startTime = Date.now(); // 设定起始时间
		if(iVal >= 0){
			clearInterval(iVal); // 如果之前就有定时器，把它停掉
		}
		//建立新的定时器
		iVal = setInterval(function(){
			var playTime = Date.now() - startTime; // 用起始时间和现在时间的差模拟播放
			CM.time(playTime); // 通报播放时间
			$('txPlayPos').textContent = playTime; // 显示播放时间
		}, 100); // 模拟播放器每 100ms 通报播放时间
	});
	
	// 开放 CM 对象到全局这样就可以在 console 终端里操控
	window.CM = CM;
});
    }
  };
</script>

<style>

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
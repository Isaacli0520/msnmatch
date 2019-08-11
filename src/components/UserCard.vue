<template>
<div class="card user-card">
    <div class="user-card-inner">
        <div id="show-modal" @click="openModal(user)">
            <progressive-img v-if="user.picture" 
                :src="user.picture" 
                :placeholder="user.avatar"
                :blur="10"
                />
        </div>
        <div class="card-body">
            <div class="title d-flex w-100 justify-content-between">
                <h5 class="mb-1 font-weight-bold">
                    {{user.first_name}} {{user.last_name}}
                </h5>
                <small style="float:right;">{{ user.year }}</small>
            </div>
            <div class="title d-flex w-100 justify-content-between">
                <small v-if="user.major" class="text-muted">Major: {{ user.major }}</small>
            </div>
            <div class="user-id-tags">
                <span v-if="user.role" class="user-id-tag" :class="user.role">{{ user.role }}</span>
                <span v-if="user.video.length" class="user-id-tag user-id-tag-video">Video</span>
                <span v-if="user.bio && wordCount(user.bio) > 100" class="user-id-tag user-id-tag-bio">百字Bio</span>
                <span v-if="user.follow" class="user-id-tag user-id-tag-fav">Like</span>
                <span v-if="user.matched" class="user-id-tag user-id-tag-match">Matched</span>
            </div>
            <small v-if="user.score && user.score > 0" class="score-text">Similarity: {{ user.score }}%</small>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import VueProgressiveImage from 'vue-progressive-image'

Vue.use(VueProgressiveImage, {})

export default {
    props: {
        user: Object,
    },
    methods: {
        wordCount(str){
            let sLen = 0;
            try{
                //先将回车换行符做特殊处理
                let tmpstr = str.replace(/(\r\n+|\s+|　+)/g,"龘");
                //处理英文字符数字，连续字母、数字、英文符号视为一个单词
                tmpstr = tmpstr.replace(/[\x00-\xff]/g,"m");
                //合并字符m，连续字母、数字、英文符号视为一个单词
                tmpstr = tmpstr.replace(/m+/g,"*");
                //去掉回车换行符
                tmpstr = tmpstr.replace(/龘+/g,"");
                //返回字数
                sLen = tmpstr.length;
            }catch(e){
            }
            return sLen;
        },
        openModal(modal_user){
            this.$emit('open-modal', modal_user);
        }
    },
    computed: {
    }
}
</script>

<style scoped lang="css">
    *{
        box-sizing: border-box;
    }
    .user-card {
        /* margin:10px; */
        margin: 3px 3px 0.75em 3px;
        flex: 1 0 auto;
        overflow:hidden;
        /* width: 30%; */
    }

    .user-id-tags{
        margin: 0px 0px 3px 0px;
        display: flex;
        flex-flow: row wrap;
        width:100%;
    }

    .user-id-tag{
        font-size: 12px;
        font-weight: 500;
        padding: 2px 6px 2px 6px;
        margin: 5px 4px 0px 0px;
        border-radius: 4px;
    }

    .user-id-tag-fav{
        color:#ffffff;
        background: rgba(255, 0, 43, 0.993);
    }

    .user-id-tag-video{
        color:#ffffff;
        background: #de21f0;
    }

    .user-id-tag-bio{
        color:#ffffff;
        background: #f0d121;
    }

    .user-id-tag-match{
        color:#ffffff;
        background: #f07421ea;
    }

    .Mentor{
        color:#ffffff;
        background: rgba(26, 158, 235, 0.781);
    }

    .Mentee{
        color:#ffffff;
        background: rgba(9, 194, 40, 0.781);
    }

    .score-text{
        color:#2b9761;
        font-weight: 550;
    }
</style>
<template>
<div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-8 col-xs-offset-0 col-sm-offset-0 container" style="width:100%; margin: 0 auto;">
    <div class="big-title mt-2 mb-2 text-center">
        <span>{{ group.group_name }}</span>
    </div>
    <hr>
    <div class= "users-manager">
        <div class="all-users">
            <div class="user-div" :key="user.pk" v-for="user in group.managers">
                <a :href="user.user_url" class="user-main">
                    <span class="font-weight-bold">{{ user.first_name }} {{ user.last_name }}</span>
                </a>
                <span class="user-year">{{ user.year }}</span>
            </div>
        </div>
    </div>
    <div class= "users-member">
        <div class="all-users">
            <div class="user-div" :key="user.pk" v-for="user in group.members">
                <a :href="user.user_url" class="user-main">
                    <span class="font-weight-bold">{{ user.first_name }} {{ user.last_name }}</span>
                </a>
                <span class="user-year">{{ user.year }}</span>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import VueProgressiveImage from 'vue-progressive-image'
import axios from 'axios'

Vue.use(VueProgressiveImage)

export default {
    data: function(){
        return{
            group:{},
        }
    },
    methods: {
        openModal(modal_user){
            this.$emit('open-modal', modal_user);
        },
        redirectToGroup(group_pk){
            window.location.href = "/groups/"+ group_pk.toString(10);
        },
    },
    filters: {
        pluralize: function (value) {
            if (value > 1){
                return value.toString(10) + " Users";
            }else{
                return value.toString(10) + " User";
            }
        },
    },
    computed: {
    },
    mounted(){
        let url = window.location.pathname.split('/');
        console.log("url",window.location.pathname,'----', url, '---', url[url.length - 2]);
        axios.get('/groups/ajax/get_group/',{params: {'group_pk': url[url.length - 2]}}).then(response => {
            this.group = response.data.groups[0]; 
        });
    },
}
</script>

<style scoped lang="css">
    *{
        box-sizing: border-box;
    }

    .big-title{
        color:#000000;
        font-weight: 500;
        font-size: 42px !important;
        font-family: Baskerville, "Baskerville Old Face", sans-serif;
    }

    .user-div{
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
        border-radius: 8px;
        margin: 5px 10px 5px 10px;
        padding: 8px 14px 8px 20px;
        overflow: hidden;
        background: #ffffff;  
        
    }

    .user-main{
        font-size: 20px;
    }

    .back-btn{
        float:right; 
        padding:7px 25px 7px 25px;
        margin: 5px 9px 0px 0px;
    }

    .user-year{
        font-size: 15px !important;
        float:right;
        padding: 3px 8px 3px 8px;
        border-radius: 5px;
        margin: 0px 0px 0px 5px;
        font-family: Gill Sans, sans-serif;
        color: #ffffff;
        background-color: #ff5c5c;
    }






</style>
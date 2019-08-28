<template>
<div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-8 col-xs-offset-0 col-sm-offset-0 container" style="width:100%; margin: 0 auto;">
    <div class="big-title mt-2 mb-2 text-center">
        <span>{{ group.group_name }}</span>
    </div>
    <hr>
    <div class="row w-100">
        <div class="col-7 card-columns custom-card-columns">
            <div class="card users-manager custom-card ">
                <div class="card-body">
                    <h5 class="card-title custom-card-title">Managers</h5>
                    <div class="all-users">
                        <div class="user-div" :key="user.pk" v-for="user in group.managers">
                            <a :href="user.user_url" class="user-main">
                                <span class="font-weight-bold">{{ user.first_name }} {{ user.last_name }}</span>
                            </a>
                            <span class="user-year">{{ user.year }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card users-member custom-card">
                <div class="card-body">
                    <h5 class="card-title custom-card-title">Members</h5>
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
        </div>
        <div class="col-5">
            <div class="card w-100 custom-card">
                <img :src="group.picture" class="card-img-top" alt="none">
                <div class="card-body">
                    <div>
                        <a v-if="edit" :href="group_edit_url">Edit Group</a>
                    </div>
                    <div>
                        <a v-if="edit" :href="group_tag_url">Add Tags</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import VueProgressiveImage from 'vue-progressive-image'
import axios from 'axios'

Vue.use(VueProgressiveImage, {})

export default {
    data: function(){
        return{
            group:{},
            edit:false,

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
        group_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
        group_edit_url: function(){
            return '/groups/' + this.group_pk + '/edit/';
        },
        group_tag_url: function(){
            return '/groups/' + this.group_pk + '/tags/';
        },
    },
    mounted(){
        axios.get('/groups/ajax/get_group/',{params: {'group_pk': this.group_pk}}).then(response => {
            this.group = response.data.groups[0]; 
        });
        axios.get('/groups/ajax/get_group_edit/',{params: {'group_pk': this.group_pk}}).then(response => {
            this.edit = response.data.edit; 
        });
    },
}
</script>

<style scoped lang="css">
    *{
        box-sizing: border-box;
    }

    .custom-card-columns{
        column-count: 1 !important;
    }

    .custom-card{
        padding: 0px 10px 0px 10px;
        margin-bottom: 20px !important;
    }

    .custom-card-title{
        color:#32a49a;
        font-weight: 500;
        font-size: 29px !important;
        font-family: Baskerville, "Baskerville Old Face", sans-serif;
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
        margin: 5px 0px 5px 0px;
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
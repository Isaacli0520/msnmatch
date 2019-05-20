<template>
<div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-8 col-xs-offset-0 col-sm-offset-0 container" style="width:100%; margin: 0 auto;">
    <h1 class="text-center">{{ group.group_name }}</h1>
    <hr>
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


</style>
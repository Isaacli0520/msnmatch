<template>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="fav-dropdown" role="button" data-toggle="dropdown" aria-haspopup="true">
            <i class="fas fa-heart"></i>
        </a>
        <div class="dropdown-menu custom-drop-menu dropdown-menu-right" @click.stop="" aria-labelledby="fav-dropdown">
                <a class="dropdown-item" v-if="following.length == 0">No Favorites</a>
                <div class="dropdown-item custom-drop-item d-flex w-100 justify-content-between" v-for="(following_user, index) in following">
                    <span class="follow-rank">{{index + 1}}</span>
                    <a :href="following_user.user_url"><span class="follow-name">{{ following_user.first_name }} {{ following_user.last_name }}</span></a>
                    <span class="trash-btn" @click="del_fav(following_user)"><i class="fas fa-trash-alt"></i></span>
                </div>
        </div>
    </li>
</template>


<script>
import axios from 'axios'

export default {
    props:{
        following:Array,

    },
    data: function(){
        return {
        }
    },
    filters: {
        numbers: function (num) {
            let tmp_arr = ["st", "nd", "rd"];
            return (num + 1).toString() + tmp_arr[num];
        }
    },
    methods:{
        del_fav(following_user){
        axios.get('/skills/ajax/del_fav/',{params: {user_pk:following_user.pk}}).then(response => {
            $('#follow-btn').popover('hide')
            $('#follow-btn').popover('disable')
            this.$emit("update-following-list",following_user, 0);
        });
        },
        
    },
    mounted(){
    },
}
</script>

<style scoped lang="css">

    .custom-drop-menu{
        box-shadow: 0 2px 5px 0px rgba(0,0,0,.16), 0 2px 10px 0px rgba(0,0,0,.12);
    }

    *{
        box-sizing: border-box;
    }
    .custom-drop-item{
        padding: 1px 8px 1px 8px;
        overflow: hidden;

    }
    .follow-name{
        text-transform:none;
    }
    .trash-btn{
        padding:14px 4px 8px 8px;
    }
    .follow-rank{
        font-size: 15px !important;
        float: left;
        padding: 9px 2px 4px 8px;
        /* border-radius: 5px; */
        margin: 0px 2px 0px 0px;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
        color: #000000;
        /* background-color: #ff5c5c; */
    }
</style>
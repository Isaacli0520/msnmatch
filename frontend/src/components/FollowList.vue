<template>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="fav-dropdown" role="button" data-toggle="dropdown" aria-haspopup="true">
            <i class="fas fa-heart"></i>
        </a>
        <div class="dropdown-menu dropdown-menu-right" @click.stop="" aria-labelledby="navbarDropdown">
                <a class="dropdown-item" v-if="following.length == 0">No Favorites</a>
                <div class="dropdown-item d-flex w-100 justify-content-between" v-for="following_user in following">
                    <a :href="following_user.user_url"><span>{{ following_user.first_name }} {{ following_user.last_name }}</span></a>
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
    *{
        box-sizing: border-box;
    }
    .trash-btn{
        padding:12px 4px 8px 4px;
    }
</style>
<template>
    <div class="mt-3 mb-3 col-xs-12 col-sm-12 col-md-10 col-lg-8 col-xs-offset-0 col-sm-offset-0 container" id="admin-app" style="width:100%; margin: 0 auto;">
        <div class="big-title text-center mt-3 mb-3">
            <span>Super Cool Admin Page</span>
        </div>
        <user-rank-list
        v-bind:all_users="all_users"
        v-bind:all_users_list="all_users_list"/>
    </div>
</template>

<script>
import UserRankList from '../components/UserRankList'
import axios from 'axios'

export default {
    name: 'SuperAdmin',
    components: {
        UserRankList,
    },
    data () {
        return {
        all_users: {},
        all_users_list:[],
        }
    },
    methods:{},
    mounted(){
        axios.get('/ajax/get_all_ranked_users/',{params: {}}).then(response => {
            // console.log(response.data.all_users);
            this.all_users = response.data.all_users;
            let tmp_arr = [];
            for (const [ key, value ] of Object.entries(this.all_users)) {
                tmp_arr = tmp_arr.concat(value);
            }
            tmp_arr = tmp_arr.sort(function(a,b){
                return b.follow.length - a.follow.length;
            });
            this.all_users_list = tmp_arr;
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

</style>
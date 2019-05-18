<template>
    <div class="all-users">
        <div v-for="user in all_users_list">
            <div class="user-big-div">
                <div class="user-div" @click=collapseDiv(user.pk)>
                    <span class="user-main font-weight-bold">{{ user.first_name }} {{ user.last_name }}</span>
                    <span v-if="user.role" class="user-role" :class="user.role">{{ user.role }}</span> 
                    <span v-if="user.year" class="user-year">{{ user.year }}</span>
                    <span v-if="user.follow.length > 0" class="user-follow">{{ user.follow.length | pluralize }}</span>
                </div>
                <div class="collapse multi-collapse" :id="user.pk">
                    <div class="card card-body w-100">
                        <span class="text-center">Followed by</span>
                        <div class=" card-columns">
                            <user-card-min
                            v-for="user_flw_pk in user.follow"
                            v-bind:key="user_flw_pk"
                            v-bind:tmp_user="all_users[user_flw_pk]"
                            />
                        </div>
                        <hr>
                        <span class="text-center">Followed</span>
                        <div class=" card-columns">
                            <user-card-min
                            v-for="user_flwee_pk in user.followee"
                            v-bind:key="user_flwee_pk"
                            v-bind:tmp_user="all_users[user_flwee_pk]"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import UserCardMin from './UserCardMin'

export default {
    props: {
      all_users: Object,
      all_users_list: Array,
    },
    components: {
        UserCardMin
    },
    methods:{
        collapseDiv(user_pk){
            let tmp_string = "#" + user_pk;
            $(tmp_string).collapse('toggle');
        },
    },
    filters: {
        pluralize: function (value) {
            if (value > 1){
                return value.toString(10) + " Followers";
            }else{
                return value.toString(10) + " Follower";
            }
        },
    },
    mixins: [],
    computed: {
      
    }
}
</script>

<style scoped lang="css">
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

.user-follow{
    font-size: 15px !important;
    float:right;
    padding: 3px 8px 3px 8px;
    border-radius: 5px;
    margin: 0px 0px 0px 5px;
    font-family: Gill Sans, sans-serif;
    color: #ffffff;
    background-color: #e714dd;
}

.user-role{
    font-size: 15px !important;
    float:right;
    padding: 3px 8px 3px 8px;
    border-radius: 5px;
    margin: 0px 0px 0px 5px;
    font-family: Gill Sans, sans-serif;
}

.Mentor{
    color:#ffffff;
    background: rgba(26, 158, 235, 0.781);
}
  
.Mentee{
    color:#ffffff;
    background: rgba(9, 194, 40, 0.781);
}    
</style>
<template>
    <v-app>
        <v-content>
            <v-container>
                <div class="big-title text-center mt-3 mb-3">
                    <span>Super Cool Admin Page</span>
                </div>
                <v-expansion-panels multiple>
                    <v-expansion-panel :key="user.pk" v-for="user in all_users_list">
                        <v-expansion-panel-header>
                            <div style="clear:both;display:block;">
                            <span class="user-main font-weight-bold">{{ user.first_name }} {{ user.last_name }}</span>
                            <span v-if="user.role" class="user-tag" :class="user.role">{{ user.role }}</span> 
                            <span v-if="user.year" class="user-tag user-year">{{ "year " + (2025 - user.year) }}</span>
                            <span v-if="user.follow.length > 0" class="user-tag user-follower">{{ user.follow.length | pluralize_follower }}</span>
                            <span v-if="user.followee.length > 0" class="user-tag user-followee">{{ user.followee.length | pluralize_followee }}</span>
                            </div>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <v-card>
                                <v-card-title>Followed By</v-card-title>
                                <v-card-text>
                                    <v-row>
                                        <v-col
                                        v-for="(us_pk, i) in user.follow"
                                        :key="i"
                                        cols="12"
                                        sm="6"
                                        md="4"
                                        lg="4"
                                        xl="3">
                                            <user-card
                                                class="fill-height"
                                                :user="all_users[us_pk]"></user-card>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                            </v-card>
                            <v-card style="margin-top:10px;">
                                <v-card-title>Followed</v-card-title>
                                <v-card-text>
                                    <v-row>
                                        <v-col
                                        v-for="(us_pk, i) in user.followee"
                                        :key="i"
                                        cols="12"
                                        sm="6"
                                        md="4"
                                        lg="4"
                                        xl="3">
                                            <user-card
                                                class="fill-height"
                                                :user="all_users[us_pk]"></user-card>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                            </v-card>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import UserCard from '../components/UserCard'

export default {
    name: 'SuperAdmin',
    components: {
        UserCard
    },
    data () {
        return {
        all_users: {},
        all_users_list:[],
        }
    },
    methods:{},
    filters: {
        pluralize_follower: function (value) {
            if (value > 1){
                return value.toString(10) + " Followers";
            }else{
                return value.toString(10) + " Follower";
            }
        },
        pluralize_followee: function (value) {
            if (value > 1){
                return value.toString(10) + " Followees";
            }else{
                return value.toString(10) + " Followee";
            }
        },
    },
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

    .user-main{
        font-size: 20px;
    }

    .user-tag{
        font-size: 15px !important;
        float:right;
        padding: 5px 8px 5px 8px;
        border-radius: 5px;
        margin: 0px 0px 0px 5px;
        font-family: Gill Sans, sans-serif;
        color: #ffffff;
        align-items: center;
    }

    .user-year{
        background-color: #ff5c5c;
    }

    .user-follower{
        background-color: #e714dd;
    }

    .user-followee{
        background-color: #ff237e;
    }

    .Mentor{
        background: rgba(26, 158, 235, 0.781);
    }
    
    .Mentee{
        background: rgba(9, 194, 40, 0.781);
    }    

    .big-title{
        color:#000000;
        font-weight: 500;
        font-size: 42px !important;
        font-family: Baskerville, "Baskerville Old Face", sans-serif;
    }

</style>
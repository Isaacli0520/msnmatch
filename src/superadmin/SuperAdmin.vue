<template>
    <v-app>
        <v-main>
            <v-container>
                <div class="big-title text-center mt-3 mb-3">
                    <span>Super Cool Admin Page</span>
                </div>
                <v-row v-if="false">
                    <v-col cols="4">
                        <v-card>
                            <v-row justify="center">
                                <v-date-picker
                                    v-model="date"
                                    class="ma-2"
                                ></v-date-picker>
                            </v-row>
                        </v-card>
                    </v-col>
                    <v-col cols="4">
                        <v-card>
                            <v-card-title>
                                <v-btn outlined color="teal darken-2" @click="getReviewUsers()">Get Users!</v-btn>
                            </v-card-title>
                            <v-card-text>
                                <v-list two-line="">
                                    <v-list-item :key="user.username" v-for="user in review_users">
                                        <v-list-item-content>
                                            <v-list-item-title v-text="user.name"></v-list-item-title>
                                            <v-list-item-subtitle v-text="user.reviews"></v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col cols="4">
                        <v-card>
                            <v-card-title>
                                <v-container>
                                    <v-row>
                                        <v-text-field v-model="tot_winners" label="Total Winners"></v-text-field>
                                    </v-row>
                                    <v-row>
                                        <v-btn outlined color="teal darken-2" @click="getRollUsers()">Roll!</v-btn>
                                    </v-row>
                                </v-container>
                            </v-card-title>
                            <v-card-text>
                                <v-list two-line="">
                                    <v-list-item :key="user.username" v-for="user in roll_users">
                                        <v-list-item-content>
                                            <v-list-item-title v-text="user.name"></v-list-item-title>
                                            <v-list-item-subtitle v-text="user.reviews"></v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
                <v-expansion-panels multiple>
                    <v-expansion-panel :key="user.pk" v-for="user in all_users_list">
                        <v-expansion-panel-header>
                            <div style="clear:both;display:block;">
                            <span class="user-main font-weight-bold">{{ user.first_name }} {{ user.last_name }}</span>
                            <span v-if="user.role" class="user-tag" :class="user.role">{{ user.role }}</span> 
                            <span v-if="user.year" class="user-tag user-year">{{ "year " + (2025 - user.year) }}</span>
                            <span v-if="user.matched" class="user-tag user-matched">matched</span>
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
                                                @open-user-dialog="matchUser(us_pk, user.pk)"
                                                :superadmin="true"
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
                                                @open-user-dialog="matchUser(us_pk, user.pk)"
                                                :superadmin="true"
                                                :user="all_users[us_pk]"></user-card>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                            </v-card>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-container>
        </v-main>
        <v-dialog v-model="match_dialog" scrollable min-width="200px" max-width="600px">
            <v-card>
                <v-card-title>三思啊少女/少年</v-card-title>
                <v-divider></v-divider>
                <v-card-text  style="color:black;margin-top:21px; font-size:16px;font-weight:500;">
                    {{match_text}}
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" :loading="matchBtnLoading" outlined @click="matchRequest(user_1_pk, user_2_pk)">Yes</v-btn>
                    <v-btn color="red lighten-1" outlined @click="match_dialog = false">No</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            Sth is wrong
            <v-btn color="white" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="2700">
            Users matched
            <template v-slot:action="{ attrs }">
                <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
    </v-app>
</template>

<script>
import axios from 'axios'
import UserCard from '../components/UserCard'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    name: 'SuperAdmin',
    components: {
        UserCard
    },
    data(){
        return {
            date: '2020-11-26',
            review_users:[],
            roll_users:[],
            tot_winners:1,
            matchBtnLoading:false,
            match_dialog:false,
            match_text:"",
            failure_snack:false,
            success_snack:false,
            user_1_pk:-1,
            user_2_pk:-1,
            all_users: {},
            all_users_list:[],
        }
    },
    watch:{
        // date(value){
        //     console.log("Date:", value);
        // },
    },
    methods:{
        getReviewUsers(){
            axios.get('/courses/api/get_top_review_users/',{params: {date:this.date}}).then(response => {
                this.review_users = response.data.review_users;
            });
        },
        getRollUsers(){
            axios.get('/courses/api/get_roll_result/',{params: {date:this.date, tot_winners:this.tot_winners}}).then(response => {
                this.roll_users = response.data.users;
            });
        },
        matchUser(user_1_pk, user_2_pk){
            this.match_text = "Do you really wanna match "
             + this.all_users[user_1_pk].first_name + " " + this.all_users[user_1_pk].last_name
             + " with " + this.all_users[user_2_pk].first_name + " " + this.all_users[user_2_pk].last_name
             + "?";
            this.user_1_pk = user_1_pk;
            this.user_2_pk = user_2_pk;
            this.match_dialog = true;
        },
        matchRequest(user_1_pk, user_2_pk){
            this.matchBtnLoading = true;
            axios.post('/users/api/match_user/', {
                "user_1":user_1_pk,
                "user_2":user_2_pk,
            }).then(response => {
                this.matchBtnLoading = false;
                this.match_dialog = false;
                if (response.data.success){
                    this.all_users[user_1_pk].matched = true;
                    this.all_users[user_2_pk].matched = true;
                    for(let i = 0;i < this.all_users_list.length; i = i + 1){
                        if(this.all_users_list[i].pk == user_1_pk || this.all_users_list[i].pk == user_2_pk){
                            this.all_users_list[i].matched = true;
                        }
                    }
                    let ref = this;
                    this.all_users_list.sort(function(a,b){
                        return ref.cmp(b.follow.length, a.follow.length);
                    }).sort(function(a, b){
                        return ref.cmp(a.matched | 0, b.matched | 0);
                    });
                    this.success_snack = true;
                }else{
                    this.failure_snack = true;
                }
            });
        },
        cmp(a, b){
            if(a > b) return +1;
            if(a < b) return -1;
            return 0
        },
    },
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
        axios.get('/api/get_all_ranked_users/',{params: {}}).then(response => {
            this.all_users = response.data.all_users;
            let ref = this;
            let tmp_arr = [];
            for (const [ key, value ] of Object.entries(this.all_users)) {
                tmp_arr.push(value);
            }
            this.all_users_list = tmp_arr.sort(function(a,b){
                return ref.cmp(b.follow.length, a.follow.length);
            }).sort(function(a, b){
                return ref.cmp(a.matched | 0, b.matched | 0);
            });
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

    .user-matched{
        background-color: #ffc13c;
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
<template>
    <v-app>
        <match-header></match-header>
        <v-content>
            <v-container v-if="!loaded" fluid fill-height>
                <v-layout 
                    align-center
                    justify-center>
                    <div>
                        <v-progress-circular
                        :size="60"
                        :width="6"
                        indeterminate
                        color="teal lighten-1">
                        </v-progress-circular>
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="!user && loaded" fluid fill-height>
                <v-layout 
                    align-center
                    justify-center>
                    <div class="item-not-exist">
                        User does not exist~~
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="user && loaded" fluid grid-list-lg>
                <v-row>
                    <v-col cols="12" sm="6" md="5" lg="5" xl="5">
                        <v-card>
                            <v-img
                            aspect-ratio="1.33"
                            :src="user.picture">
                            </v-img>
                            <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title>
                            <template v-if="editable">
                                <v-divider></v-divider>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn
                                        :href="'/users/' + username + '/edit/'"
                                        color="purple"
                                        text>
                                        Edit Profile
                                    </v-btn>
                                </v-card-actions>
                            </template>
                        </v-card>
                    </v-col>
                    <v-col cols="12" sm="6" md="7" lg="7" xl="7">
                            <v-card style="margin-bottom:15px;">
                                <v-card-title>Basic Info</v-card-title>
                                <v-divider></v-divider>
                                <v-card-text>
                                    <table class="cus-table">
                                        <colgroup>
                                            <col class="left-tr" />
                                            <col class="right-td" />
                                        </colgroup>
                                        <tbody>
                                            <tr>
                                                <td>Gender</td>
                                                <td>{{ user.sex }}</td>
                                            </tr>
                                            <tr>
                                                <td>Graduate Year</td>
                                                <td>{{ user.graduate_year }}</td>
                                            </tr>
                                            <tr>
                                                <td>Major</td>
                                                <td>{{ user.major }}</td>
                                            </tr>
                                            <tr v-if="user.major_two">
                                                <td>Second Major</td>
                                                <td>{{ user.major_two }}</td>
                                            </tr>
                                            <tr v-if="user.minor">
                                                <td>Minor</td>
                                                <td>{{ user.minor }}</td>
                                            </tr>
                                            <tr>
                                                <td style="vertical-align:top;">Bio</td>
                                                <td class="description-td">{{ user.bio }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </v-card-text>
                            </v-card>
                            <v-card>
                                <v-card-title>Contact Info</v-card-title>
                                <v-divider></v-divider>
                                <v-card-text>
                                    <table class="cus-table">
                                        <colgroup>
                                            <col class="left-tr" />
                                            <col class="right-td" />
                                        </colgroup>
                                        <tbody>
                                            <tr v-if="user.wechat">
                                                <td>WeChat ID</td>
                                                <td>{{ user.wechat }}</td>
                                            </tr>
                                            <tr>
                                                <td>Email</td>
                                                <td>{{ user.email }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </v-card-text>
                            </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'

  export default {
	data() {
        return {
            loaded:false,
            user:null,
            editable:false,
        }
	},
	components:{
        MatchHeader,
	},
	watch: {
        
	},
	computed:{
        username: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
        getProfile(username){
            axios.get('/users/api/get_profile/',{params: {username:username}}).then(response => {
                if(response.data.success){
                    this.user = response.data.user;
                    this.editable = response.data.editable;
                }
                this.loaded = true;
            });
        },
	},
	mounted(){
        this.getProfile(this.username);
	},
  };
</script>

<style>
    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {

    }


    @media (min-width: 10px) and (max-width: 767px) {
        
    }


</style>
<template>
    <v-app>
        <match-header></match-header>
        <v-main>
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
            <v-container v-if="loaded && skill==null">
                <v-layout 
                    align-center
                    justify-center>
                    <div class="skill-not-exist">
                        Skill does not exist~~
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="loaded && skill">
                <v-row justify="center">
                    <v-card>
                        <v-card-title>{{skill.name}}</v-card-title>
                        <v-card-subtitle>{{skill.type}}</v-card-subtitle>
                        <v-divider></v-divider>
                        <v-card-text>
                            <v-list two-line>
                                <v-list-item
                                    v-for="user in users"
                                    :key="user.username"
                                    :href="'/users/' + user.username">

                                    <v-list-item-content>
                                        <v-list-item-title>{{user.first_name + " " + user.last_name}}</v-list-item-title>
                                        <v-list-item-subtitle>{{year_str(user.year)}}</v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-card-text>
                    </v-card>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import axios from 'axios'
import { MatchHeader } from '../components'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    data() {
        return {
            loaded:false,
            users:null,
            skill:null,
        }
    },
    components:{
        MatchHeader,
    },
    computed:{
        skill_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
    },
    methods: {
        getSkill(){
            axios.get('/skills/api/get_skill/',{params:{"id":this.skill_pk}}).then(response => {
                if(response.data.success){
                    this.users = response.data.users;
                    this.skill = response.data.skill;
                }
                this.loaded = true;
            });
        },
        year_str(year){
            if(year.length == 0) return "";
            if(year == 1){
                return "1st year";
            }
            else if(year == 2){
                return "2nd year";
            }
            else if(year == 3){
                return "3rd year";
            }
            else if(year == 4){
                return "4th year";
            }
            else{
                return "";
            }
        },
    },
    mounted(){
        this.getSkill();
    },
};
</script>

<style>
    .cus-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 2.1em;
        font-weight: 300;
        color:rgb(0, 0, 0);
        padding: 1px 12px 7px 3px;
        border-radius: 5px;
        line-height: 1.0;
    }

    .skill-not-exist{
        font-size: 25px;
    }

    .skill-type-text{
        color: #32a49a;
        font-family: Palatino, URW Palladio L, serif;
    }

    .skill-tags{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 5px 0px 20px 0px;
    }

    .title-text{
        color:#32a49a; 
        font-size:45px;
        font-weight: 500 !important;
        font-family: Palatino, URW Palladio L, serif !important;
    }

    .subtitle-text{
        font-weight: 300 !important;
        color:#a8a8a8;
        font-family: Roboto,sans-serif !important;
    }

    @media (min-width: 10px) and (max-width: 767px) {
        .title-text{
            font-size: 35px !important;
        }
    }


</style>
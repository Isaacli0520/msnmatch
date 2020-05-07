<template>
    <v-dialog :value="value" @input="$emit('input')" v-if='user' min-width="330px" max-width="550px">
        <v-card>
            <v-img :src="user.picture"></v-img>
            <div style="padding-top: 10px; padding-bottom:0px;">
                <div class="title-div">
                    <span class="cus-title" style="float:left;">{{user.first_name + " " + user.last_name}}</span>
                    <span v-if="user.follow" class="role-title" style="float:right;">Favorite</span>
                </div>
            </div>
            <v-card-text>
                <div class="skill-tags">
                    <template v-for="(skills_of_type, skills_type_name) in user.skills">
                        <tag-span v-for="skill in skills_of_type"
                            :key="skills_type_name + skill.id"
                            :skill="skill"
                            :clickable="'href'"
                        />
                    </template>
                </div>
                <div>
                    <table class="table table-user-information">
                        <tbody>
                            <tr>
                                <td class="field-title">Email</td>
                                <td>{{user.email}}</td>
                            </tr>
                            <tr>
                                <td class="field-title">Year</td>
                                <td>{{user.year}}</td>
                            </tr>
                            <tr v-if="user.major">
                                <td class="field-title">Major</td>
                                <td>{{user.major}}</td>
                            </tr>
                            <tr v-if="user.major_two">
                                <td class="field-title">Second Major</td>
                                <td>{{user.major_two}}</td>
                            </tr>
                            <tr v-if="user.minor">
                                <td class="field-title">Minor</td>
                                <td>{{user.minor}}</td>
                            </tr>
                            <tr v-if="user.role">
                                <td class="field-title">Role</td>
                                <td>{{user.role}}</td>
                            </tr>
                            <tr v-if="user.wechat">
                                <td class="field-title">WeChat ID</td>
                                <td>{{user.wechat}}</td>
                            </tr>
                            <!-- <tr v-if="user.birth_date">
                                <td class="field-title">Birth Date</td>
                                <td>{{user.birth_date}}</td>
                            </tr> -->
                            <tr v-if="user.sex">
                                <td class="field-title">Gender</td>
                                <td>{{user.sex}}</td>
                            </tr>
                            <tr v-if="user.location">
                                <td class="field-title">Location</td>
                                <td>{{user.location}}</td>
                            </tr>
                            <tr v-if="user.bio">
                                <td style="vertical-align:top;" class="field-title">Bio</td>
                                <td>{{user.bio}}</td>
                            </tr>
                            <tr v-if="rm">
                                <td style="vertical-align:top;" class="field-title">Roommate Bio</td>
                                <td>{{user.rm_bio}}</td>
                            </tr>
                            <tr v-if="rm">
                                <td style="vertical-align:top;" class="field-title">Schedule</td>
                                <td>{{user.rm_schedule}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="video-div" v-if="user.video.length">
                    <video width="100%" controls :src="user.video">
                        Your Browser does not support video tags lol
                    </video>
                </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="purple darken-1" outlined :loading="addFavBtnLoading" v-if="add_to_fav && !user.follow" @click="addFav(user)">Add to Favorite</v-btn>
                <v-btn color="purple darken-1" outlined :loading="delFavBtnLoading" v-if="add_to_fav && user.follow" @click="delFav(user)">Remove from Favorite</v-btn>
                <v-btn color="purple darken-1" outlined v-if="edit" :href="'/users/'+user.username+'/edit/'">Edit</v-btn>
                <v-btn color="blue darken-1" outlined @click.native="$emit('input')">Close</v-btn>
            </v-card-actions>
        </v-card>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="1800">
            {{success_text}}
            <v-btn color="cyan accent-1" text @click="success_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            {{failure_text}}
            <v-btn color="white" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
    </v-dialog>
</template>



<script>
import TagSpan from '../components/TagSpan'
import axios from 'axios'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default{
    props: {
        user:{
            type:Object,
            default:null,
        },
        value:{
            type:Boolean,
            default:false,
        },
        edit:{
            type:Boolean,
            default:false,
        },
        rm:{
            type:Boolean,
            default:false,
        },
        add_to_fav:{
            type:Boolean,
            default:false,
        }
    },
    data(){
        return{
            success_text:"",
            success_snack:false,
            failure_text:"",
            failure_snack:false,
            addFavBtnLoading:false,
            delFavBtnLoading:false,
        }
    },
    components:{
        TagSpan,
    },
    watch:{
    },
    computed:{
        
    },
    methods:{
        addFav(user){
            this.addFavBtnLoading = true;
            axios.post('/skills/api/add_fav/',{"user_pk":user.pk}).then(response => {
                this.addFavBtnLoading = false;
                if(response.data.success){
                    this.$emit('add-to-fav', user);
                    this.success_text = "Added to Favorite";
                    this.success_snack = true;
                }
                else{
                    this.failure_text = "做人不能太贪心(*￣︶￣)~";
                    this.failure_snack = true;
                }
            });
        },
        delFav(user){
            this.delFavBtnLoading = true;
            axios.post('/skills/api/del_fav/',{"user_pk":user.pk}).then(response => {
                this.delFavBtnLoading = false;
                if(response.data.success){
                    this.$emit('del-from-fav', user);
                    this.success_text = "Deleted from Favorite";
                    this.success_snack = true;
                }
                else{
                    this.failure_text = "Sth is wronggggggg!!";
                    this.failure_snack = true;
                }
            });
        },
    },
    mounted(){
    },
}
</script>


<style lang="css">
    .title-div{
        display:block; 
        height:28px; 
        line-height:28px;
        clear:both;
        padding: 0px 16px 0px 16px;
    }

    .cus-title{
        font-family: "Roboto", sans-serif !important;
        font-weight: 700 !important;
        align-items: center;
        font-size: 18px;
        letter-spacing: 0.0125em;
    }

    .role-title{
        font-family: "Roboto", sans-serif !important;
        font-weight: 700 !important;
        align-items: center;
        font-size: 13px;
        letter-spacing: 0.0125em;
        padding: 0px 6px 0px 6px;
        color: white;
        background-color: rgb(255, 38, 38);
        border-radius: 5px;
    }

    .skill-tags{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 0px 0px 10px 0px;
        }

    .table-user-information{
        width: 100%;
        table-layout: fixed;
        border-collapse: collapse;
    }

    .field-title{
        font-weight: 670;
        width:30%;
    }

    tr td:first-child{
        color: rgb(134, 132, 132);
    }

    tr td:last-child{
        color: rgb(0, 0, 0);
        font-weight:300 !important;
    }

    table tr:last-child td{
        border: none !important;
        padding-bottom: 0px !important;
    }

    .v-card__text td{
        border-bottom: 1px solid rgb(216, 216, 216) !important;
        word-break: break-all;
        white-space: pre-line;
        font-family: "Roboto", sans-serif !important;
        font-size: 15px !important;
        padding: 11px 12px;
    }

    .video-div{
        margin-top: 12px;
    }
</style>
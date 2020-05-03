<template>
    <v-dialog :value="value" @input="$emit('input')" v-if='user' min-width="330px" max-width="550px">
        <v-card>
            <v-img :src="user.picture"></v-img>
            <v-card-title>{{ user.first_name + " " + user.last_name}}</v-card-title>
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
                <v-btn color="purple darken-1" outlined v-if="edit" :href="'/users/'+user.username+'/edit/'">Edit</v-btn>
                <v-btn color="blue darken-1" outlined @click.native="$emit('input')">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>



<script>
import TagSpan from '../components/TagSpan'

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
        }
    },
    data(){
        return{
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
    },
    mounted(){
    },
}
</script>


<style lang="css">
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
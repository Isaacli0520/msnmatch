<template>
    <div>
        <v-navigation-drawer
            light
            floating
            temporary
            app
            v-model="drawer">
            <!-- :clipped="$vuetify.breakpoint.mdAndUp" -->
            <v-container v-if="!loaded || user == null || follow_users == null" fluid fill-height>
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
            <v-container v-if="loaded && user && follow_users">
                <v-card 
                    color="#FFFFFF">
                    <!-- <v-list-item>
                        <v-list-item-avatar color="grey">
                            <v-img :src="user.picture"></v-img>
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title class="headline">{{user.first_name + " " + user.last_name}}</v-list-item-title>
                            <v-list-item-subtitle>Role: {{ user.role ? user.role : "None" }}</v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item> -->
                    <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title>
                    <v-card-subtitle>Role: {{ user.role ? user.role : "None" }}</v-card-subtitle>
                </v-card>
                <v-card
                    style="margin-top:15px;">
                    <v-card-title style="padding-bottom:0px !important;">Favorite Users</v-card-title>
                    <v-list dense>
                        <v-list-item
                            v-for="(follow_user, idx) in follow_users" 
                            :key="idx">
                            <v-list-item-avatar color="grey">
                                <v-img :src="follow_user.picture"></v-img>
                            </v-list-item-avatar>
                            <v-list-item-content>
                                <v-list-item-title>{{follow_user.first_name + " " + follow_user.last_name}}</v-list-item-title>
                            </v-list-item-content>
                            <v-list-item-action>
                                <v-btn icon small>
                                    <v-icon small color="black lighten-1" @click="delFav(follow_user)">mdi-delete-outline</v-icon>
                                </v-btn>
                            </v-list-item-action>
                        </v-list-item>
                    </v-list>
                </v-card>
                <v-card
                    v-for="(items, i) in side_bar_items"
                    :key="i"
                    style="margin-top:15px;"
                    color="#FFFFFF">
                    <v-list dense>
                        <v-list-item
                            :key="index_item + '-trash' " 
                            v-for="(item, index_item) in items"
                            @click="navMethod(item)"
                            :target="item.target">
                            <v-list-item-avatar
                                v-if="item.icon">
                                <v-icon>{{ item.icon }}</v-icon>
                            </v-list-item-avatar>
                            <v-list-item-content>
                                <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-container>
        </v-navigation-drawer>
        <v-app-bar
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            dense
            light
            elevation="1"
            >
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <!-- <v-btn
                @click.stop="drawer = !drawer"
                text
                small>
                <v-icon small>
                    fas fa-bars
                </v-icon>
            </v-btn> -->
            <img style="margin-left:6px;" :src="brand_pic" width="40" height="38" alt="">
            <template v-if="$vuetify.breakpoint.mdAndUp">
                <v-btn 
                    :href="general_urls.match_url"
                    text>Match</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="general_urls.skills_url"
                    text>Tags</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="general_urls.roommate_url"
                    text>Roommate</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="general_urls.courses_url"
                    text>HoosMyProfessor</v-btn>
                <!-- <v-divider inset vertical></v-divider> -->
                <!-- <v-btn 
                    :href="general_urls.market_url"
                    text>Market</v-btn> -->
            </template>
            <v-spacer></v-spacer>
            <v-btn
                icon
                color="black"
                @click="reportBugDialog=true">
                <v-icon>mdi-help-circle-outline</v-icon>
            </v-btn>
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
                        color="black"
                        v-on="on">
                        <v-icon>mdi-apps</v-icon>
                    </v-btn>
                </template>
                <v-list dense rounded>
                    <v-list-item
                        v-for="(item, index) in app_items"
                        :key="index + '-app'"
                        @click="navMethod(item)">
                        <v-list-item-icon>
                            <v-icon color="black" dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        class="mr-1"
                        icon
                        color="black"
                        v-on="on">
                        <v-icon>mdi-account-circle-outline</v-icon>
                    </v-btn>
                </template>
                <v-list dense rounded>
                    <v-list-item
                        v-for="(item, index) in user_items"
                        :key="index"
                        @click="navMethod(item)">
                        <v-list-item-icon>
                            <v-icon color="black" dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>
        <v-dialog v-model="reportBugDialog" max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline">Report Bugs</span>
                </v-card-title>
                <v-card-text style="margin-top:10px;">
                    <v-form
                        ref="report_form"
                        v-model="report_form_valid">
                        <v-text-field
                            outlined
                            v-model="report_title"
                            dense
                            :rules="reportTitleRules"
                            label="Title"
                            ></v-text-field>

                        <v-textarea
                            v-model="report_text"
                            label="Describe the Bug"
                            auto-grow
                            dense
                            outlined
                            :rules="reportTextRules"
                            rows="4"
                            row-height="20">
                        </v-textarea>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="teal darken-1" outlined :loading="reportBugBtnLoading" @click="submitReport()">Submit</v-btn>
                    <v-btn color="red lighten-1" outlined @click="reportBugDialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="1800">
            {{success_text}}
            <template v-slot:action="{ attrs }">
            <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            {{failure_text}}
            <template v-slot:action="{ attrs }">
            <v-btn color="white" v-bind="attrs" text @click="failure_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
    </div>
</template>

<script>
import axios from 'axios'
import { general_urls, general_icons, brand_pic } from "../utils"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default{
    props: {
        headerUpdate:{
            type:Boolean,
            default:false,
        },
    },
    data: function () {
        return {
            // general
            brand_pic:brand_pic,
            general_urls:general_urls,

            reportBugDialog:false,
            reportBugBtnLoading:false,
            success_snack:false,
            success_text:"",
            failure_text:"",
            failure_snack:false,
            navDrawer:false,
            drawer: false,
            loaded:false,
            user: null,
            follow_users:null,
            report_title:"",
            report_text:"",
            report_form_valid:true,
            reportTextRules:[
                v => !!v || 'Description is required',
                v => (v && v.length <= 1000) || 'Description must be less than 1000 characters',
            ],
            reportTitleRules: [
                v => !!v || 'Title is required',
                v => (v && v.length <= 55) || 'Title must be less than 55 characters',
            ],
            user_items:[
                { title:"Profile", icon:general_icons.profile },
                { title:"Edit Profile", icon:general_icons.edit_profile},
                { title:"Log Out", icon:general_icons.logout},
            ],
            app_items:[
                { title:"Market", icon:general_icons.market },
                { title:"HoosMyProfessor", icon:general_icons.courses},
                { title:"Live Comments", icon:general_icons.live_comments },
            ],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                market_url:"",
                rm_url:"",
                courses_url:"",
                match_url:"",
                comment_url:"",
                skills_url:"",
            },
            side_bar_items:[
                [{
                    "title":"Add Tags",
                    "icon":general_icons.add_tags,
                },
                {
                    "title":"Edit Profile",
                    "icon":general_icons.edit_profile,
                }],
                [{
                    "title":"Match",
                    "icon":general_icons.match,
                },
                {
                    "title":"Market",
                    "icon":general_icons.market,
                },
                {
                    "title":"HoosMyProfessor",
                    "icon":general_icons.courses,
                }]
            ],
            old_items: [
                { icon: 'fas fa-book', text: 'HoosMyProfessor' },
                { icon: 'fas fa-user', text: 'Match' },
            ],
        }
    },
    components:{
    },
    watch:{
        headerUpdate(){
            this.get_match_header();
            this.get_follow_users();
        }
    },
    computed:{
    },
    methods:{
        navAsideMethod(item){
            if(item.text == "HoosMyProfessor"){
                this.goToHref(this.general_urls.courses_url);
            }
            else if(item.text == "Match"){
                this.goToHref(this.general_urls.match_url);
            }
        },
        navMethod(item){
            if(item.title=="Profile"){
                this.goToHref(this.urls.profile)
            }
            else if(item.title=="Edit Profile"){
                this.goToHref(this.urls.update_profile)
            }
            else if(item.title=="Log Out"){
                this.goToHref(this.general_urls.logout)
            }
            else if(item.title=="Match"){
                this.goToHref(this.general_urls.match_url)
            }
            else if(item.title=="Add Tags"){
                this.goToHref('/skills/')
            }
            else if(item.title=="Market"){
                this.goToHref(this.general_urls.market_url)
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.general_urls.comment_url)
            }
            else if(item.title == "HoosMyProfessor"){
                this.goToHref(this.general_urls.courses_url);
            }
        },
        get_basic_info(){
            axios.get('/courses/api/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
                this.loaded = true;
            });
        },
        get_follow_users(){
            axios.get('/users/api/get_follow_list/',{params: {}}).then(response => {
                this.follow_users = response.data.following;
            });
        },
        get_match_header(){
            axios.get('/users/api/get_user_match_header/',{params: {}}).then(response => {
                this.user = response.data.user;
            });
        },
        goToHref(text){
            window.location.href = text;
        },
        delFav(user){
            axios.post('/users/api/del_fav/',{"user_pk":user.pk}).then(response => {
                if(response.data.success){
                    this.$emit('del-from-fav', user);
                    this.get_follow_users();
                    this.success_text = "Deleted from Favorite";
                    this.success_snack = true;
                }
                else{
                    this.failure_text = "Sth is wronggggggg!!";
                    this.failure_snack = true;
                }
            });
        },
        submitReport(){
            this.$refs.report_form.validate();
            if(!this.report_form_valid){
                return;
            }
            this.reportBugBtnLoading = true;
            axios.post('/courses/api/report_bug/',{"title":this.report_title, "text":this.report_text}).then(response => {
                this.reportBugBtnLoading = false;
                if(response.data.success){
                    this.success_text = "Thank you!";
                    this.success_snack = true;
                    this.reportBugDialog = false;
                    this.report_title = "";
                    this.report_text = "";
                    this.$refs.report_form.resetValidation();
                }
                else{
                    this.failure_text = "Sth is wronggggggg!!";
                    this.failure_snack = true;
                }
            });
        }
    },
    mounted(){
        this.get_basic_info();
        this.get_match_header();
        this.get_follow_users();
    },
}
</script>


<style scoped lang="css">
    .theme--light.v-app-bar.v-toolbar.v-sheet{
        background-color: white !important;
    }

    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>
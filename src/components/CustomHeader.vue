<template>
    <div>
        <!-- Side Navigation Drawer -->
        <v-navigation-drawer
            color="#fcfcfc"
            app
            hide-overlay
            v-model="drawer"
            :clipped="$vuetify.breakpoint.mdAndUp">
            <v-container>
            <v-card 
                color="#FFFFFF"
                v-if="user">
                <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title>
                <v-card-subtitle>Reviews: {{user.num_reviews}}</v-card-subtitle>
                </v-card>
            <v-card
                style="margin-top:15px;"
                color="#FFFFFF">
            <v-list
                dense>
                <v-list-item
                    :key="index_item + '-trash' " 
                    v-for="(item, index_item) in nav_drawer_items"
                    :href="item.href"
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
        <!-- APP BAR -->
        <v-app-bar
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            light
            height="62"
            elevation="1">
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-img max-height="46" max-width="46" :src="urls.brand_pic" alt=""></v-img>
            <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
                <v-btn 
                    :href="urls.courses_url"
                    text>HoosMyProfessor</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.match_url"
                    text>Match</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.market_url"
                    text>Market</v-btn>
            </v-toolbar-items>
            <search-course
                v-if="searchBool"></search-course>
            <v-spacer v-if="!searchBool"></v-spacer>
            <!-- App Menu -->
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
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
                            <v-icon dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
            <!-- User Drop Menu -->
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
                        v-on="on">
                        <v-icon>fas fa-user-circle</v-icon>
                    </v-btn>
                </template>
                <v-list dense rounded>
                    <v-list-item
                        v-for="(item, index) in user_items"
                        :key="index"
                        @click="navMethod(item)">
                        <v-list-item-icon>
                            <v-icon dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>
    </div>
</template>

<script>
import axios from 'axios'
import SearchCourse from './SearchCourse'

export default{
    props: {
        searchBool:{
            type:Boolean,
            default:true,
        },
        headerUpdate:{
            type:Boolean,
            default:false,
        },
    },
    data: function () {
        return {
            navDrawer:false,
            user:null,
            drawer: null,
            credential:"",
            plannableURL:"",
            username:"",
            taking_courses:[],
            courseTypes:[
                'Clinical',
                'Discussion',
                'Drill',
                'Independent Study',
                'Laboratory',
                'Lecture',
                'Practicum',
                'Seminar',
                'Studio',
                'Workshop',
                '',
            ],
            user_items:[
                { title:"Profile", icon:"fas fa-user" },
                { title:"Edit Profile", icon:"fas fa-user-edit" },
                { title:"My Courses", icon:"fas fa-list-ol" },
                { title:"Log Out", icon:"fas fa-sign-out-alt"},
            ],
            app_items:[
                { title:"Match", icon:"fas fa-user-friends" },
                { title:"Market", icon:"fas fa-search-dollar" },
                { title:"Live Comments", icon:"fas fa-comment" },
            ],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                courses_url:"",
                match_url:"",
                comment_url:"",
                market_url:"",
                skills_url:"",
            },
            nav_drawer_items:[
                {
                    "title":"Home",
                    "icon":"fas fa-home",
                    "href":"/courses/",
                    "target":"",
                },
                {
                    "title":"Departments",
                    "icon":"fas fa-list-ol",
                    "href":"/courses/departments/",
                    "target":"",
                },
                {
                    "title":"My Courses",
                    "icon":"fas fa-user-circle",
                    "href":"",
                    "target":"",
                },
                {
                    "title":"My Reviews",
                    "icon":"fas fa-book",
                    "href":"/courses/reviews/",
                    "target":"",
                },
                {
                    "title":"Plannable",
                    "icon":"fas fa-paper-plane",
                    "href":"https://plannable.org",
                    "target":"_blank",
                },
            ],
        }
    },
    components:{
        SearchCourse,
    },
    watch:{
        headerUpdate(){
            this.getTakingCourses();
        },
        credential(){
            this.getPlannableURL();
        },
        username(){
            this.getPlannableURL();
            this.nav_drawer_items[2].href = "/users/" + this.username + "/courses/";
        },
        taking_courses(val){
            var tmp_arr = [];
            for(let i = 0; i < val.length; i++){
                tmp_arr.push(val[i].mnemonic.toLowerCase() + val[i].number+this.courseTypes.indexOf(val[i].type).toString(10))
            }
            this.plannableURL = JSON.stringify(tmp_arr);
            this.getPlannableURL();
        },
    },
    computed:{

    },
    methods:{
        sortCourseNumber(a, b){
            return a.number.toString(10) - b.number.toString(10);
        },
        navAsideMethod(item){
            if(item.text == "HoosMyProfessor"){
                this.goToHref(this.urls.courses_url);
            }
            else if(item.text == "Match"){
                this.goToHref(this.urls.match_url);
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
                this.goToHref(this.urls.logout)
            }
            else if(item.title=="My Courses"){
                this.goToHref(this.urls.my_courses)
            }
            else if(item.title=="Match"){
                this.goToHref(this.urls.match_url)
            }
            else if(item.title=="Market"){
                this.goToHref(this.urls.market_url)
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.urls.comment_url)
            }
        },
        get_basic_info(){
            axios.get('/courses/ajax/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
            });
        },
        goToHref(text){
            window.location.href = text;
        },
        getCredential(){
            axios.get('/courses/ajax/get_credential/',{params: {}}).then(response => {
                this.credential = response.data.credential;
                this.username = response.data.username;
            }).catch( err => {
                this.credential = "";
                this.username = "";
            });
        },
        getTakingCourses(){
            axios.get('/courses/api/get_user_hmp_header/',{params: {}}).then(response => {
                this.user = response.data.user;
                this.taking_courses = response.data.taking_courses;
            });
        },
        getPlannableURL(){
            // var preHref = "localhost:8080"
            var preHref = "https://plannable.org"
            this.nav_drawer_items[4].href = preHref + "/?courses=" + this.plannableURL + "&username=" + this.username + "&credential=" + this.credential + "";
        },
    },
    mounted(){
        this.getCredential();
        this.get_basic_info();
        this.getTakingCourses();
    },
}
</script>


<style scoped lang="css">
    .cus-navbar-item{
        font-size: 15px !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .theme--light.v-app-bar.v-toolbar.v-sheet{
        background-color: white !important;
    }

    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>
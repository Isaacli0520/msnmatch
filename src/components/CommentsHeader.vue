<template>
    <div>
        <v-app-bar
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            light
            height="62"
            
            elevation="1"
            >
            <!-- <a class="navbar-brand" :href="urls.courses_url">
                <img :src="urls.brand_pic" style="margin:5px 0px 0px 0px;" width="35" height="35" class="d-inline-block align-center" alt="">
            </a> -->
            <!-- <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
                <template v-for="item in navBarItems">
                    <v-btn 
                        :key="item.text + '-btn' "
                        :href="item.href"
                        text>
                        {{item.text}}
                    </v-btn>
                    <v-divider
                        :key="item.text + '-divider' "
                        inset
                        vertical></v-divider>
                </template>
            </v-toolbar-items> -->
            <v-img max-height="46" max-width="46" :src="urls.brand_pic" alt=""></v-img>
            <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
                <v-btn
                    text>Comments</v-btn>
            </v-toolbar-items>
            <v-spacer></v-spacer>
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
    data(){
        return {
            navDrawer:false,
            drawer: null,
            credential:"",
            plannableURL:"",
            username:"",
            taking_courses:[],
            navBarItems:[
                {
                    text:"HoosMyProfessor",
                    href:"",
                    diabled:true,
                },
                {
                    text:"Match",
                    href:"",
                    diabled:true,
                },
            ],
            user_items:[
                { title:"Profile", icon:"fas fa-user" },
                { title:"Edit Profile", icon:"fas fa-biohazard" },
                { title:"My Courses", icon:"fas fa-list-ol" },
                { title:"Log Out", icon:"fas fa-angry"},
            ],
            app_items:[
                { title:"Match", icon:"fas fa-user-friends" },
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
            },
            old_items: [
                { icon: 'fas fa-book', text: 'HoosMyProfessor' },
                { icon: 'fas fa-user', text: 'Match' },
                ],
        }
    },
    components:{
    },
    watch:{
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
            if(item.title=="Match"){
                this.goToHref(this.urls.match_url)
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.urls.comment_url)
            }
        },
        get_basic_info(){
            axios.get('/courses/ajax/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
                this.navBarItems[0] = {
                    text:"HoosMyProfessor",
                    href:this.urls.courses_url,
                    diabled:false,
                };
                this.navBarItems[1] = {
                    text:"Match",
                    href:this.urls.match_url,
                    diabled:false,
                };
            });
        },
        goToHref(text){
            window.location.href = text;
        },
    },
    mounted(){
        this.get_basic_info();
    },
}
</script>


<style lang="css">

    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>
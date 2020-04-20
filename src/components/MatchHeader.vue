<template>
    <div>
        <v-navigation-drawer
            light
            color="white"
            app
            hide-overlay
            v-model="drawer"
            :clipped="$vuetify.breakpoint.mdAndUp"
            >
            <v-list dense>
                <v-list-item
                    :key="index_item + '-trash' " 
                    v-for="(item, index_item) in main_items"
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
        </v-navigation-drawer>
        <v-app-bar
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            light
            height="62"
            
            elevation="1"
            >
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-img max-height="46" max-width="46" :src="urls.brand_pic" alt=""></v-img>
            <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
                <v-btn 
                    :href="urls.match_url"
                    text>Match</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.skills_url"
                    text>Interests</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.courses_url"
                    text>HoosMyProfessor</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.market_url"
                    text>Market</v-btn>
                
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
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default{
    props: {
    },
    data: function () {
        return {
            navDrawer:false,
            drawer: false,
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
                { title:"Edit Profile", icon:"fas fa-user-edit" },
                { title:"Log Out", icon:"fas fa-sign-out-alt"},
            ],
            app_items:[
                { title:"Market", icon:"fas fa-search-dollar" },
                { title:"HoosMyProfessor", icon:"fas fa-graduation-cap" },
                { title:"Live Comments", icon:"fas fa-comment" },
            ],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                market_url:"",
                courses_url:"",
                match_url:"",
                comment_url:"",
                skills_url:"",
            },
            main_items:[
                {
                    "title":"Home",
                    "icon":"fas fa-home",
                    "href":"/match/",
                    "target":"",
                },

                {
                    "title":"Add Your Interests",
                    "icon":"fas fa-heart",
                    "href":"/skills/",
                    "target":"",
                },
                {
                    "title":"Market",
                    "icon":"fas fa-search-dollar",
                    "href":"/market/",
                    "target":"",
                },
                {
                    "title":"HoosMyProfessor",
                    "icon":"fas fa-graduation-cap",
                    "href":"/courses/",
                    "target":"",
                }],
            
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
            else if(item.title=="Match"){
                this.goToHref(this.urls.match_url)
            }
            else if(item.title=="Market"){
                this.goToHref(this.urls.market_url)
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.urls.comment_url)
            }
            else if(item.title == "HoosMyProfessor"){
                this.goToHref(this.urls.courses_url);
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
    .theme--light.v-app-bar.v-toolbar.v-sheet{
        background-color: white !important;
    }
    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>
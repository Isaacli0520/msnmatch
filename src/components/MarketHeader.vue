<template>
    <div>
        <v-navigation-drawer
            light
            app
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
            <v-divider></v-divider>
            <v-list dense>
                <v-list-item
                    :key="index_item + '-trash' " 
                    v-for="(item, index_item) in category_items"
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
                    :href="urls.courses_url"
                    text>Market</v-btn>
            </v-toolbar-items>
            <search-course
                v-if="searchBool"></search-course>
            <v-spacer v-if="!searchBool"></v-spacer>
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
import SearchCourse from './SearchCourse'

export default{
    props: {
        searchBool:{
            type:Boolean,
            default:false,
        },
        headerUpdate:{
            type:Boolean,
            default:false,
        },
    },
    data: function () {
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
                { title:"Log Out", icon:"fas fa-angry"},
            ],
            app_items:[
                { title:"Match", icon:"fas fa-user-friends" },
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
                courses_url:"",
                match_url:"",
                comment_url:"",
            },
            main_items:[
                {
                    "title":"Home",
                    "icon":"fas fa-home",
                    "href":"/market/",
                    "target":"",
                },
                {
                    "title":"My Items",
                    "icon":"fas fa-list-ul",
                    "href":"/market/items/",
                    "target":"",
                }],
            category_items:[
                {
                    "title":"Electronics",
                    "icon":"fas fa-bolt",
                    "href":"/market/electronics/",
                    "target":"",
                },
                {
                    "title":"Textbooks",
                    "icon":"fas fa-book",
                    "href":"/market/textbooks/",
                    "target":"",
                },
                {
                    "title":"School Supplies",
                    "icon":"fas fa-school",
                    "href":"/market/schoolsupplies/",
                    "target":"",
                },
                {
                    "title":"Pets",
                    "icon":"fas fa-cat",
                    "href":"/market/pets/",
                    "target":"",
                },
                {
                    "title":"Clothing",
                    "icon":"fas fa-tshirt",
                    "href":"/market/clothing/",
                    "target":"",
                },
                {
                    "title":"Housing",
                    "icon":"fas fa-bed",
                    "href":"/market/housing/",
                    "target":"",
                },
                {
                    "title":"Miscellaneous",
                    "icon":"fas fa-question",
                    "href":"/market/miscellaneous/",
                    "target":"",
                },
            ],
            old_items: [
                { icon: 'fas fa-book', text: 'HoosMyProfessor' },
                { icon: 'fas fa-user', text: 'Match' },
                ],
        }
    },
    components:{
        SearchCourse,
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

    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>
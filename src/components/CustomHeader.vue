<template>
    <div>
        <v-navigation-drawer
            v-if="navDrawer"
            fixed
            :clipped="$vuetify.breakpoint.mdAndUp"
            app
            v-model="drawer">
            <v-list dense>
                <template v-for="item in old_items">
                    <v-layout
                        row
                        v-if="item.heading"
                        align-center
                        :key="item.heading">
                        <v-flex xs6>
                            <v-subheader v-if="item.heading">
                                {{ item.heading }}
                            </v-subheader>
                        </v-flex>
                        <v-flex xs6 class="text-xs-center">
                            <a href="#!" class="body-2 black--text">EDIT</a>
                        </v-flex>
                    </v-layout>
                    <v-list-group
                        v-else-if="item.children"
                        v-model="item.model"
                        :key="item.text"
                        :prepend-icon="item.model ? item.icon : item['icon-alt']"
                        append-icon="">
                        <v-list-item slot="activator">
                            <v-list-item-content>
                                <v-list-item-title>
                                    {{ item.text }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                        <v-list-item
                            v-for="(child, i) in item.children"
                            :key="i">
                            <v-list-item-action v-if="child.icon">
                                <v-icon>{{ child.icon }}</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>
                                {{ child.text }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-group>
                    <v-list-item v-else @click="navAsideMethod(item)" :key="item.text">
                            <v-list-item-action>
                                <v-icon>{{ item.icon }}</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>
                                    {{ item.text }}
                                </v-list-item-title>
                            </v-list-item-content>
                    </v-list-item>
                </template>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar
            color="white"
            app
            light
            absolute
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            fixed>
            <v-app-bar-nav-icon v-if="navDrawer" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <a class="navbar-brand" :href="urls.courses_url">
                <img :src="urls.brand_pic" style="margin:5px 0px 0px 0px;" width="35" height="35" class="d-inline-block align-center" alt="">
            </a>
            <v-toolbar-title class="nav-bar-title ml-0 mr-2 pl-3">
                HoosMyProfessor
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <search-course
                v-if="searchBool"></search-course>
            <v-spacer></v-spacer>
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
    },
    data: function () {
        return {
            navDrawer:false,
            drawer: false,
            user_items:[
                { title:"Profile", icon:"fas fa-user" },
                { title:"Edit Profile", icon:"fas fa-biohazard" },
                { title:"My Courses", icon:"fas fa-list-ol" },
                { title:"Log Out", icon:"fas fa-angry"},
            ],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                courses_url:"",
            },
            old_items: [
                //   {  icon: 'contacts', text: 'Contacts' },
                //   { icon: 'history', text: 'Frequently contacted' },
                //   { icon: 'content_copy', text: 'Duplicates' },
                //   {
                //     icon: 'keyboard_arrow_up',
                //     'icon-alt': 'keyboard_arrow_down',
                //     text: 'Labels',
                //     model: true,
                //     children: [
                //       { icon: 'add', text: 'Create label' }
                //     ]
                //   },
                //   {
                //     icon: 'keyboard_arrow_up',
                //     'icon-alt': 'keyboard_arrow_down',
                //     text: 'More',
                //     model: false,
                //     children: [
                //       { text: 'Import' },
                //       { text: 'Export' },
                //       { text: 'Print' },
                //       { text: 'Undo changes' },
                //       { text: 'Other contacts' }
                //     ]
                //   },
                { icon: 'settings', text: 'Settings' },
                { icon: 'chat_bubble', text: 'Send feedback' },
                { icon: 'help', text: 'Help' },
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
        sortCourseNumber(a, b){
            return a.number.toString(10) - b.number.toString(10);
        },
        navAsideMethod(item){
            
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
        },
        get_basic_info(){
            axios.get('/courses/ajax/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
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

    
    .nav-bar-title{
        font-family: "Raleway", Helvetica, sans-serif;
        font-weight: 300;
        letter-spacing: 0.07em;
    }

</style>
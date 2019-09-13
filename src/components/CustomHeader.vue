<template>
    <div>
        <v-navigation-drawer
            fixed
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
            color="blue-grey darken-1"
            app
            dark
            height="56"
            absolute
            elevation="0"
            fixed>
            <v-app-bar-nav-icon v-if="$vuetify.breakpoint.smAndDown" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <a class="navbar-brand" :href="urls.courses_url">
                <img :src="urls.brand_pic" style="margin:5px 0px 0px 0px;" width="35" height="35" class="d-inline-block align-center" alt="">
            </a>
            <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
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
            </v-toolbar-items>
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
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                courses_url:"",
                match_url:"",
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
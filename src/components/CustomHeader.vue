<template>
    <div>
        <v-navigation-drawer
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
      color="teal darken-2"
      dark
      app
      :clipped-left="$vuetify.breakpoint.mdAndUp"
      fixed>
    <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        Hoosmyprofessor
      </v-toolbar-title>

      <v-autocomplete
      v-model="selected_item"
      :items="search_result_items"
      :loading="isLoading"
      :search-input.sync="search"
      color="teal"
      clearable
      solo-inverted
      no-filter
      flat
      hide-no-data
      hide-selected
      hide-details
      placeholder="Search for Courses/Instructors"
      return-object
    >
      <template v-slot:item="{ item }">
        <v-list-item-content>
            <v-list-item-title mb-2>{{item.text}}</v-list-item-title>
            <v-list-item-subtitle v-if="item.type=='course'">Last taught:{{item.last_taught}}</v-list-item-subtitle>
        </v-list-item-content>  
      </template>
    </v-autocomplete>
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
// import Vue from 'vue'
// import Vuetify from 'vuetify/lib'
// Vue.use(Vuetify);

export default{
    data: function () {
        return {
            courseNameLimit: 42,
            drawer: false,
            selected_item:null,
            isLoading: false,
            lastTime: 0,
            entries:[],
            search: null,
            searchquery: '',
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
    },
    watch:{
        selected_item(val){
            if(val != null){
                if(val.type == "course"){
                    this.goToHref("/courses/" + val.value + "/");
                }
                else if(val.type == "instructor"){
                    this.goToHref("/courses/instructors/" + val.value + "/");
                }
            }
        },
        search(val) {
            // Items have already been loaded
            if (val == null || val.length == 0){
            this.entries = []
            return
            }
            if (val.length < 2) return

            // Items have already been requested
            // if (this.isLoading) return

            this.isLoading = true
            this.lastTime += 1;
            // Lazily load input items
            axios.get('/courses/ajax/course_search_result/',{params: {query:val, time: this.lastTime}}).then(response => {
                    if(response.data.time == this.lastTime){
                        this.entries = response.data.course_result; 
                    }
            })
            .catch(err => {
                console.log("error: ",err)
            })
            .finally(() => {this.isLoading = false});
        },
    },
    computed:{
        search_result_items(){
            return this.entries.map(entry => {
                if(entry.type == "course"){
                    let tmp_course_name = entry.mnemonic + entry.number + " " + entry.title;
                    const course_name = tmp_course_name.length > this.courseNameLimit
                        ? tmp_course_name.slice(0, this.courseNameLimit) + '...'
                        : tmp_course_name;

                    return {text:course_name, value:entry.pk, last_taught:entry.last_taught, type:"course"};
                }
                else if(entry.type == "instructor"){
                    return {text:entry.name, value:entry.pk,  last_taught:"", type:"instructor"};
                }
                else{
                    console.log("Search Bar Error");
                    return {}
                }
                })
        },
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


<style scoped lang="css">

</style>
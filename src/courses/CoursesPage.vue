<template>
  <v-app id="inspire">
    <v-navigation-drawer
      fixed
      :clipped="$vuetify.breakpoint.mdAndUp"
      app
      v-model="drawer"
    >
      <v-list dense>
        <template v-for="item in old_items">
          <v-layout
            row
            v-if="item.heading"
            align-center
            :key="item.heading"
          >
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
            append-icon=""
          >
            <v-list-item slot="activator">
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.text }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item
              v-for="(child, i) in item.children"
              :key="i"
              @click=""
            >
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
          <v-list-item v-else @click="" :key="item.text">
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
      color="teal darken-3"
      dark
      app
      :clipped-left="$vuetify.breakpoint.mdAndUp"
      fixed
    >
    <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        Hoosmyprofessor
      </v-toolbar-title>
      
      <!-- <v-text-field
        flat
        solo-inverted
        prepend-inner-icon="search"
        label="Search"
        hide-details
      ></v-text-field> -->
      <v-autocomplete
      v-model="selected_course"
      :items="items"
      :loading="isLoading"
      :search-input.sync="search"
      color="white"
      solo-inverted
      flat
      hide-no-data
      hide-selected
      hide-details
      label="Public APIs"
      placeholder="Start typing to Search"
      prepend-icon="mdi-database-search"
      return-object
    >
      <template v-slot:item="data">
        <v-list-item-content>
          <v-list-item-title v-html="data.item.text"></v-list-item-title>
          <v-list-item-subtitle v-if="data.item.take != 'Null' " v-html="data.item.take"></v-list-item-subtitle>
        </v-list-item-content>  
      </template>
    </v-autocomplete>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>notifications</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'

  export default {
    data() {
      return {
        selected_course:null,
        courseNameLimit:40,
        isLoading: false,
        entries:[],
        search: null,

        dialog: false,
        drawer: null,
        source: "/lessons/",
        old_items: [
          { icon: 'contacts', text: 'Contacts' },
          { icon: 'history', text: 'Frequently contacted' },
          { icon: 'content_copy', text: 'Duplicates' },
          {
            icon: 'keyboard_arrow_up',
            'icon-alt': 'keyboard_arrow_down',
            text: 'Labels',
            model: true,
            children: [
              { icon: 'add', text: 'Create label' }
            ]
          },
          {
            icon: 'keyboard_arrow_up',
            'icon-alt': 'keyboard_arrow_down',
            text: 'More',
            model: false,
            children: [
              { text: 'Import' },
              { text: 'Export' },
              { text: 'Print' },
              { text: 'Undo changes' },
              { text: 'Other contacts' }
            ]
          },
          { icon: 'settings', text: 'Settings' },
          { icon: 'chat_bubble', text: 'Send feedback' },
          { icon: 'help', text: 'Help' },
          { icon: 'phonelink', text: 'App downloads' },
          { icon: 'keyboard', text: 'Go to the old version' }
        ],
      }
    },
    components:{
      CustomHeader,
    },
    watch: {
      selected_course(val){
        if(val != null){
          this.goToHref("/courses/" + val.value + "/");
        }
      },
      search (val) {
        // Items have already been loaded
        if (val == null || val.length == 0){
          this.entries = []
          return
        }
        if (val.length < 2) return

        // Items have already been requested
        if (this.isLoading) return

        this.isLoading = true

        // Lazily load input items
        axios.get('/courses/ajax/course_search_result/',{params: {query:val, }}).then(response => {
                this.entries = response.data.course_result; 
          })
          .catch(err => {
            console.log("error: ",err)
          })
          .finally(() => {this.isLoading = false})
          ;
      },
    },
    computed:{
      items(){
        // if (this.entries.length > 12){
        //   var tmp_entry = this.entries.slice(0, 12);
        // }
        // else{
        //   var tmp_entry = this.entries;
        // }
        return this.entries.map(entry => {
          let tmp_course_name = entry.mnemonic + entry.number + " " + entry.title;
          const course_name = tmp_course_name.length > this.courseNameLimit
            ? tmp_course_name.slice(0, this.courseNameLimit) + '...'
            : tmp_course_name;

          return {text:course_name, value:entry.pk, take:entry.take};
        })
      },
    },
    methods: {
        goToHref(text){
            window.location.href = text;
        },
        getAutoComplete(query){
          axios.get('/courses/ajax/course_search_result/',{params: {query:query, }}).then(response => {
                this.allFmls = response.data.groups; 
          });
        },
    },
    mounted(){
    },
  };
</script>

<style>

  .cus-main{
    width: 100vh;
  }
    

</style>
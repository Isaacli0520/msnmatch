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
          <v-list-item-subtitle v-html="data.item.take"></v-list-item-subtitle>
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
        <v-container fluid grid-list-md pa-2>
            <v-layout mt-2 mb-3>
                <v-flex> 
                    <span class="cus-headline-number">{{course.mnemonic}}{{course.number}}</span>
                    <span class="cus-headline-text">{{course.title}}</span>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout row wrap>
                <v-flex d-flex 
                :key="instructor_name"
                v-for="(semesters, instructor_name) in course.instructors">
                <v-card
                >
                    <v-card-text>
                        <div class="instructor-name mb-2">{{ instructor_name }}</div>
                        <div class="semester-div">
                            <v-chip
                                class="ma-1"
                                color="pink"
                                label
                                text-color="white"
                                :key="index1"
                                v-for="(semester, index1) in semesters"
                            >
                                <v-icon left>label</v-icon>
                                {{semester}}
                            </v-chip>
                            <!-- <template  v-for="(semester, index2) in semesters">
                                <span class="semester-span-year" :key="index2"> {{semester.substring(0,4)}} </span>
                                <span class="semester-span-season" :key="index2 + 100000"> {{semester.substring(4)}} </span>
                            </template> -->
                        </div>
                    </v-card-text>
                    <v-card-actions>
                        <v-btn
                        text
                        color="deep-purple accent-4"
                        >
                        Learn More
                        </v-btn>
                    </v-card-actions>
                </v-card>
                </v-flex>
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
        course:{
            "pk": 0,
            "mnemonic": "",
            "number": "",
            "title": "",
            "take": "",
            "instructors":{},
        },
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
            return this.entries.map(entry => {
            let tmp_course_name = entry.mnemonic + entry.number + " " + entry.title;
            const course_name = tmp_course_name.length > this.courseNameLimit
                ? tmp_course_name.slice(0, this.courseNameLimit) + '...'
                : tmp_course_name;

            return {text:course_name, value:entry.pk, take:entry.take};
            })
        },
        course_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
        course_edit_url: function(){
            return '/courses/' + this.course_pk + '/edit/';
        },
    },
    methods: {
        getCourse(){
            axios.get('/courses/ajax/get_course/',{params: {pk:this.course_pk, }}).then(response => {
                this.course = response.data.course; 
          });
        },
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
        this.getCourse();
    },
  };
</script>

<style>
    .semester-div{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 15px 0px 5px 0px;
    }

    .semester-span-season{
        font-family: "Roboto", sans-serif;
        font-size: 1em;
        font-weight: 500;
        padding: 5px 7px 6px 8px;
        margin: 0px 5px 0px 0px;
        border-radius: 0px 5px 5px 0px;
        color:rgb(255, 255, 255);
        background-color:#FF6600;
    }

    .semester-span-year{
        font-family: "Roboto", sans-serif;
        font-size: 1em;
        font-weight: 500;
        padding: 5px 7px 6px 8px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px 0px 0px 5px;
        color:rgb(0, 0, 0);
        background-color:rgb(253, 217, 116);
    }

    .instructor-name{
        font-family: "Roboto", sans-serif;
        font-size: 2em;
        font-weight: 500;
        margin: 0px 0px 4px 0px;
        color: rgb(0, 0, 0);
    }

    .cus-headline-number{
        font-family: "Roboto", sans-serif;
        font-size: 2.5em;
        font-weight: 500;
        background-color: rgb(11, 105, 92);
        color:#fff;
        padding: 7px 12px 7px 12px;
        border-radius: 5px 0px 0px 5px;
    }

    .cus-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 2.5em;
        font-weight: 300;
        background-color: rgb(226, 225, 225);
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 12px;
        border-radius: 0px 5px 5px 0px;
    }

    .cus-main{
        width: 100vh;
    }

    @media (min-width: 1281px) { 
        
    }

    @media (min-width: 1025px) and (max-width: 1280px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
        
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
        
    }


    @media (min-width: 10px) and (max-width: 767px) {
        .cus-headline-number{
            font-size: 1.3em;
        }

        .cus-headline-text{
            font-size: 1.3em;
            
        }
    }


    /* @media (min-width: 320px) and (max-width: 480px) {

    }

    @media (min-width: 10px) and (max-width: 319px) {
        
    } */
    

</style>
<template>
  <v-app id="inspire">
    <custom-header></custom-header>
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

        lastTime:0,
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
        // if (this.isLoading) return

        this.isLoading = true
        this.lastTime += 1;
        // Lazily load input items
        axios.get('/courses/ajax/course_search_result/',{params: {query:val, time: this.lastTime}}).then(response => {
                console.log("response",response)
                if(response.data.time == this.lastTime){
                    this.entries = response.data.course_result; 
                }
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
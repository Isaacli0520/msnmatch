<template>
    <v-app>
        <v-toolbar clipped-left>
    <v-toolbar-side-icon  @click.stop="drawer = !drawer" class="hidden-md-and-up"></v-toolbar-side-icon>
    <v-toolbar-title>Title</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn flat>Link One</v-btn>
      <v-btn flat>Link Two</v-btn>
      <v-btn flat>Link Three</v-btn>
    </v-toolbar-items>
  </v-toolbar>
  
    <v-navigation-drawer
      v-model="drawer"
      temporary
      absolute
      width = "200"
      id = "drawer"
    >
    </v-navigation-drawer>
        <v-content>
            <v-container
                fluid
                fill-height>
                <v-layout
                align-center
                justify-center>
                    <v-flex
                        xs12
                        sm8
                        md4>
                        <v-card>
                            <v-card-title>Super Cool Main Page</v-card-title>
                            <v-card-text>
                                <v-layout wrap>
                                    <v-flex d-flex>
                                        <v-btn @click="goToHref('/match/')" color="primary">Match</v-btn>
                                    </v-flex>
                                    <v-spacer></v-spacer>
                                    <v-flex d-flex>
                                        <v-btn @click="goToHref('/courses/')" color="primary">Hoosmyprofessor</v-btn>
                                    </v-flex>
                                </v-layout>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                </v-layout>
        </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'

  export default {
    data() {
      return {
          drawer:null,
          isCollapse:true,
          recognition: '',
          activeIndex: '1',
          navOptions:[
              {
                  href:"/match/",
                  label:"Match",
              },
              {
                  href:"",
                  label:"Hoosmyprofessor",
              },
              {
                  href:"www.msnatuva.org",
                  label:"MSN",
              },
          ]
      }
    },
    components:{
    },
    computed:{
    },
    methods: {
        goToHref(href){
            window.location.href = href;
        },
    },
    mounted(){
    },
  };
</script>

<style>
  
</style>
<template>
    <v-app>
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
            console.log("lalala");
            window.location.href = href;
        },
    },
    mounted(){
    },
  };
</script>

<style>
  
</style>
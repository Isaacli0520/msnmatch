<template>
    <v-app>
        <v-main>
            <v-container fluid fill-height>
                <v-layout justify-center align-center>
                    <v-card outlined>
                        <v-card-text>
                            <v-btn class="ma-3 d-flex flex-column justify-center" outlined @click="goToHref('/match/')" color="pink lighten-2">Match</v-btn>
                            <!-- <v-btn class="ma-3 d-flex flex-column justify-center" outlined @click="goToHref('/market/')" color="blue darken-1">Market</v-btn> -->
                            <v-btn class="ma-3 d-flex flex-column justify-center" outlined @click="goToHref('/courses/')" color="teal darken-2">Hoosmyprofessor</v-btn>
                            <!-- <v-btn class="ma-3 d-flex flex-column justify-center" outlined @click="goToHref('/comments/send/')" color="Purple lighten-2">If You Are The One</v-btn> -->
                        </v-card-text>
                    </v-card>
                </v-layout>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>

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

.cus-main{
    margin: 0 auto;
    width: 100%;
    height: 100%;
}
  
</style>
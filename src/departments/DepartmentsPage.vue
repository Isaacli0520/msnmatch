<template>
  <v-app>
    <custom-header></custom-header>
    <v-content>
        <v-container fluid grid-list-lg>
            <v-layout>
                <v-flex>
                    <v-breadcrumbs class="cus-breadcrumbs" :items="navItems" divider=">"></v-breadcrumbs>
                </v-flex>
            </v-layout>
            <v-layout mb-3>
                <v-flex class="cus-headline-flex"> 
                    <div>
                    <span class="cus-headline-text">Departments</span>
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout row wrap>
                <v-flex d-flex xs12 sm12 lg12 md12 xl12 :key="index_school + 'school' " v-for="(departments, school, index_school) in departments_dict">
                    <v-card>
                        <v-card-title>{{ school }}</v-card-title>
                        <v-divider></v-divider>
                        <v-card-text class="text--primary">
                            <v-layout row wrap>
                                <v-flex
                                    pa-1
                                    xs12 sm6 md6 lg6 xl6
                                    :key="index_d + 'department' " 
                                    v-for="(department, index_d) in departments">
                                    <v-list-item
                                        dense
                                        :href="'/courses/departments/'+ department.department_pk + '/' ">
                                        <v-list-item-content>
                                            <v-list-item-title>{{department.name}}</v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-flex>
                            </v-layout>
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>
    <!-- <custom-footer></custom-footer> -->
  </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import CustomFooter from '../components/CustomFooter'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
    data() {
      return {
        departments:[],
        navItems:[],
        departments_dict:{},

        
      }
    },
    components:{
        CustomHeader,
        CustomFooter,
    },
    watch: {
      
    },
    computed:{
    },
    methods: {
        getDepartments(){
            axios.get('/courses/ajax/get_departments/',{params: {}}).then(response => {
                this.departments = response.data.departments;
                var tmp_d = {};
                for(let i = 0; i < this.departments.length; i++){
                    if(this.departments[i].name=="Computer Science"){
                        if(this.departments[i].school=="School of Engineering and Applied Science"){
                            var tmp_cs_department_pk = this.departments[i].department_pk;
                        }
                        else{
                            var tmp_cs_index = i;
                        }
                    }
                }
                this.departments[tmp_cs_index].department_pk = tmp_cs_department_pk;
                for(let i = 0; i < this.departments.length; i++){
                    if(! (this.departments[i].school in tmp_d)){
                        tmp_d[this.departments[i].school] = [];
                    }
                    else{
                        tmp_d[this.departments[i].school].push(this.departments[i])
                    }
                }
                this.departments_dict = tmp_d;
                this.navItems = [
                    {
                        text: "Main",
                        disabled: false,
                        href: '/courses/',
                    },
                    {
                        text: "Departments",
                        disabled: true,
                        href: '',
                    },
                ];
                
          });
        },
        goToHref(text){
            window.location.href = text;
        },
    },
    mounted(){
        this.getDepartments();
    },
  };
</script>

<style>

    .v-breadcrumbs li{
        font-size:20px !important;
    }

    .cus-breadcrumbs{
        padding-left: 4px !important;
    }

    .taking{
        background-color: rgb(11, 105, 92);
        padding: 5px 6px 6px 6px;
        color:#fff;
        border-radius: 5px;
        margin: 0px 0px 0px 6px;
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 500;
    }

    .taken{
        background-color: rgb(40, 123, 247);
        padding: 5px 6px 6px 6px;
        color:#fff;
        border-radius: 5px;
        margin: 0px 0px 0px 6px;
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 500;
    }

    .instructor-topic{
        font-family: "Roboto", sans-serif;
        font-size: 1.7em;
        font-weight: 500;
        margin: 0px 0px 4px 0px;
        color: rgb(255, 255, 255);
        background-color: rgb(11, 105, 92);
        color:#fff;
        padding: 5px 8px 5px 8px;
        border-radius: 5px 5px 5px 5px;
        line-height: 1.6;
        box-decoration-break: clone;
    }

    .instructor-banner{
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 500;
    }

    .semester-div{
        display: flex;
        flex-flow: row wrap;
        width:100%;
        margin: 15px 0px 5px 0px;
    }

    .instructor-name{
        font-family: "Roboto", sans-serif;
        font-size: 2em;
        font-weight: 500;
        color: rgb(0, 0, 0);
    }

    .cus-headline-number{
        font-family: "Roboto", sans-serif;
        font-size: 2.1em;
        font-weight: 500;
        background-color: rgb(11, 105, 92);
        color:#fff;
        padding: 7px 12px 7px 12px;
        border-radius: 5px 0px 0px 5px;
        line-height: 2.0;
        box-decoration-break: clone;
    }

    .cus-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 2.1em;
        font-weight: 300;
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 3px;
        border-radius: 5px;
        line-height: 2.0;
        box-decoration-break: clone;

    }

    .cus-main{
        width: 100vh;
    }

    @media (min-width: 1025px) {
        
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

        .instructor-name{
            font-size:1.7em;
        }

        .instructor-topic{
            font-size:1.4em;
        }

        .v-breadcrumbs li{
        font-size:14px !important;
    }
    }


    /* @media (min-width: 320px) and (max-width: 480px) {

    }

    @media (min-width: 10px) and (max-width: 319px) {
        
    } */
    

</style>
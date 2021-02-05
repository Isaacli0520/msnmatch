<template>
  <v-app>
    <custom-header></custom-header>
    <v-main>
        <v-container v-if="!loaded" fluid fill-height>
            <v-layout 
                align-center
                justify-center>
                <div>
                    <v-progress-circular
                    :size="60"
                    :width="6"
                    indeterminate
                    color="teal lighten-1">
                    </v-progress-circular>
                </div>
            </v-layout>
        </v-container>
        <v-container v-if="loaded" fluid grid-list-lg>
            <v-layout>
                <v-flex>
                    <custom-breadcrumb :items="navItems"></custom-breadcrumb>
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
                    <v-card elevation="3">
                        <v-card-title>{{ school }}</v-card-title>
                        <v-divider></v-divider>
                        <v-card-text class="text--primary">
                            <v-layout row wrap>
                                <v-flex
                                    pa-2
                                    xs12 sm6 md6 lg6 xl6
                                    :key="index_d + 'department' " 
                                    v-for="(department, index_d) in departments">
                                        <v-chip
                                            label
                                            :href="'/courses/departments/'+ department.id + '/' "
                                            outlined 
                                            
                                            :color="variables.secondary_color">{{department.name}}</v-chip>
                                </v-flex>
                            </v-layout>
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import CustomBreadcrumb from '../components/CustomBreadcrumb'
import variables from '../sass/variables.scss'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    data() {
        return {
            variables:variables,
            departments:[],
            navItems:[],
            departments_dict:{},
            loaded:false,
        }
    },
    components:{
        CustomHeader,
        CustomBreadcrumb,
    },
    watch: {
    },
    computed:{
    },
    methods: {
        getDepartments(){
            axios.get('/courses/api/get_departments/',{params: {}}).then(response => {
                this.departments = response.data.departments;
                this.loaded = true;
                var tmp_d = {};
                for(let i = 0; i < this.departments.length; i++){
                    if(this.departments[i].name=="Computer Science"){
                        if(this.departments[i].school=="School of Engineering and Applied Science"){
                            var tmp_cs_department_pk = this.departments[i].id;
                        }
                        else{
                            var tmp_cs_index = i;
                        }
                    }
                }
                this.departments[tmp_cs_index].id = tmp_cs_department_pk;
                for(let i = 0; i < this.departments.length; i++){
                    if(! (this.departments[i].school in tmp_d)){
                        tmp_d[this.departments[i].school] = [];
                    }
                    tmp_d[this.departments[i].school].push(this.departments[i]);
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
        line-height: 1.0;
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
<template>
  <v-app>
    <custom-header></custom-header>
    <v-main>
        <v-container v-if="!loaded" fluid fill-height>
            <v-row justify="center">
                <v-progress-circular
                    :size="60"
                    :width="6"
                    indeterminate
                    color="teal lighten-1"/>
            </v-row>
        </v-container>
        <v-container v-if="loaded" fluid grid-list-lg>
            <v-layout>
                <v-flex>
                    <custom-breadcrumb :items="navItems"></custom-breadcrumb>
                </v-flex>
            </v-layout>
            <v-layout mb-3>
                <v-flex> 
                    <div>
                    <span v-if="department.name.length > 0" class="cus-headline-text">{{department.name}}</span>
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout row wrap>
                <template v-for="(course, index) in courses">
                    <v-flex xs12 sm12 md12 lg12 xl12 :key="index" child-flex  d-flex>
                        <v-card
                            :ripple="false"
                            :href="'/courses/' + course.course_pk + '/' ">
                            <v-card-title>{{course.mnemonic}}{{course.number}} {{ course.title }}</v-card-title>
                            <v-card-text>
                                <div>
                                    <v-chip
                                        class="ma-1" color="teal lighten-2" label small text-color="white">
                                        Rating: {{course.rating_course}}
                                    </v-chip>
                                    <v-chip
                                        class="ma-1" color="teal lighten-2" label small text-color="white">
                                        Taking: {{course.taking}}
                                    </v-chip>
                                    <v-chip
                                        class="ma-1" color="teal lighten-2" label small text-color="white">
                                        Taken: {{course.taken}}
                                    </v-chip>
                                    <v-chip
                                        class="ma-1" :color=" course.last_taught == currentSemester ? 'cyan lighten-2' : 'blue-grey lighten-3' " label small text-color="white">
                                        Last Taught: {{course.last_taught}}
                                    </v-chip>
                                    <v-chip
                                        v-if=" taking_or_taken(course) != '' "
                                        class="ma-1" color="orange darken-1" label small text-color="white">
                                        {{taking_or_taken(course)}}
                                    </v-chip>
                                </div>
                                <v-flex d-flex>
                                    {{ course.description }}
                                </v-flex>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                    <v-flex mt-4 mb-4  v-if="course.divider" :key="index+'divider'">
                    </v-flex>
                    <!-- <v-spacer :key="index+'spacer'"></v-spacer> -->
                </template>
            </v-layout>
        </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import CustomBreadcrumb from '../components/CustomBreadcrumb'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    data() {
        return {
            loaded: false,
            department:{
                name:"",
                school:"",
            },
            courses:[],
            currentSemester:"",
            navItems:[],
        }
    },
    components:{
        CustomHeader,
        CustomBreadcrumb,
    },
    watch: {
    },
    computed:{
        department_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
    },
    methods: {
        getCurrentSemester(){
            axios.get('/courses/api/get_current_semester/',{params: { }}).then(response => {
                this.currentSemester = response.data.year + response.data.semester;
            });
        },
        taking_or_taken(course){
            if(course.take.take == "taking")
                return "Taking"
            else if(course.take.take == "taken")
                return "Taken"
            else
                return ""
        },
        sortCourseNumber(a, b){
            return a.number.toString(10) - b.number.toString(10);
        },
        getDepartment(){
            axios.get('/courses/api/get_department/',{params: {department_pk:this.department_pk, }}).then(response => {
                this.courses = response.data.courses.sort(this.sortCourseNumber);
                for(let i = 0; i < this.courses.length - 1; i++){
                    if(Math.floor(this.courses[i + 1].number.toString(10)/1000) - Math.floor(this.courses[i].number.toString(10)/1000) >= 1){
                        this.courses[i]["divider"] = true;
                    }
                    else{
                        this.courses[i]["divider"] = false;
                    }
                }
                this.department = response.data.department;
                this.navItems = [
                    {
                        text: "Main",
                        disabled: false,
                        href: '/courses/',
                    },
                    {
                        text: "Departments",
                        disabled: false,
                        href: '/courses/departments/',
                    },
                    {
                        text: this.department.name,
                        disabled: true,
                        href:  '/courses/departments/' + this.department_pk + "/",
                    },
                ];
                this.loaded = true;           
            });
        },
        goToHref(text){
            window.location.href = text;
        },
    },
    mounted(){
        this.getCurrentSemester();
        this.getDepartment();
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
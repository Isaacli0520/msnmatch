<template>
  <v-app>
    <custom-header 
        @submit-review="getCourse"
        :headerUpdate="header_update"></custom-header>
    <v-main>
        <v-container v-if="!loaded" fluid fill-height>
            <v-layout 
                align-center
                justify-center>
                <div>
                    <v-progress-circular
                    :size="60"
                    :width="6"
                    v-if="!loaded"
                    indeterminate
                    color="teal lighten-1">
                    </v-progress-circular>
                </div>
            </v-layout>
        </v-container>
        <v-container v-if="loaded" fluid grid-list-lg>
            <v-layout>
                <v-flex>
                    <!-- <v-breadcrumbs class="cus-breadcrumbs" :items="navItems" divider="/"></v-breadcrumbs> -->
                    <custom-breadcrumb :items="navItems"></custom-breadcrumb>
                </v-flex>
            </v-layout>
            <v-layout mb-1>
                <v-flex class="cus-headline-flex"> 
                    <div>
                    <span class="cus-headline-number">{{course.mnemonic}}{{course.number}}</span>
                    <span class="cus-headline-text">{{course.title}}</span>
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout> <!-- Course Description -->
                <v-flex child-flex d-flex>
                    <v-card>
                        <v-card-title>Prerequisite</v-card-title>
                        <v-card-text v-if="course.prerequisite">{{course.prerequisite.trim()}}</v-card-text>
                        <v-card-text v-else>No prereq is specified for this course(Please check on SIS)</v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
            <v-layout wrap> <!-- Prereq and Rate -->
                <v-flex xl7 lg7 md6 sm12 xs12 d-flex child-flex>
                    <v-card>
                        <v-card-title>Description</v-card-title>
                        <v-card-text>{{course.description}}</v-card-text>
                    </v-card>
                </v-flex>
                <v-flex xl5 lg5 md6 sm12 xs12 d-flex child-flex>
                    <custom-rating
                        :rating="course.rating_course"
                        :actiontext="course.taken + ' students have taken this course' "
                        :counter="course.rating_course_counter"
                        ></custom-rating>
                </v-flex>
            </v-layout>
            <v-layout row wrap>
                <template v-for="i in 2">
                    <v-flex :key="i + '-instructor-card' " xs12 sm12 md12 lg12 xl12 d-flex child-flex>
                        <v-card>
                            <v-card-title> {{ i==1 ? 'Instructors teaching this semester': 'Past semesters' }} </v-card-title>
                        </v-card>
                    </v-flex>
                    <v-flex 
                    xs12 sm6 md4 lg4 xl4
                    d-flex 
                    :key="index_instr + (i == 1 ? '-teaching' : '-not-teaching') "
                    v-for="(instructor, index_instr) in i == 1 ? teaching_instructors : not_teaching_instructors">
                        <v-card style="width:100%;">
                            <v-card-title>
                                <div>
                                    <div>{{instructor.name}}</div>
                                    <div v-if="instructor.topic" class="subtitle-1 grey--text">   {{instructor.topic}}</div>
                                </div>
                            </v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <div style="margin: 0px 0px 6px 0px">
                                    <v-chip 
                                        class="ma-1"
                                        v-if="course.take.instructor_pk == instructor.pk"
                                        label
                                        small
                                        text-color="white"
                                        color="orange lighten-1">
                                        {{takeToText(course.take.take)}}
                                    </v-chip>
                                    <v-chip
                                        class="ma-1"
                                        label
                                        small
                                        text-color="white"
                                        color="teal darken-1">
                                        Semesters Taught:{{instructor.semesters.length}}
                                    </v-chip>
                                    <v-chip
                                        class="ma-1"
                                        label
                                        small
                                        text-color="white"
                                        color="teal darken-1">
                                        Taking:{{instructor.taking}}
                                    </v-chip>
                                    <v-chip
                                        class="ma-1"
                                        label
                                        small
                                        text-color="white"
                                        color="teal darken-1">
                                        Taken:{{instructor.taken}}
                                    </v-chip>
                                </div>
                                <div style="margin-left:4px;">
                                    <span>Rating: {{instructor.rating_instructor}}</span>
                                    <v-rating 
                                    color="yellow darken-3"
                                    background-color="grey darken-1"
                                    half-increments
                                    v-model="instructor.rating_instructor"
                                    readonly></v-rating>
                                </div>
                            </v-card-text>
                            <v-divider class=""></v-divider>
                            <v-card-actions class="instructor-card-action">
                                <v-chip
                                    class="ma-1"
                                    outlined
                                    label
                                    color="deep-purple accent-4"
                                    @click="goToHref('/courses/'+course.course_pk+'/'+instructor.pk+'/')"
                                    >
                                    Reviews & More
                                </v-chip>
                                <v-chip
                                    class="ma-1"
                                    @click="openDialogTake(instructor)"
                                    color="deep-purple accent-4" 
                                    outlined
                                    label
                                    >
                                    Planning/Taken
                                </v-chip>
                            </v-card-actions>
                        </v-card>
                    </v-flex>
                </template>
            </v-layout>
        </v-container>
        <v-dialog v-model="dialogTake" scrollable min-width="350px" max-width="600px">
            <v-card>
                <v-card-title>Select Semester</v-card-title>
                <v-divider></v-divider>
                <v-card-text style="height: 300px;">
                    <p class="mt-3 grey--text">Some semesters may not appear in the following list :(</p>
                    <v-checkbox 
                        v-model="takeCourse" 
                        :key="item.value.course_instructor_pk" 
                        v-for="item in takeItemsComputed" 
                        :label="item.label" 
                        :value="item.value"
                        color="black"
                        ></v-checkbox>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="dialogTake = false">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="takeSave()">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-main>
  </v-app>
</template>

<script>

import axios from 'axios'
import { CustomHeader, CustomRating, CustomBreadcrumb } from '../components'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
    data() {
        return {
            header_update:false,
            rating_default:[5,4,3,2,1],
            tmp_num:0,
            course:{
                "course_pk": 0,
                "mnemonic": "",
                "number": "",
                "title": "",
                "description":"",
                "prerequisite":"",
                "category":"",
                "take": {
                    "instructor":"",
                    "semester":"",
                    "take":"",
                },
                "department":{
                    "name":"",
                    "department_pk":"",
                },
                "taking":0,
                "taken":0,
                "instructors":[],
                "rating_course":0,
                "rating_course_counter":[],
            },
            currentSemester:"",

            loaded:false,
            navItems:[],

            takeCourse:null,
            takeItems:[],
            takeItemKey:"", 
            dialogTake: false,
            source: "/lessons/",
        }
    },
    components:{
        CustomHeader,
        CustomRating,
        CustomBreadcrumb,
    },
    watch: {
      
    },
    computed:{
        rating_course_counter_sum(){
            var sum = 0;
            for(let key in this.course.rating_course_counter){
                sum += this.course.rating_course_counter[key];
            }
            return sum;
        },
        takeItemsComputed(){
            return this.takeItems.filter(obj => {
                return obj.value.instructor_pk == this.takeItemKey;
            })
        },
        teaching_instructors(){
            return this.course.instructors.filter(obj => {
                for(let i = 0; i < obj.semesters.length; i++){
                    if(obj.semesters[i].semester == this.currentSemester){
                        return true
                    }
                }
                return false;
            })
        },
        not_teaching_instructors(){
            return this.course.instructors.filter(obj => {
                for(let i = 0; i < obj.semesters.length; i++){
                    if(obj.semesters[i].semester == this.currentSemester){
                        return false
                    }
                }
                return true;
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
        takeToText(txt){
            if(txt == "taking"){
                return "planning";
            }
            else if(txt == "taken"){
                return "taken";
            }
            else{
                return "null";
            }
        },
        getCurrentSemester(){
            axios.get('/courses/ajax/get_current_semester/',{params: {}}).then(response => {
                this.currentSemester = response.data.year + response.data.semester;
                this.getCourse();
            });
        },
        sortBySemester(a, b){
            if(a.substring(0,4) != b.substring(0,4)){
                return b.substring(0,4).toString(10) - a.substring(0,4).toString(10);
            }
            else{
                if(a.substring(4) == b.substring(4)){
                    return 0;
                }
                else if(a.substring(4) == "Fall"){
                    return -1;
                }
                else{
                    return 1;
                }
            }
        },
        openDialogTake(instructor){
            this.takeItemKey = instructor.pk;
            this.dialogTake = true;
        },
        takeSave(){
            var tmp_params = {}
            if(this.takeCourse != null){
                tmp_params = {
                    'course_pk':this.takeCourse.course_pk,
                    'instructor_pk':this.takeCourse.instructor_pk,
                    'semester':this.takeCourse.semester, 
                    'take':this.takeCourse.take,
                    'course_instructor_pk':this.takeCourse.course_instructor_pk,
                    'delete':false,
                }
            }
            else{
                tmp_params = {
                    'course_pk':this.course.course_pk,
                    'instructor_pk':"",
                    'course_instructor_pk':"",
                    'semester':"", 
                    'take':"",
                    'delete':true,
                }
            }
            axios.post('/courses/ajax/save_take/',
            tmp_params,).then(response => {
                if(response.data.success){
                    this.$message({
                        message: 'Updated',
                        type: 'success'
                    });
                }
                this.header_update = !this.header_update;
                this.takeCourse = null;
                this.takeItemKey = "";
                this.getCourse();
            });
            this.dialogTake = false;
        },
        getCourse(){
            axios.get('/courses/api/get_course/',{params: {pk:this.course_pk, }}).then(response => {
                this.course = response.data.course;
                document.title = this.course.mnemonic + this.course.number;
                this.takeItems = [];
                for(let i = 0; i < this.course.instructors.length; i++){
                    // this.course.instructors[i].semesters = this.course.instructors[i].semesters.sort(this.sortBySemester);
                    for(let j = 0; j < this.course.instructors[i].semesters.length; j++){
                        var tmp_label = " Taken";
                        var tmp_take = "taken";
                        if(this.course.instructors[i].semesters[j].semester == this.currentSemester){
                            tmp_label = " Plan on Taking";
                            tmp_take = "taking";
                        }
                        var tmp_topic = ""
                        if(this.course.instructors[i].semesters[j].topic.length > 0)
                            tmp_topic = " Topic: " + this.course.instructors[i].semesters[j].topic;
                        this.takeItems.push({
                            "label":this.course.instructors[i].semesters[j].semester + tmp_label + tmp_topic,
                            "value":{
                                "semester":this.course.instructors[i].semesters[j].semester,
                                "instructor_pk":this.course.instructors[i].pk,
                                "course_pk":this.course.course_pk,
                                "course_instructor_pk":this.course.instructors[i].semesters[j].course_instructor_pk,
                                "topic":this.course.instructors[i].semesters[j].topic,
                                "take": tmp_take,
                            }
                        });
                    }
                }

                for(let k = 0; k < this.takeItems.length; k++){
                    if(this.takeItems[k].value.course_instructor_pk == this.course.take.course_instructor_pk){
                        this.takeCourse = this.takeItems[k].value;
                    }
                }

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
                        text: this.course.department.name,
                        disabled: false,
                        href: '/courses/departments/' + this.course.department.department_pk + "/",
                    },
                    {
                        text: this.course.mnemonic + this.course.number,
                        disabled: true,
                        href: '/courses/'+this.course.course_pk + "/",
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
    },
  };
</script>

<style>
    .instructor-name{
        font-family: "Roboto", sans-serif;
        font-size: 1.6em;
        font-weight: 500;
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
        font-size: 1.6em;
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
        background-color: rgb(226, 225, 225);
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 12px;
        border-radius: 0px 5px 5px 0px;
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

        .instructor-card-action > .v-chip > .v-chip__content{
            font-size:11px !important;
        }


        .cus-headline-number{
            font-size: 1.3em;
        }

        .cus-headline-text{
            font-size: 1.3em;
            
        }

        .instructor-name{
            font-size:1.7em;
        }

        .instructor-banner{
            font-size: 1.3em;
        }

        .instructor-topic{
            font-size:1.4em;
        }

        .v-breadcrumbs li{
            /* font-size:14px !important; */
        }
    }


    /* @media (min-width: 320px) and (max-width: 480px) {

    }

    @media (min-width: 10px) and (max-width: 319px) {
        
    } */
    

</style>
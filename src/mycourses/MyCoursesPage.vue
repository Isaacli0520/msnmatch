<template>
    <v-app>
        <custom-header></custom-header>
        <v-main>
            <v-container fluid grid-list-lg>
                <v-row>
                    <v-col>
                        <custom-breadcrumb :items="navItems"></custom-breadcrumb>
                    </v-col>
                </v-row>
                <v-row mb-3>
                    <v-col> 
                        <span class="cus-headline-text">My Courses</span>
                    </v-col>
                </v-row>
                <v-row v-if="loaded">
                    <v-col cols=12>
                        <v-card elevation="3" color="#fcfcfc">
                            <v-card-title>Courses Planning</v-card-title>
                            <v-card-text>
                                <v-row dense v-if="taking_courses.length > 0">
                                    <v-col 
                                        cols=12 sm=12 md=6 lg=6 xl=6
                                        :key="index_course + '-taking-course' " 
                                        v-for="(course, index_course) in taking_courses">
                                        <v-card hover :href="'/courses/'+ course.course_pk + '/' ">
                                            <v-card-title>
                                                <span class="course-number">{{course.mnemonic}}{{course.number}}</span>
                                                <span class="course-title">{{course.title}}</span>
                                            </v-card-title>
                                        </v-card>
                                    </v-col>
                                </v-row>
                                <span v-else>You can search courses in the search bar and add them as taking/taken.</span>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col cols=12 sm=12 md=6 lg=6 xl=6
                        :key="index_semester + '-semester-course' "
                        v-for="(courses, index_semester) in taken_courses_semester">
                        <v-card elevation="3" color="#fcfcfc">
                            <v-card-title>{{courses.semester}}</v-card-title>
                            <v-card-text>
                                <v-row dense>
                                    <v-col
                                        cols=12
                                        :key="index_course + '-taken-course' " 
                                        v-for="(course, index_course) in courses.courses">
                                        <v-card hover :href="'/courses/'+ course.course_pk + '/' ">
                                            <v-card-title>
                                                <span class="course-number">{{course.mnemonic}}{{course.number}}</span>
                                                <span class="course-title">{{course.title}}</span>
                                            </v-card-title>
                                        </v-card>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
            <v-container fill-height fluid v-if="!loaded" >
                <v-row justify="center">
                    <v-progress-circular
                        :size="60"
                        :width="6"
                        indeterminate
                        color="teal lighten-1"/>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import CustomBreadcrumb from '../components/CustomBreadcrumb'
import { sortBySemester } from '../utils'

export default {
    data() {
        return {
            taking_courses:[],
            taken_courses:[],
            taken_courses_semester:[],
            navItems:[],
            loaded:false,
        }
    },
    components:{
        CustomHeader,
        CustomBreadcrumb,
    },
    methods: {
        goToHref(text){
            window.location.href = text;
        },
        getMyCourses(){
            axios.get('/courses/api/get_my_courses/',{params: {}}).then(response => {
                this.taking_courses = response.data.taking_courses;
                this.taken_courses = response.data.taken_courses;
                this.taken_courses_semester = this.seperateSemesters(this.taken_courses);
                this.loaded = true;
            });
        },
        seperateSemesters(courses){
            var tmp_taking_semester = {}
            for(let i = 0; i < courses.length; i++){
                if(!(courses[i].semester in tmp_taking_semester)){
                    tmp_taking_semester[courses[i].semester] = [];
                }
                tmp_taking_semester[courses[i].semester].push(courses[i]);
            }
            var ret_taking_courses = [];
            for(let key in tmp_taking_semester){
                ret_taking_courses.push({
                    "semester":key,
                    "courses":tmp_taking_semester[key]
                });
            }
            ret_taking_courses = ret_taking_courses.sort((a, b) => {return sortBySemester(a["semester"], b["semester"]);});
            return ret_taking_courses
        },
    },
    mounted(){
        this.navItems = [
            {
                text: "Main",
                disabled: false,
                href: '/courses/',
            },
            {
                text: "My Courses",
                disabled: true,
                href: '',
            },
        ];
        this.getMyCourses();
    },
};
</script>

<style>

    .course-number{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color:#ffffff;
        padding: 3px 5px;
        margin-right: 5px;
        border-radius: 4px;
        line-height: 1.3;
        font-size: 18px;
        background-color: #00796b;
    }

    .course-title{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.3;
        font-size: 18px;
    }

    .v-breadcrumbs li{
        font-size:20px !important;
    }

    .cus-breadcrumbs{
        padding-left: 4px !important;
    }

    .cus-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 2.1em;
        font-weight: 300;
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 3px;
        border-radius: 5px;
        line-height: 1.0;
    }

    @media (min-width: 10px) and (max-width: 767px) {
        .cus-headline-number{
            font-size: 1.3em;
        }

        .cus-headline-text{
            font-size: 1.3em;
        }

        .course-number{
            font-size: 16px;
        }

        .course-title{
            font-size: 16px;
        }

        .v-breadcrumbs li{
            font-size:14px !important;
        }
    }

</style>
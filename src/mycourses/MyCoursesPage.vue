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
                    <v-flex> 
                        <div>
                            <span class="cus-headline-text">My Courses</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-layout wrap>
                    <v-flex d-flex child-flex xs12 sm12 md12 lg12 xl12>
                        <v-card>
                            <v-card-title>Taking Courses</v-card-title>
                            <v-card-text>
                                <v-layout row wrap>
                                    <v-flex 
                                        xs12 sm12 md6 lg6 xl6
                                        :key="index_course + '-taking-course' " 
                                        v-for="(course, index_course) in taking_courses">
                                        <v-list-item
                                            :href="'/courses/'+ course.course_pk + '/' ">
                                            <v-list-item-avatar
                                                color="orange lighten-2">
                                                <span style="color:#fff;">{{index_course + 1}}</span>
                                            </v-list-item-avatar>
                                            <v-list-item-content>
                                                <v-list-item-title>{{course.mnemonic}}{{course.number}} {{course.title}}</v-list-item-title>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-flex>
                                </v-layout>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                    <v-flex d-flex child-flex xs12 sm12 md6 lg6 xl6
                        :key="index_semester + '-semester-course' "
                        v-for="(courses, semester, index_semester) in taken_courses_semester">
                        <v-card>
                            <v-card-title>{{semester}}</v-card-title>
                            <v-card-text>
                                    <v-list
                                        style="width:100%;"
                                        :key="index_course + '-taken-course' " 
                                        v-for="(course, index_course) in courses">
                                        <v-list-item
                                            :href="'/courses/'+ course.course_pk + '/' ">
                                            <v-list-item-avatar
                                                color="orange lighten-2">
                                                <span style="color:#fff;">{{index_course + 1}}</span>
                                            </v-list-item-avatar>
                                            <v-list-item-content>
                                                <v-list-item-title>{{course.mnemonic}}{{course.number}} {{course.title}}</v-list-item-title>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list>
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
import CustomHeader from '../components/CustomHeader'

  export default {
	data() {
	    return {
            taking_courses:[],
            taken_courses:[],
            taken_courses_semester:[],
            navItems:[],
	    }
	},
	components:{
	  CustomHeader,
	},
	watch: {

	},
	computed:{
	  
	},
	methods: {
		goToHref(text){
			window.location.href = text;
        },
        getMyCourses(){
            axios.get('/courses/ajax/get_my_courses/',{params: {}}).then(response => {
                this.taking_courses = response.data.taking_courses;
                this.taken_courses = response.data.taken_courses;
                this.taken_courses_semester = this.seperateSemesters(this.taken_courses);
            });
        },
        seperateSemesters(courses){
            var tmp_taking_semester = {}
            for(let i = 0; i < courses.length; i++){
                if(!(courses[i].semester in tmp_taking_semester)){
                    tmp_taking_semester[courses[i].semester] = []
                }
                tmp_taking_semester[courses[i].semester].push(courses[i])
            }
            return tmp_taking_semester
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
		line-height: 2.0;
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

</style>
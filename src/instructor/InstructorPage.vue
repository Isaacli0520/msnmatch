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
                            <span class="cus-headline-text">{{instructor.name}}</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-layout>
                    <v-flex d-flex child-flex>
                        <custom-rating
                            :rating="instructor.rating"
                            :counter="instructor.rating_counter"
                            :actiontext=" instructor.rating_users_count + ' users have reviewed this instructor.' ">
                        </custom-rating>
                    </v-flex>
                </v-layout>
                <v-layout row wrap>
                    <v-flex xs12 sm6 md4 lg4 xl4 d-flex child-flex
                        :key="index_course"
                        v-for="(course, index_course) in courses">
                        <v-card style="width:100%;">
                            <v-card-title>
                                <div>
                                    <div>{{course.mnemonic}}{{course.number}}</div>
                                    <div class="subtitle-1 grey--text">{{course.title}}</div>
                                </div>
                            </v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-flex>
                                    <span>Rating: {{course.rating}}</span>
                                    <v-rating 
                                    v-model="course.rating"
                                    medium
                                    color="yellow darken-3"
                                    background-color="grey darken-1"
                                    half-increments
                                    readonly></v-rating>
                                </v-flex>
                                <v-flex>
                                    <v-chip
                                        class="ma-1"
                                        label
                                        small
                                        :key="index_semester + 'semester' "
                                        v-for="(semester, index_semester) in course.semesters"
                                        text-color="white"
                                        :color="getSemesterColor(semester)">
                                        {{semester}}
                                    </v-chip>
                                </v-flex>
                                <v-spacer></v-spacer>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-chip
                                    class="ma-1"
                                    outlined
                                    color="deep-purple accent-4"
                                    @click="goToHref('/courses/'+course.course_pk+'/'+instructor_pk+'/')"
                                    >
                                    Learn More
                                </v-chip>
                            </v-card-actions>
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
import CustomRating from '../components/CustomRating'
import CustomFooter from '../components/CustomFooter'

  export default {
	data() {
	    return {
            rating_default:[5,4,3,2,1],
            taking_courses:[],
            taken_courses:[],
            taken_courses_semester:[],
            navItems:[],
            instructor:{
                name:"",
                rating:0,
                rating_counter:[],
                courses:[],
            },
            courses:[],
	    }
	},
	components:{
        CustomHeader,
        CustomRating,
        CustomFooter,
	},
	watch: {

	},
	computed:{
        instructor_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
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
        sortByNumber(a, b){
            return a.number.toString(10) - b.number.toString(10);
        },
        getSemesterColor(semester){
            if(semester.substring(4) == "Fall"){
                return 'orange';
            }
            else if(semester.substring(4) == "Spring"){
                return 'green';
            }
            else{
                return "";
            }
        },
		goToHref(text){
			window.location.href = text;
        },
        getInstructor(){
            axios.get('/courses/ajax/get_instructor/',{params: {"instructor_pk":this.instructor_pk,}}).then(response => {
                this.instructor = response.data;
                for(var key in this.instructor.courses){
                    this.instructor.courses[key].semesters = this.instructor.courses[key].semesters.sort(this.sortBySemester);
                    this.courses.push(this.instructor.courses[key]);
                }
                this.courses = this.courses.sort(this.sortByNumber);
                this.navItems = [
                    {
                        text: "Main",
                        disabled: false,
                        href: '/courses/',
                    },
                    {
                        text: this.instructor.name,
                        disabled: true,
                        href: '',
                    },
                ];
            });
        },
	},
	mounted(){
        this.getInstructor();
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
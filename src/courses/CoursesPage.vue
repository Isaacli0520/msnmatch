<template>
    <v-app>
        <custom-header
            ref="custom_header"
            :searchBool="false"></custom-header>
        <v-main>
            <v-container fluid grid-list-xl class="courses-main">
                <v-row>
                    <v-col cols="12" sm="12" md="8" lg="8" xl="6" offset-md="2" offset-lg="2" offset-xl="3">
                        <v-row>
                            <div class="headline-div-center">
                                <div class="cus-headline-title-text">HOOS MY PROFESSOR</div>
                                <div class="cus-subheadline-title-text">Reviews, Ratings & More</div>
                            </div>
                        </v-row>
                        <v-row row wrap>
                            <v-spacer></v-spacer>
                            <v-col cols="10">
                                <search-course class="custom-search"
                                    :dense="false"
                                    background_color="white"></search-course>
                            </v-col>
                            <v-spacer></v-spacer>
                        </v-row>
                        <v-row class="spacer-layout"></v-row>
                        <v-row>
                            <template v-for="(func, index) in main_functions">
                                <v-col :key="index" sm="4" md="4" lg="4" xl="4" cols="6">
                                    <v-tooltip top>
                                        <template v-slot:activator="{ on, attrs }">
                                            <v-card
                                                v-bind="attrs"
                                                v-on="on"
                                                @click.native="navFunctions(func)"
                                                :ripple="false"
                                                hover>
                                                <v-card-text>
                                                    <v-layout class="align-center justify-center">
                                                    <div style="padding: 8px;"><v-icon
                                                        x-large
                                                        color="teal darken-2"
                                                        >{{func.icon}}</v-icon></div>
                                                    </v-layout>
                                                </v-card-text>
                                                <v-divider></v-divider>
                                                <v-card-actions class="justify-center">
                                                    <span class="function-subtext">{{func.title}}</span>
                                                </v-card-actions>
                                            </v-card>
                                        </template>
                                        <span>{{func.tip}}</span>
                                    </v-tooltip>
                                </v-col>
                            </template>
                        </v-row>
                        <!-- Interesting Reviews -->
                        <template>
                            <v-layout mt-2 row wrap>
                                <v-flex> 
                                    <div class="headline-div">
                                        <span class="cus-headline-text">Interesting Reviews</span>
                                        <v-btn class="mb-2" color="teal darken-2" icon outlined
                                            :loading="topReviewsLoading" @click="getTopReviews()">
                                            <v-icon>mdi-refresh</v-icon>
                                        </v-btn>
                                    </div>
                                </v-flex>
                                <v-spacer></v-spacer>
                            </v-layout>
                            <v-row v-if="!topReviewsLoading">
                                <template v-for="(review, index) in top_reviews">
                                    <v-col :key="index" cols="12">
                                        <review-card :review="review" :editable="false"></review-card>
                                    </v-col>
                                </template>
                            </v-row>
                            <v-container v-else fluid>
                                <v-layout 
                                    style="padding:15px;"
                                    align-center
                                    justify-center>
                                    <v-progress-circular
                                        :size="60"
                                        :width="6"
                                        v-if="topReviewsLoading"
                                        indeterminate
                                        color="teal lighten-1"/>
                                </v-layout>
                            </v-container>
                        </template>
                        <!-- Trending Courses -->
                        <template>
                            <v-layout row wrap>
                                <v-flex> 
                                    <div class="headline-div">
                                    <span class="cus-headline-text">Popular Courses</span>
                                    </div>
                                </v-flex>
                                <v-spacer></v-spacer>
                            </v-layout>
                            <v-row v-if="!trendingCoursesLoading">
                                <v-col cols="12" v-for="(course, index) in trending_courses['Taken']" :key="index">
                                    <v-card
                                        outlined
                                        elevation="3"
                                        :href="'/courses/' + course.course_pk + '/' ">
                                        <v-card-title style="padding-bottom:8px;">
                                            <span class="course-number">{{course.mnemonic}}{{course.number}}</span>
                                            <span class="course-name">{{course.title}}</span>
                                        </v-card-title>
                                        <v-card-text>
                                            {{ course.description }}
                                        </v-card-text>
                                        <v-divider></v-divider>
                                        <v-card-actions style="flex-flow:row wrap !important;">
                                            <v-spacer v-if="$vuetify.breakpoint.smAndUp"></v-spacer>
                                            <v-chip
                                                class="ma-1" color="teal darken-2" label outlined small>
                                                Last Taught: {{course.last_taught}}
                                            </v-chip>
                                            <v-chip
                                                class="ma-1" color="teal darken-2" label outlined small>
                                                Taking: {{course.taking}}
                                            </v-chip>
                                            <v-chip
                                                class="ma-1" color="teal darken-2" label outlined small>
                                                Taken: {{course.taken}}
                                            </v-chip>
                                        </v-card-actions>
                                    </v-card>
                                </v-col>
                            </v-row>
                            <v-container v-else fluid>
                                <v-layout 
                                    style="padding:15px;"
                                    align-center
                                    justify-center>
                                    <v-progress-circular
                                        :size="60"
                                        :width="6"
                                        v-if="trendingCoursesLoading"
                                        indeterminate
                                        color="teal lighten-1"/>
                                </v-layout>
                            </v-container>
                        </template>
                    </v-col>
                </v-row>
            </v-container>
            <recommendation v-model="recommendationDialog"/>
        </v-main>
    </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import SearchCourse from '../components/SearchCourse'
import ReviewCard from '../components/ReviewCard'
import Recommendation from '../components/Recommendation'
import { general_urls, general_icons } from '../utils'

export default {
    data() {
        return {
            topReviewsLoading:true,
            trendingCoursesLoading:true,
            recommendationDialog:false,
            trending_courses:{
                "Taking":[],
                "Taken":[],
            },
            top_reviews:[],
            main_functions:{
                "my_courses":{
                    "title":"My Courses",
                    "icon":general_icons.my_courses,
                    "tip":"View your taken courses",
                },
                "my_reviews":{
                    "title":"My Reviews",
                    "icon":general_icons.my_reviews,
                    "tip":"View your reviews",
                },
                "submit_review":{
                    "title":"Submit a Review",
                    "icon":general_icons.submit_review,
                    "tip":"Submit a new review :)",
                },
                "departments":{
                    "title":"Departments",
                    "icon":general_icons.departments,
                    "tip":"View courses by departments",
                },
                "plannable":{
                    "title":"Plannable",
                    "icon":general_icons.plannable,
                    "tip":"Go to plannable and schedule your courses",
                },
                "recommendation":{
                    "title":"Recommendation",
                    "icon":general_icons.recommendation,
                    "tip":"Provide recommendations based on semester and major",
                },
            },
        }
    },
    components:{
        CustomHeader,
        SearchCourse,
        ReviewCard,
        Recommendation,
    },
    computed:{

    },
    methods: {
        navFunctions(func){
            if(func.title == "My Courses"){
                this.goToHref(general_urls.my_courses_url);
            }
            else if(func.title == "My Reviews"){
                this.goToHref(general_urls.review_url);
            }
            else if(func.title == "Submit a Review"){
                this.$refs.custom_header.openSubmitReviewDialog();
            }
            else if(func.title == "Departments"){
                this.goToHref(general_urls.department_url);
            }
            else if(func.title == "Plannable"){
                this.$refs.custom_header.navMethod(func);
            }
            else if(func.title == "Recommendation"){
                this.recommendationDialog = true;
            }
        },
        goToHref(text){
            window.location.href = text;
        },
        getTrendingCourses(){
            axios.get('/courses/api/get_trending_courses/',{params: {}}).then(response => {
                this.trending_courses["Taken"] = response.data.taken_courses;
                this.trendingCoursesLoading = false;
            });
        },
        getTopReviews(){
            this.topReviewsLoading = true;
            axios.get('/courses/api/get_top_reviews/',{params: {}}).then(response => {
                this.top_reviews = response.data.reviews;
                this.topReviewsLoading = false;
            });
        },
    },
    mounted(){
        this.getTopReviews();
        this.getTrendingCourses();
    },
};
</script>

<style scoped>
    .spacer-layout{
        padding: 10px 5px 15px 5px;
    }

    .headline-div-center{
        width:100%;
        margin: 0 auto;
        text-align: center; 
        padding: 22px 12px 32px 12px;
    }

    .custom-search{
        box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
    }

    .search-courses{
        position: relative;
        margin: auto auto 60px auto;
        width: 80%;
        max-width: 600px;
    }

    .main-title{
        margin-top: 100px;
        margin-bottom: 30px;
        /* color:#32a49a; */
        color:rgb(0, 0, 0);
        font-weight: 800 !important;
        /* font-family: Baskerville, "Baskerville Old Face", sans-serif; */
        /* text-transform: uppercase; */
        font-family: "Raleway", Helvetica, sans-serif;
        /* font-family: Optima, sans-serif; */
        font-size: 45px;
        letter-spacing: 0.05em;
    }

    .recommendation-div{
        overflow: scroll;
        max-height: 248px;
    }

    .function-subtext{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 300;
        font-size: 1.05em;
        letter-spacing: 0.04em;
    }

    .course-number{
        font-family: "Roboto", sans-serif;
        font-size: 1.1em;
        font-weight: 500;
        background-color: rgb(13, 124, 109);
        color:#fff;
        padding: 1px 7px 1px 7px;
        border-radius: 5px 0px 0px 5px;
        line-height: 1.4;
    }

    .course-name{
        white-space: normal;
        font-family: "Roboto", sans-serif;
        font-size: 1.1em;
        font-weight: 300;
        background-color: rgb(240, 240, 240);
        color:rgb(0, 0, 0);
        padding: 1px 7px 1px 7px;
        border-radius: 0px 5px 5px 0px;
        line-height: 1.4;

    }

    .cus-subheadline-title-text{
        font-family: "Roboto", sans-serif;
        font-size: 1.4em;
        font-weight: 300;
        letter-spacing: 0.06em;
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 3px;
        line-height: 1.0;
    }

    .cus-headline-title-text{
        font-family: "Roboto", sans-serif;
        font-size: 2.3em;
        font-weight: 300;
        letter-spacing: 0.06em;
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 3px;
        line-height: 1.0;
    }

    .cus-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 1.8em;
        font-weight: 300;
        color:rgb(0, 0, 0);
        padding: 7px 12px 7px 3px;
        border-radius: 5px;
        line-height: 1.0;
    }

    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
        .main-title{
            font-size: 45px;
        }
        .search-courses{
            margin: auto auto 45px auto;
        }
    }


    @media (min-width: 10px) and (max-width: 767px) {

        .cus-headline-title-text{
            font-size: 25px;
        }

        .cus-subheadline-title-text{
            font-size: 18px;
        }

        .course-name{
            font-size: 15px;
        }

        .course-number{
            font-size: 15px;
        }

        .main-title{
            font-size: 28px;
            margin-top: 60px;
            margin-bottom: 20px;
        }
        .recommendation-div{
            overflow: scroll;
            max-height: 300px;
        }
        .search-courses{
            margin: auto auto 30px auto;
        }
        
    }

</style>
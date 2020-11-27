<template>
    <v-app>
        <custom-header
            ref="custom_header"
            :searchBool="false"></custom-header>
        <v-main>
            <v-container fluid grid-list-xl class="courses-main">
                <v-row>
                <v-col xs="12" sm="12" md="8" lg="8" xl="6" offset-md="2" offset-lg="2" offset-xl="3">
                <v-row>
                    <div class="headline-div-center">
                        <div class="cus-headline-title-text">HOOS MY PROFESSOR</div>
                        <div class="cus-subheadline-title-text">Reviews, Ratings & More</div>
                    </div>
                </v-row>
                <v-row row wrap>
                    <v-spacer></v-spacer>
                    <v-flex d-flex xs10 sm10 md10 lg10 xl10>
                        <search-course class="custom-search"
                            :dense="false"
                            background_color="white"></search-course>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-row>
                <v-row class="spacer-layout"></v-row>
                <v-row>
                    <template v-for="(func, index) in main_functions">
                        <v-col :key="index" sm="3" md="3" lg="3" xl="3" cols="6">
                            <v-card
                                @click.native="navFunctions(func)"
                                class="fill-height"
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
                        </v-col>
                    </template>
                </v-row>
                <!-- <v-layout wrap>
                    <v-flex child-flex d-flex xs12 sm12 md12 lg12 xl12>
                        <v-card
                            outlined
                            elevation="3"
                            :loading="!recommendation_loaded">
                            <v-card-title>Recommendations</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-layout row wrap>
                                    <v-flex xs6 sm6 md4 lg4 xl4 d-flex>
                                        <v-select
                                            v-model="year"
                                            :items="year_options"
                                            label="Year"
                                            hide-details
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                    <v-flex xs6 sm6 md4 lg4 xl4 d-flex>
                                        <v-select
                                            v-model="semester"
                                            :items="semester_options"
                                            label="Semester"
                                            hide-details
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                    <v-flex xs12 sm12 md4 lg4 xl4 d-flex>
                                        <v-select
                                            v-model="major"
                                            :items="major_options"
                                            label="Major"
                                            hide-details
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                </v-layout>
                                    <div class="recommendation-div"
                                        v-if="recommendation_loaded">
                                        <template v-if="rcm_courses.length>0">
                                            <v-list-item
                                                style="width:100%;"
                                                :key="index_course + '-rcm-course' " 
                                                v-for="(course, index_course) in rcm_courses"
                                                :href="'/courses/'+ course.course_pk + '/' ">
                                                <v-list-item-avatar
                                                    color="teal lighten-2">
                                                    <span style="color:#fff;">{{index_course + 1}}</span>
                                                </v-list-item-avatar>
                                                <v-list-item-content two-line>
                                                    <v-list-item-title>{{course.mnemonic}}{{course.number}} {{course.title}}</v-list-item-title>
                                                    <v-list-item-subtitle>Taken: {{ course.taken }}</v-list-item-subtitle>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </template>
                                        <div v-else>
                                            Recommendations are not available for this setting.
                                        </div>
                                    </div>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                </v-layout> -->
                <template v-if="top_reviews.length > 0">
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
                    <v-row>
                        <template v-for="(review, index) in top_reviews">
                            <v-col :key="index"
                                cols="12"
                                sm="12"
                                md="12"
                                lg="12"
                                xl="12">
                                <review-card :review="review" :editable="false"></review-card>
                            </v-col>
                        </template>
                    </v-row>
                </template>
                <template v-if="trending_courses['Taken'].length > 0">
                    <v-layout row wrap>
                        <v-flex> 
                            <div class="headline-div">
                            <span class="cus-headline-text">Popular Courses</span>
                            </div>
                        </v-flex>
                        <v-spacer></v-spacer>
                    </v-layout>
                    <v-layout row wrap>
                        <template v-for="(course, index) in trending_courses['Taken']">
                            <v-flex xs12 sm12 md12 lg12 xl12 :key="index" child-flex  d-flex>
                                <v-card
                                    outlined
                                    elevation="3"
                                    :href="'/courses/' + course.course_pk + '/' ">
                                    <v-card-title>
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
                            </v-flex>
                        </template>
                    </v-layout>
                </template>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import axios from 'axios'
import { CustomHeader, SearchCourse, ReviewCard } from '../components'
import { general_urls, general_icons } from '../utils'
// import CustomHeader from '../components/CustomHeader'
// import SearchCourse from '../components/SearchCourse'
// import ReviewCard from '../components/ReviewCard'

  export default {
    data() {
        return {
            topReviewsLoading:true,
            loaded:{
                "Taken":false,
            },
            trending_courses:{
                "Taking":[],
                "Taken":[],
            },
            top_reviews:[],
            main_functions:{
                "my_courses":{
                    "title":"My Courses",
                    "icon":general_icons.my_courses,
                },
                "my_reviews":{
                    "title":"My Reviews",
                    "icon":general_icons.my_reviews,
                },
                "submit_review":{
                    "title":"Submit a Review",
                    "icon":general_icons.submit_review,
                },
                "departments":{
                    "title":"Departments",
                    "icon":general_icons.departments,
                },
            },
            // user_info_get:false,
            // recommendation_loaded:false,
            // year:1,
            // semester:"",
            // major:null,
            // major_options:[],
            // year_options:[
            //     {"text":"1","value":1,},
            //     {"text":"2","value":2,},
            //     {"text":"3","value":3,},
            //     {"text":"4","value":4,},
            // ],
            // semester_options:[
            //     {"text":"Fall","value":"Fall",},
            //     {"text":"Spring","value":"Spring",},
            // ],
            // rcm_courses:[],
        }
    },
    components:{
        CustomHeader,
        SearchCourse,
        ReviewCard,
    },
    watch: {
        // year(){
        //     if(this.user_info_get){
        //         this.recommendation_loaded = false;
        //         this.getRecommendations();
        //     }
        // },
        // semester(){
        //     if(this.user_info_get){
        //         this.recommendation_loaded = false;
        //         this.getRecommendations();
        //     }
        // },
        // major(){
        //     if(this.user_info_get){
        //         this.recommendation_loaded = false;
        //         this.getRecommendations();
        //     }
        // },
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
        },
        getCurrentSemester(){
            axios.get('/courses/ajax/get_current_semester/',{params: { }}).then(response => {
                this.semester = response.data.semester;
            });
        },
        goToHref(text){
            window.location.href = text;
        },
        getTrendingCourses(){
            axios.get('/courses/ajax/get_trending_courses/',{params: {}}).then(response => {
                this.trending_courses["Taken"] = response.data.taken_courses;
                this.loaded["Taken"] = true;
            });
        },
        getTopReviews(){
            this.topReviewsLoading = true;
            axios.get('/courses/api/get_top_reviews/',{params: {}}).then(response => {
                this.top_reviews = response.data.reviews;
                this.topReviewsLoading = false;
            });
        },
        // getRecommendations(){
        //     axios.get('/courses/ajax/get_recommendations/',{params: {year:this.year, semester:this.semester, major:this.major}}).then(response => {
        //         this.rcm_courses = response.data.rcm_courses;
        //         this.recommendation_loaded = true;
        //         this.user_info_get = true;
        //     });
        // },
        // getMajorOptions(){
        //     axios.get('/courses/ajax/get_major_options/',{params: {}}).then(response => {
        //         this.major_options = response.data.major_options;
        //         this.major = response.data.major == "" ? this.major_options[0].value : response.data.major;
        //         this.semester = response.data.semester == "" ? this.semester_options[0].value : response.data.semester;
        //         this.year = response.data.year == 0 ? this.year_options[0].value : response.data.year;
        //         this.getRecommendations();
        //     });
        // },
    },
    mounted(){
        this.getTopReviews();
        this.getTrendingCourses();
        // this.getMajorOptions();
        this.getCurrentSemester();
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

    .upper-div{
        position: relative;
        padding: 75px 0px 20px 0px;
        color:#000000;
        background-color: #fff;
        width:100%;
        /* height: 100%; */
        position:relative;
        /* background: url('../assets/static/css/images/cloud_new_09.jpg') no-repeat;
        background-attachment: fixed;
        background-position: center center;
        background-size: cover; */

        /* -webkit-box-shadow: inset 0 -3px 3px 0px rgba(0,0,0,.13), inset 0 -7px 7px 0px rgba(0,0,0,.12);
        box-shadow: inset 0 -3px 3px 0px rgba(0,0,0,.13), inset 0 -7px 7px 0px rgba(0,0,0,.12); */
        /* padding: 0; */
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
        box-decoration-break: clone;
    }

    .course-name{
        font-family: "Roboto", sans-serif;
        font-size: 1.1em;
        font-weight: 300;
        background-color: rgb(240, 240, 240);
        color:rgb(0, 0, 0);
        padding: 1px 7px 1px 7px;
        border-radius: 0px 5px 5px 0px;
        line-height: 1.4;
        box-decoration-break: clone;

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

        .course-name{
            font-size: 0.95em
        }

        .course-number{
            font-size: 0.95em;
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
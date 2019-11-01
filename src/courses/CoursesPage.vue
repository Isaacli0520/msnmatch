<template>
    <v-app>
        <custom-header
            :searchBool="false"></custom-header>
        <v-content>
            <v-container fluid grid-list-xl class="courses-main">
                <v-layout wrap>
                    <v-flex child-flex d-flex xs12 sm12 md12 lg12 xl12>
                    <v-card
                        outlined
                        elevation="3">

                            <div class="headline-div-center">
                                <span class="cus-headline-title-text">Search Courses</span>
                            </div>
                        <v-layout row wrap>
                            <v-spacer></v-spacer>
                            <v-flex d-flex xs10 sm10 md8 lg8 xl8>
                                <search-course class="custom-search"
                                    background_color="white"></search-course>
                            </v-flex>
                            <v-spacer></v-spacer>
                        </v-layout>
                        <v-layout class="spacer-layout"></v-layout>
                        <v-spacer></v-spacer>
                    </v-card>
                    </v-flex>
                </v-layout>
                <v-layout wrap>
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
                    <!-- <template v-for="i in ['Taking', 'Taken']">
                        <v-flex child-flex d-flex :key="i + '-taking-taken' " xs12 sm4 md4 lg4 xl4>
                            <v-card 
                                :elevation="cardElevation"
                                :loading="!loaded[i]">
                                <v-card-title>Top 10 {{i}} Courses</v-card-title>
                                <v-divider></v-divider>
                                <v-card-text>
                                    <v-list v-if="loaded[i]">
                                        <v-list-item
                                            style="width:100%;"
                                            :key="index_course + '-trending-course' " 
                                            v-for="(course, index_course) in trending_courses[i]"
                                            :href="'/courses/'+ course.course_pk + '/' ">
                                            <v-list-item-avatar
                                                color="teal lighten-1">
                                                <span style="color:#fff;">{{index_course + 1}}</span>
                                            </v-list-item-avatar>
                                            <v-list-item-content two-line>
                                                <v-list-item-title>{{course.mnemonic}}{{course.number}} {{course.title}}</v-list-item-title>
                                                <v-list-item-subtitle>{{i}}: {{course[i.toLowerCase()]}}</v-list-item-subtitle>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list>
                                </v-card-text>
                            </v-card>
                        </v-flex>
                    </template>
                    <v-flex child-flex d-flex xs12 sm4 md4 lg4 xl4>
                        <v-card 
                            :elevation="cardElevation"
                            :loading="!review_user_load">
                            <v-card-title>Top 10 Users</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-list v-if="review_user_load">
                                    <v-list-item
                                        style="width:100%;"
                                        :key="index_review + '-review_user' " 
                                        v-for="(user, index_review) in review_users"
                                        :href="'/users/'+ user.username + '/' ">
                                        <v-list-item-avatar
                                            color="teal lighten-1"
                                            >
                                            <span style="color:#fff;">{{index_review + 1}}</span>
                                        </v-list-item-avatar>
                                        <v-list-item-content two-line>
                                            <v-list-item-title>{{user.name}}</v-list-item-title>
                                            <v-list-item-subtitle>Reviews: {{user.reviews}}</v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-card-text>
                        </v-card>
                    </v-flex> -->
                </v-layout>
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
                                <v-card-title>{{course.mnemonic}}{{course.number}} {{ course.title }}</v-card-title>
                                <v-card-text>
                                    <div>
                                        <!-- <v-chip
                                            class="ma-1" color="teal lighten-2" label small text-color="white">
                                            Rating: {{course.rating_course}}
                                        </v-chip> -->
                                        <v-chip
                                            class="ma-1" color="teal lighten-2" label small text-color="white">
                                            Taking: {{course.taking}}
                                        </v-chip>
                                        <v-chip
                                            class="ma-1" color="teal lighten-2" label small text-color="white">
                                            Taken: {{course.taken}}
                                        </v-chip>
                                        <!-- <v-chip
                                            v-if=" taking_or_taken(course) != '' "
                                            class="ma-1" color="orange darken-1" label small text-color="white">
                                            {{taking_or_taken(course)}}
                                        </v-chip> -->
                                    </div>
                                    <v-flex d-flex>
                                        {{ course.description }}
                                    </v-flex>
                                </v-card-text>
                            </v-card>
                        </v-flex>
                        <!-- <v-spacer :key="index+'spacer'"></v-spacer> -->
                    </template>
                </v-layout>
                <!-- <v-layout>
                    <v-flex xs12 sm12 md12 lg12 xl12 child-flex d-flex>
                        <v-card 
                            :elevation="cardElevation"
                            :loading="!review_user_load">
                            <v-card-title>Top 30 Users</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-list v-if="review_user_load">
                                    <v-list-item
                                        style="width:100%;"
                                        :key="index_review + '-review_user' " 
                                        v-for="(user, index_review) in review_users"
                                        :href="'/users/'+ user.username + '/' ">
                                        <v-list-item-avatar
                                            color="teal lighten-1"
                                            >
                                            <span style="color:#fff;">{{index_review + 1}}</span>
                                        </v-list-item-avatar>
                                        <v-list-item-content two-line>
                                            <v-list-item-title>{{user.name}}</v-list-item-title>
                                            <v-list-item-subtitle>Reviews: {{user.reviews}}</v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                </v-layout> -->
            </v-container>
        </v-content>
        <!-- <custom-footer></custom-footer> -->
    </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import SearchCourse from '../components/SearchCourse'
import CustomFooter from '../components/CustomFooter'

  export default {
	data() {
	    return {
            cardElevation:4,
            review_users:[],
            review_user_load:false,
            recommendation_loaded:false,
            loaded:{
                "Taken":false,
                "Taking":false,
            },
            credential:"",
            plannableURL:"",
            username:"",
            year:1,
            semester:"",
            major:null,
            major_options:[],
            taking_courses:[],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                courses_url:"",
                match_url:"",
            },
            year_options:[
                {
                    "text":"1",
                    "value":1,
                },
                {
                    "text":"2",
                    "value":2,
                },
                {
                    "text":"3",
                    "value":3,
                },
                {
                    "text":"4",
                    "value":4,
                },
            ],
            semester_options:[
                {
                    "text":"Fall",
                    "value":"Fall",
                },
                {
                    "text":"Spring",
                    "value":"Spring",
                },
            ],
            with_carousel:false,
            trending_courses:{
                "Taking":[],
                "Taken":[],
            },
            rcm_courses:[],
            trash_items:[
                {
                    "title":"Departments",
                    "icon":"fas fa-list-ol",
                    "href":"/courses/departments/",
                    "target":"",
                },
                {
                    "title":"Courses",
                    "icon":"fas fa-user-circle",
                    "href":"",
                    "target":"",
                },
                {
                    "title":"Reviews",
                    "icon":"fas fa-book",
                    "href":"/courses/reviews/",
                    "target":"",
                },
                {
                    "title":"Plannable",
                    "icon":"fas fa-paper-plane",
                    "href":"https://plannable.org",
                    "target":"_blank",
                },
                {
                    "title":"Home",
                    "icon":"fas fa-home",
                    "href":"/",
                    "target":"",
                },
            ],
            colors: [
                'primary',
                'secondary',
                'yellow darken-2',
                'red',
                'orange',
            ],
            courseTypes:[
                'Clinical',
                'Discussion',
                'Drill',
                'Independent Study',
                'Laboratory',
                'Lecture',
                'Practicum',
                'Seminar',
                'Studio',
                'Workshop',
                '',
            ]
	    }
	},
	components:{
        CustomHeader,
        SearchCourse,
        CustomFooter,
	},
	watch: {
        year(){
            this.recommendation_loaded = false;
            this.getRecommendations();
        },
        semester(){
            this.recommendation_loaded = false;
            this.getRecommendations();
        },
        major(){
            this.recommendation_loaded = false;
            this.getRecommendations();
        },
	},
	computed:{
	},
	methods: {
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
                this.trending_courses["Taking"] = response.data.taking_courses;
                this.trending_courses["Taken"] = response.data.taken_courses;
                this.loaded["Taken"] = true;
                this.loaded["Taking"] = true;
            });
        },
        getReviewUsers(){
            this.review_user_load = false;
            axios.get('/courses/ajax/get_top_review_users/',{params: {}}).then(response => {
                this.review_users = response.data.review_users;
                this.review_user_load = true;
            });
        },
        getRecommendations(){
            axios.get('/courses/ajax/get_recommendations/',{params: {year:this.year, semester:this.semester, major:this.major}}).then(response => {
                this.rcm_courses = response.data.rcm_courses;
                this.recommendation_loaded = true;
            });
        },
        getMajorOptions(){
            axios.get('/courses/ajax/get_major_options/',{params: {}}).then(response => {
                this.major_options = response.data.major_options;
                this.major = response.data.major == "" ? this.major_options[0].value : response.data.major;
                this.semester = response.data.semester == "" ? this.semester_options[0].value : response.data.semester;
                this.year = response.data.year == 0 ? this.year_options[0].value : response.data.year;
                this.getRecommendations();
            });
        },
        getTakingCourses(){
            axios.get('/courses/ajax/get_taking_courses/',{params: {}}).then(response => {
                this.taking_courses = response.data.taking_courses;
            });
        },
	},
	mounted(){
        this.getTrendingCourses();
        this.getMajorOptions();
        this.getTakingCourses();
        this.getReviewUsers();
        this.getCurrentSemester();
	},
  };
</script>

<style>
    .spacer-layout{
        padding: 10px 5px 50px 5px;
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

    .courses-main{
        /* background-color: #fff; */
        /* background: url('../assets/static/css/images/cloud_new_11.jpg') no-repeat;
        background-attachment: fixed;
        background-position: center center;
        background-size: cover; */
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

    .cus-headline-title-text{
		font-family: "Roboto", sans-serif;
		font-size: 2.1em;
		font-weight: 300;
		color:rgb(0, 0, 0);
		padding: 7px 12px 7px 3px;
		border-radius: 5px;
		line-height: 1.0;
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
            font-size:1.7em;
        }

        .

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
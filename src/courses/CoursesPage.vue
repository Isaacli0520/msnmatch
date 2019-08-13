<template>
    <v-app>
        <custom-header></custom-header>
        <v-content>
            <v-carousel v-if="with_carousel">
                <v-carousel-item
                    v-for="(color, i) in colors"
                    :key="color"
                >
                    <v-sheet
                    :color="color"
                    height="100%"
                    tile
                    >
                    <v-layout
                        align-center
                        fill-height
                        justify-center
                    >
                        <div class="display-3">Slide {{ i + 1 }}</div>
                    </v-layout>
                    </v-sheet>
                </v-carousel-item>
            </v-carousel>
            <div class="upper-div">
                <div class="container mb-1 text-center">
                    <h1 class="main-title">HoosMyProfessor</h1>
                </div>
            </div>
            <v-container fluid grid-list-xl class="courses-main"> 
                <v-layout wrap>
                    <v-flex xs12 sm12 md4 lg4 xl4>
                        <v-card
                            :elevation="cardElevation">
                            <v-card-title>Trash Can</v-card-title>
                            <v-card-text>
                                <v-list>
                                    <v-list-item
                                        style="width:100%;"
                                        :key="index_item + '-trash' " 
                                        v-for="(item, index_item) in trash_items"
                                        :href="item.href"
                                        :target="item.target">
                                        <v-list-item-avatar
                                            v-if="item.icon">
                                            <v-icon>{{ item.icon }}</v-icon>
                                        </v-list-item-avatar>
                                        <v-list-item-content>
                                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-card-text>
                            <v-card-actions></v-card-actions>
                        </v-card>
                    </v-flex>
                    <v-flex child-flex d-flex xs12 sm12 md8 lg8 xl8>
                        <v-card
                            :elevation="cardElevation"
                            :loading="!recommendation_loaded">
                            <v-card-title>Recommendations</v-card-title>
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
                                                    color="orange lighten-2">
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
                    <template v-for="i in ['Taking', 'Taken']">
                        <v-flex child-flex d-flex :key="i + '-taking-taken' " xs12 sm4 md4 lg4 xl4>
                            <v-card 
                                :elevation="cardElevation"
                                :loading="!loaded[i]">
                                <v-card-title>Top 10 {{i}} Courses</v-card-title>
                                <v-card-text>
                                    <v-list v-if="loaded[i]">
                                        <v-list-item
                                            style="width:100%;"
                                            :key="index_course + '-trending-course' " 
                                            v-for="(course, index_course) in trending_courses[i]"
                                            :href="'/courses/'+ course.course_pk + '/' ">
                                            <v-list-item-avatar
                                                color="orange lighten-2">
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
                            <v-card-text>
                                <v-list v-if="review_user_load">
                                    <v-list-item
                                        style="width:100%;"
                                        :key="index_review + '-review_user' " 
                                        v-for="(user, index_review) in review_users"
                                        :href="'/users/'+ user.username + '/' ">
                                        <v-list-item-avatar
                                            color="orange lighten-2"
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
            cardElevation: 4,
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
            semester:"Fall",
            major:null,
            major_options:[],
            taking_courses:[],
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
                    "title":"Browse by Departments",
                    "icon":"fas fa-list-ol",
                    "href":"/courses/departments/",
                    "target":"",
                },
                {
                    "title":"My Courses",
                    "icon":"fas fa-user-circle",
                    "href":"",
                    "target":"",
                },
                {
                    "title":"My Reviews",
                    "icon":"fas fa-book",
                    "href":"/courses/reviews/",
                    "target":"",
                },
                {
                    "title":"Go to Plannable",
                    "icon":"fas fa-paper-plane",
                    "href":"https://plannable.gitee.io",
                    "target":"_blank",
                },
                {
                    "title":"Home Page",
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
	},
	watch: {
        taking_courses(val){
            var tmp_arr = [];
            for(let i = 0; i < val.length; i++){
                tmp_arr.push(val[i].mnemonic.toLowerCase() + val[i].number+this.courseTypes.indexOf(val[i].type).toString(10))
            }
            this.plannableURL = JSON.stringify(tmp_arr);
            this.getPlannableURL();
        },
        credential(){
            this.getPlannableURL();
        },
        username(){
            this.getPlannableURL();
            this.trash_items[1].href = "/users/" + this.username + "/courses/";
        },
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
        getCredential(){
            axios.get('/courses/ajax/get_credential/',{params: {}}).then(response => {
                this.credential = response.data.credential;
                this.username = response.data.username;
            }).catch( err => {
                this.credential = "";
                this.username = "";
            });
        },
        getPlannableURL(){
            // var preHref = "localhost:8080"
            var preHref = "https://plannable.gitee.io"
            this.trash_items[3].href = preHref + "/?courses=" + this.plannableURL + "&username=" + this.username + "&credential=" + this.credential + "";
        },
	},
	mounted(){
        this.getCredential();
        this.getTrendingCourses();
        this.getMajorOptions();
        this.getTakingCourses();
        this.getReviewUsers();
	},
  };
</script>

<style>

    .courses-main{
        background-color: #fff;
    }

    .main-title{
        margin-top: 100px;
        margin-bottom: 30px;
        color:#32a49a;
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
        padding: 0px 0px 40px 0px;
        color:#000000;
        width:100%;
        /* height: 100%; */
        position:relative;
        background: url('../assets/static/css/images/cloud_new_09.jpg') no-repeat;
        background-attachment: fixed;
        background-position: center center;
        background-size: cover;

        -webkit-box-shadow: inset 0 -3px 3px 0px rgba(0,0,0,.13), inset 0 -7px 7px 0px rgba(0,0,0,.12);
        box-shadow: inset 0 -3px 3px 0px rgba(0,0,0,.13), inset 0 -7px 7px 0px rgba(0,0,0,.12);
        /* padding: 0; */
    }

    .recommendation-div{
        overflow: scroll;
        max-height: 248px;
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
        .recommendation-div{
            overflow: scroll;
            max-height: 300px;
        }
        
    }

</style>
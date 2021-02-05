<template>
    <div>
        <!-- Side Navigation Drawer -->
        <v-navigation-drawer
            app
            v-model="drawer"
            temporary
            :clipped="$vuetify.breakpoint.mdAndUp">
            <v-container>
                <v-card 
                    color="#FFFFFF"
                    v-if="user">
                    <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title>
                    <v-card-subtitle>Role: {{user.role ? user.role : "None"}}</v-card-subtitle>
                </v-card>
                <v-card
                    v-for="(items, i) in nav_drawer_items"
                    :key="i"
                    style="margin-top:15px;"
                    color="#FFFFFF">
                    <v-list dense>
                        <v-list-item
                            :key="index_item + '-trash' " 
                            v-for="(item, index_item) in items"
                            @click="navMethod(item)">
                            <v-list-item-avatar
                                v-if="item.icon">
                                <v-icon>{{ item.icon }}</v-icon>
                            </v-list-item-avatar>
                            <v-list-item-content>
                                <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-container>
        </v-navigation-drawer>
        <!-- APP BAR -->
        <v-app-bar
            :class="[homepage ? 'homepage-bar' : '']"
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            :dense="!homepage"
            :color="variables.navbar_bg_color"
            absolute
            dark
            :src="homepage ? '/static/css/images/usp_17.jpg' : undefined"
            :height="homepage ? '280px' : undefined "
            >
            <div :class="[homepage ? 'cus-toolbar__content' : 'cus-toolbar__content_2']">
                <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
                <img class="nav-img" :src="brand_pic" width="40" height="38" alt="">
                <template v-if="$vuetify.breakpoint.mdAndUp">
                    <v-btn
                        :href="general_urls.courses_url"
                        text>HoosMyProfessor</v-btn>
                    <!-- <v-divider inset vertical></v-divider> -->
                    <v-btn 
                        :href="general_urls.match_url"
                        text>Match</v-btn>
                    <!-- <v-divider inset vertical></v-divider> -->
                    <!-- <v-btn 
                        :href="general_urls.market_url"
                        text>Market</v-btn> -->
                </template>
                <search-course
                    style="padding-left:6px;"
                    light
                    background_color="white"
                    v-if="searchBool"></search-course>
                <v-spacer></v-spacer>
                <!-- App Menu -->
                <v-menu offset-y
                    class="mx-auto"
                    min-width="170">
                    <template v-slot:activator="{ attrs, on }">
                        <v-btn
                            color="white"
                            icon
                            v-bind="attrs"
                            v-on="on">
                            <v-icon>mdi-apps</v-icon>
                        </v-btn>
                    </template>
                    <v-list dense rounded>
                        <v-list-item
                            v-for="(item, index) in app_items"
                            :key="index + '-app'"
                            @click="navMethod(item)">
                            <v-list-item-icon>
                                <v-icon color="black" dense v-text="item.icon"></v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                                <v-list-item-title>{{ item.title }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-menu>
                <!-- User Drop Menu -->
                <v-menu offset-y
                    class="mx-auto"
                    min-width="170">
                    <template v-slot:activator="{ attrs, on }">
                        <v-btn
                            color="white"
                            icon
                            v-bind="attrs"
                            v-on="on">
                            <v-icon>mdi-account-circle-outline</v-icon>
                        </v-btn>
                    </template>
                    <v-list dense rounded>
                        <v-list-item
                            v-for="(item, index) in user_items"
                            :key="index"
                            @click="navMethod(item)">
                            <v-list-item-icon>
                                <v-icon color="black" dense v-text="item.icon"></v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                                <v-list-item-title>{{ item.title }}</v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </div>
            <template v-if="homepage">
                <div class="header-bottom-div">
                    HOOS MY PROFESSOR
                </div>
                <div class="subheader-bottom-div">
                    Reviews, Ratings & More
                </div>
            </template>
        </v-app-bar>
        <v-snackbar
            top
            v-model="form_invalid_snack"
            color="red lighten-1"
            :timeout="2700">
            Form Invalid
            <template v-slot:action="{ attrs }">
                <v-btn color="white" v-bind="attrs" text @click="form_invalid_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            Sth is wrong
            <template v-slot:action="{ attrs }">
                <v-btn color="white" v-bind="attrs" text @click="failure_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="2700">
            Review Submitted
            <template v-slot:action="{ attrs }">
                <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-dialog v-model="submitReviewDialog" transition="fade-transition" scrollable min-width="350px" max-width="600px">
            <v-card>
                <v-card-title>Submit a Review</v-card-title>
                <v-divider></v-divider>
                <v-card-text style="padding-bottom:0px;">
                    <v-form
                        ref="review_form"
                        v-model="submit_review_form_valid">
                        <v-row>
                            <v-col class="pb-0">
                                <span class="rating-label">Instructor Rating:</span>
                                <v-rating
                                    v-model="review.rating_instructor"
                                    color="yellow darken-3"
                                    background-color="grey darken-1"
                                    medium
                                    hover>
                                </v-rating>
                            </v-col>
                            <v-col class="pb-0">
                                <span class="rating-label">Course Rating:</span>
                                <v-rating
                                    v-model="review.rating_course"
                                    color="yellow darken-3"
                                    background-color="grey darken-1"
                                    medium
                                    hover>
                                </v-rating>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                            <search-course
                                flat
                                light
                                dense
                                searchFunction="select"
                                :searchInstructor="false"
                                background_color="white"
                                :outlined="true"
                                @select-course="selectCourse">
                            </search-course>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-select
                                    v-model="review_instructor_pk"
                                    :items="instructor_options"
                                    item-text="name"
                                    item-value="instructor_pk"
                                    :disabled="review_course_pk==null"
                                    :loading="instructorSelectLoading"
                                    label="Instructor"
                                    :rules="[v => !!v || 'Instructor is required']"
                                    :menu-props="{ offsetY: true }"
                                    outlined
                                    dense
                                    hide-details>
                                </v-select>
                            </v-col>
                            <v-col>
                                <v-select
                                    dense
                                    hide-details
                                    v-model="review.course_instructor_pk"
                                    :items="course_instructor_options"
                                    item-text="semester"
                                    item-value="course_instructor_pk"
                                    :disabled="review_instructor_pk==null"
                                    label="Semester"
                                    :rules="[v => !!v || 'Semester is required']"
                                    :menu-props="{ offsetY: true }"
                                    outlined>
                                </v-select>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col class="pb-0">
                                <v-textarea
                                    v-model="review.text"
                                    label="Write Your Review"
                                    auto-grow
                                    outlined
                                    required
                                    :rules="reviewTextRules"
                                    rows="6"
                                    row-height="20">
                                </v-textarea>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" class="white--text" :loading="submitReviewBtnLoading"  @click.prevent="submitReview(review)">Submit</v-btn>   
                    <v-btn color="red darken-1" class="white--text" @click="submitReviewDialog = false">Close</v-btn> 
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from 'axios'
import SearchCourse from './SearchCourse'
import { general_urls, general_icons, brand_pic } from '../utils'
import variables from '../sass/variables.scss'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default{
    props: {
        homepage:{
            type:Boolean,
            default:false,
        },
        searchBool:{
            type:Boolean,
            default:true,
        },
        headerUpdate:{
            type:Boolean,
            default:false,
        },
    },
    data: function () {
        return {
            variables:variables,
            // Urls
            brand_pic:brand_pic,
            general_urls:general_urls,
            // Review
            submit_review_form_valid:true,
            submitReviewDialog:false,
            submitReviewBtnLoading:false,
            instructorSelectLoading:false,
            reviewTextRules: [
                v => !!v || 'Review is required',
                v => (v && v.length <= 2000) || 'Review must be less than 2000 characters',
            ],
            review_course_pk:null,
            review_course:null,
            review_instructor_pk:null,
            instructors:[],
            instructor_options:[],
            course_instructor_options:[],
            review:{
                rating_course:1,
                rating_instructor:1,
                text:"",
                course_instructor_pk:null,
            },
            // Snacks
            form_invalid_snack:false,
            failure_snack:false,
            success_snack:false,

            loaded:false,
            navDrawer:false,
            user:null,
            drawer: null,
            plannableURL:"https://plannable.org/?auth=Hoosmyprofessor",
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
            ],
            user_items:[
                { title:"Profile", icon:general_icons.profile },
                { title:"Edit Profile", icon:general_icons.edit_profile},
                { title:"My Courses", icon:general_icons.my_courses },
                { title:"My Reviews", icon:general_icons.my_reviews },
                { title:"Log Out", icon:general_icons.logout},
            ],
            app_items:[
                { title:"Match", icon:general_icons.match },
                { title:"Market", icon:general_icons.market },
                { title:"Live Comments", icon:general_icons.live_comments },
            ],
            urls:{
                profile:"",
                update_profile:"",
            },
            nav_drawer_items:[
                [{
                    "title":"My Courses",
                    "icon":general_icons.my_courses,
                },
                {
                    "title":"My Reviews",
                    "icon":general_icons.my_reviews,
                },
                {
                    "title":"Submit a Review",
                    "icon":general_icons.submit_review,
                },],
                [{
                    "title":"Home",
                    "icon":general_icons.home,
                },
                {
                    "title":"Departments",
                    "icon":general_icons.departments,
                },
                {
                    "title":"Plannable",
                    "icon":general_icons.plannable,
                },]
            ],
        }
    },
    components:{
        SearchCourse,
    },
    watch:{
        review_instructor_pk(val){
            this.course_instructor_options = this.instructors[val];
        },
        review_course_pk(){
            this.instructorSelectLoading = true;
            this.getCourse();
        },
        headerUpdate(){
            this.getTakingCourses();
        },
    },
    methods:{
        selectCourse(course){
            this.review_course_pk = course.value;
        },
        submitReview(review){
            this.$refs.review_form.validate();
            if(!this.submit_review_form_valid){
                this.form_invalid_snack = true;
                return;
            }
            this.submitReviewBtnLoading = true;
            axios.post('/courses/api/submit_review/', {
                "text":review.text,
                "rating_course":review.rating_course,
                "rating_instructor":review.rating_instructor,
                "course_instructor_pk":review.course_instructor_pk,
            }).then(response => {
                this.submitReviewBtnLoading = false;
                if(response.data.success){
                    this.success_snack = true;
                    this.review = {
                        rating_course:1,
                        rating_instructor:1,
                        text:"",
                        course_instructor_pk:null,
                    }
                    this.$refs.review_form.reset()
                    this.$emit("submit-review")
                }
                else{
                    this.failure_snack = true;
                }
                this.submitReviewDialog = false;
            });
        },
        getCourse(){
            axios.get('/courses/api/get_course/',{params: {pk:this.review_course_pk, }}).then(response => {
                this.review_course = response.data.course;
                this.instructors = {};
                this.instructor_options = [];
                for(let i = 0; i < this.review_course.instructors.length; i++){
                    this.instructor_options.push({
                        "instructor_pk":this.review_course.instructors[i].pk,
                        "name":this.review_course.instructors[i].name
                    });
                    this.instructors[this.review_course.instructors[i].pk] = []
                    for(let j = 0; j < this.review_course.instructors[i].semesters.length; j++){
                        this.instructors[this.review_course.instructors[i].pk].push({
                            "semester":this.review_course.instructors[i].semesters[j].semester,
                            "course_instructor_pk":this.review_course.instructors[i].semesters[j].course_instructor_pk,
                        });
                    }
                }
                this.instructor_options.sort(function(a,b){
                    let nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase();
                    if (nameA < nameB) return -1;
                    if (nameA > nameB) return 1;
                    return 0;
                })
                this.instructorSelectLoading = false;
            });
        },
        navAsideMethod(item){
            if(item.text == "HoosMyProfessor"){
                this.goToHref(this.general_urls.courses_url);
            }
            else if(item.text == "Match"){
                this.goToHref(this.general_urls.match_url);
            }
        },
        openSubmitReviewDialog(){
            this.submitReviewDialog = true;
        },
        navMethod(item){
            if(item.title=="Profile"){
                this.goToHref(this.urls.profile);
            }
            else if(item.title=="Edit Profile"){
                this.goToHref(this.urls.update_profile);
            }
            else if(item.title=="My Courses"){
                this.goToHref(this.general_urls.my_courses_url);
            }
            else if(item.title=="My Reviews"){
                this.goToHref(this.general_urls.review_url);
            }
            else if(item.title=="Log Out"){
                this.goToHref(this.general_urls.logout_url);
            }
            else if(item.title=="Match"){
                this.goToHref(this.general_urls.match_url);
            }
            else if(item.title=="Market"){
                this.goToHref(this.general_urls.market_url);
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.general_urls.comment_url);
            }
            else if(item.title=="Home"){
                this.goToHref("/courses/");
            }
            else if(item.title=="Departments"){
                this.goToHref(this.general_urls.department_url);
            }
            else if(item.title=="Plannable"){
                this.goToHref(this.plannableURL);
            }
            else if(item.title=="Submit a Review"){
                this.submitReviewDialog = true;
            }
        },
        get_basic_info(){
            axios.get('/courses/api/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
                this.user = response.data.user;
                this.loaded = true;
            });
        },
        goToHref(text){
            window.location.href = text;
        },
    },
    mounted(){
        this.get_basic_info();
    },
}
</script>


<style lang="css">
    .header-bottom-div{
        width: 100%;
        position: absolute;
        top: 120px;
        font-size: 36px;
        font-weight: 300;
        font-family: "Roboto", sans-serif;
        letter-spacing: 0.06em;
        text-align: center;
        color: white;
    }

    .subheader-bottom-div{
        width: 100%;
        position: absolute;
        top: 175px;
        font-size: 25px;
        font-weight: 300;
        font-family: "Roboto", sans-serif;
        letter-spacing: 0.06em;
        text-align: center;
        color: white;
    }

    .cus-toolbar__content{
        width: 100%;
        display: flex;
        position: fixed;
        align-items: center;
        padding: 10px 0px 0px 0px;
    }

    .cus-toolbar__content_2{
        width: 100%;
        display: flex;
        position: fixed;
        align-items: center;
    }

    .homepage-bar .v-toolbar__content{
        align-items: normal !important;
    }

    .v-toolbar__content{
        padding: 0px !important;
    }

    .rating-label{
        padding-left: 9px;
        font-size: 15px;
    }

    .nav-img{
        margin-left:6px;
    }

    @media (min-width: 10px) and (max-width: 767px) {
        .nav-img{
            margin-left:0px;
        }

        .header-bottom-div{
            font-size: 27px;
        }

        .subheader-bottom-div{
            top: 167px;
            font-size: 18px;
        }
    }

    .cus-navbar-item{
        font-size: 15px !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }

</style>
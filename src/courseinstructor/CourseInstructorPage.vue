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
            <v-layout mt-2> <!-- Mnemonic and Number -->
                <v-flex class="cus-headline-flex"> 
                    <div>
                    <span class="cus-headline-number">{{course.mnemonic}}{{course.number}}</span>
                    <span class="cus-headline-text">{{course.title}}</span>
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout> <!-- Instructor Name -->
                <v-flex>
                    <div class="instructor-name">
                        {{instructor.name}}
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout> <!-- Course Description -->
                <v-flex d-flex>
                    <v-card>
                        <v-card-title>Prerequisite</v-card-title>
                        <v-card-text v-if="course.prerequisite">{{course.prerequisite.substring(13).trim()}}</v-card-text>
                        <v-card-text v-else>No prereq is specified for this course(Please check on SIS)</v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
            <v-layout row wrap> <!-- Prereq and Rate -->
                <v-flex lg8 md6 sm12 xs12 d-flex>
                    <v-card>
                        <v-card-title>Description</v-card-title>
                        <v-card-text>{{course.description}}</v-card-text>
                    </v-card>
                </v-flex>
                <v-flex lg4 md6 sm12 xs12 d-flex>
                    <v-card>
                        <v-card-title>Rating</v-card-title>
                        <v-card-text>
                            <v-flex class="rating-div">
                                <span>Instructor: {{instructor.rating_instructor}}</span>
                                <v-rating
                                    v-model="instructor.rating_instructor"
                                    color="yellow darken-3"
                                    background-color="grey darken-1"
                                    readonly
                                    medium
                                    hover>
                                </v-rating>
                            </v-flex>
                            <v-flex class="rating-div">
                                <span>Course: {{course.rating_course}}</span>
                                <v-rating
                                    v-model="course.rating_course"
                                    color="yellow darken-3"
                                    background-color="grey darken-1"
                                    readonly
                                    medium
                                    hover>
                                </v-rating>
                            </v-flex>
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
            <v-layout row wrap> <!-- Users Taking -->
                <v-flex d-flex>
                    <v-card>
                        <v-card-title>Users Taking {{course.mnemonic}} {{course.number}}</v-card-title>
                        <v-card-text v-if="users_taking.length > 0">
                            <v-chip 
                            v-for="(user_taking, index) in users_taking"
                            :key="index" 
                            :href=" '/users/'+user_taking.user_pk+'/' ">
                                <v-icon left color="black">mdi-account</v-icon>
                                {{ user_taking.name }}
                            </v-chip>
                        </v-card-text>
                        <v-card-text v-else>
                            No user is taking this class
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
            <v-layout>
                <v-flex>
                    <v-card>
                        <v-card-title>Users who have Taken {{course.mnemonic}} {{course.number}}</v-card-title>
                        <v-card-text v-if="users_taken.length > 0">
                            <v-chip 
                            v-for="(user_taken, index) in users_taken"
                            :key="index" 
                            :href=" '/users/'+user_taken.user_pk+'/' "
                            >
                                <v-icon left color="black">mdi-account</v-icon>
                                {{ user_taken.name }}
                            </v-chip>
                        </v-card-text>
                        <v-card-text v-else>
                            No user has taken this class
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
            <v-layout> <!-- Review Div Title -->
                <v-flex align-self-center class="instructor-name">
                        <span class="review-title">Reviews</span>
                        <v-btn @click="reviewDialog = true;" color="teal darken-3" fab large dark>
                            <v-icon>edit</v-icon>
                        </v-btn>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout row wrap>  <!-- Reviews -->
                <v-flex d-flex :key="user.user_pk" v-for="user in users_with_review">
                    <v-card>
                        <v-card-text>
                            <div class="review-text">
                                {{user.text}}
                            </div>
                        </v-card-text>
                        <v-card-actions>
                            <v-layout>
                                <v-spacer></v-spacer>
                            <div>
                                <v-chip
                                    class="ma-1" color="teal lighten-2" label small text-color="white">
                                    {{user.semester}}
                                </v-chip>
                                <v-chip
                                    class="ma-1" color="teal lighten-2" label small text-color="white">
                                    Course: {{user.rating_course}}
                                </v-chip>
                                <v-chip
                                    class="ma-1" color="teal lighten-2" label small text-color="white">
                                    Instructor: {{user.rating_instructor}}
                                </v-chip>
                            </div>
                            </v-layout>
                        </v-card-actions>
                    </v-card>
                </v-flex>
                <v-flex v-if="users_with_review.length == 0">
                    <v-card>
                        <v-card-text>
                            There is no review for this course.
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>
    <v-dialog v-model="reviewDialog" persistent max-width="600px">
        <v-card>
            <v-card-title>
                <span class="headline">Submit a Review</span>
            </v-card-title>
            <v-card-text>
                <v-container grid-list-md>
                    <v-layout wrap>
                        <v-flex>
                            <span>Instructor Rating:</span>
                            <v-rating
                                v-model="review_rating_instructor"
                                color="yellow darken-3"
                                background-color="grey darken-1"
                                medium
                                hover>
                            </v-rating>
                            <span>Course Rating:</span>
                            <v-rating
                                v-model="review_rating_course"
                                color="yellow darken-3"
                                background-color="grey darken-1"
                                medium
                                hover>
                            </v-rating>
                        </v-flex>
                        <v-flex d-flex>
                            <v-select
                                v-model="review_course_instructor_pk"
                                :items="course_instructors"
                                item-text="semester"
                                item-value="course_instructor_pk"
                                label="Semester"
                                :menu-props="{ offsetY: true }"
                                outlined>
                            </v-select>
                        </v-flex>
                    </v-layout>
                    <v-layout>
                        <v-flex>
                            <v-textarea
                                v-model="review_text"
                                label="Write Your Review"
                                auto-grow
                                outlined
                                rows="5"
                                row-height="20"
                            ></v-textarea>
                        </v-flex>
                    </v-layout>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="reviewDialog = false">Close</v-btn>
                <v-btn color="blue darken-1" text @click="submitReview()">Submit</v-btn>
            </v-card-actions>
        </v-card>
      </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
    data() {
      return {
        currentSemester:"2019Fall",
        selected_course:null,
        courseNameLimit:40,
        isLoading: false,
        entries:[],
        search: null,
        home_url:"",
        brand_pic:"",
        profile:"",
        update_profile:"",
        logout:"",
        navItems:[],
        course:{
            "course_pk":"",
            "mnemonic":"",
            "number":"",
            "title":"",
            "description":"",
            "prerequisite":"",
            "type":"",
            "rating_instructor":null,
            "rating_course":null,
        },
        course_instructors:[],
        course_users:[],
        semester:"",
        topic:"",
        instructor:{
            "name":"",
            "rating_instructor":"",
        },

        reviewDialog:false,
        review_rating_course:0,
        review_rating_instructor:0,
        review_text:"",
        review_course_instructor_pk:null,

        drawer: null,
        source: "/lessons/",
        user_items:[
            { title:"Profile", icon:"fas fa-user" },
            { title:"Edit Profile", icon:"fas fa-biohazard" },
            { title:"Log Out", icon:"fas fa-angry"},
        ],
        old_items: [
        //   {  icon: 'contacts', text: 'Contacts' },
        //   { icon: 'history', text: 'Frequently contacted' },
        //   { icon: 'content_copy', text: 'Duplicates' },
        //   {
        //     icon: 'keyboard_arrow_up',
        //     'icon-alt': 'keyboard_arrow_down',
        //     text: 'Labels',
        //     model: true,
        //     children: [
        //       { icon: 'add', text: 'Create label' }
        //     ]
        //   },
        //   {
        //     icon: 'keyboard_arrow_up',
        //     'icon-alt': 'keyboard_arrow_down',
        //     text: 'More',
        //     model: false,
        //     children: [
        //       { text: 'Import' },
        //       { text: 'Export' },
        //       { text: 'Print' },
        //       { text: 'Undo changes' },
        //       { text: 'Other contacts' }
        //     ]
        //   },
          { icon: 'settings', text: 'Settings' },
          { icon: 'chat_bubble', text: 'Send feedback' },
          { icon: 'help', text: 'Help' },
        ],
      }
    },
    components:{
        CustomHeader,
    },
    watch: {
      selected_course(val){
        if(val != null){
          this.goToHref("/courses/" + val.value + "/");
        }
      },
      search (val) {
        // Items have already been loaded
        if (val == null || val.length == 0){
          this.entries = []
          return
        }
        if (val.length < 2) return

        // Items have already been requested
        if (this.isLoading) return

        this.isLoading = true

        // Lazily load input items
        axios.get('/courses/ajax/course_search_result/',{params: {query:val, }}).then(response => {
                this.entries = response.data.course_result; 
          })
          .catch(err => {
            console.log("error: ",err)
          })
          .finally(() => {this.isLoading = false})
          ;
      },
    },
    computed:{
        users_with_review(){
            return this.course_users.filter(obj => {
                return obj.text.length > 0;
            })
        },
        users_taking(){
            return this.course_users.filter(obj => {
                return obj.take=="taking";
            })
        },
        users_taken(){
            return this.course_users.filter(obj => {
                return obj.take=="taken";
            })
        },
        teaching_instructors(){
            return this.course.instructors.filter(obj => {
                return obj.semesters.indexOf(this.currentSemester) != -1;
            })
        },
        not_teaching_instructors(){
            return this.course.instructors.filter(obj => {
                return obj.semesters.indexOf(this.currentSemester) == -1;
            })
        },
        items(){
            return this.entries.map(entry => {
            let tmp_course_name = entry.mnemonic + entry.number + " " + entry.title;
            const course_name = tmp_course_name.length > this.courseNameLimit
                ? tmp_course_name.slice(0, this.courseNameLimit) + '...'
                : tmp_course_name;

            return {text:course_name, value:entry.pk, take:entry.take};
            })
        },
        course_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 3];
        },
        instructor_pk:function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
    },
    methods: {
        submitReview(){
            axios.post('/courses/ajax/submit_review/', {
                "text":this.review_text,
                "rating_course":this.review_rating_course,
                "rating_instructor":this.review_rating_instructor,
                "course_pk":this.course_pk,
                "instructor_pk":this.instructor_pk,
                "course_instructor_pk":this.review_course_instructor_pk,
            }).then(response => {
                if(response.data.success){
                    this.$message({
                        message: 'Review Submitted',
                        type: 'success'
                    });
                    this.getCourseInstructor();
                }
            });
            this.reviewDialog = false;
        },
        getCourseInstructor(){
            axios.get('/courses/ajax/get_course_instructor/',{params: {course_pk:this.course_pk, instructor_pk:this.instructor_pk, }}).then(response => {
                let data = response.data;
                this.course = data.course;
                document.title = this.course.mnemonic + this.course.number;
                this.course_instructors = data.course_instructors;
                this.instructor = data.instructor;
                this.course_users = data.course_users;
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
                        disabled: false,
                        href: '/courses/'+this.course.course_pk + "/",
                    },
                    {
                        text: this.instructor.name,
                        disabled: true,
                        href: "NONE",
                    },
                ];
          });
        },
        goToHref(text){
            window.location.href = text;
        },
        getAutoComplete(query){
          axios.get('/courses/ajax/course_search_result/',{params: {query:query, }}).then(response => {
                this.allFmls = response.data.groups; 
          });
        },
    },
    mounted(){
        this.getCourseInstructor();
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

    .review-text{
        color:rgb(0, 0, 0);
        font-size: 16px;
        font-family: "Roboto", sans-serif;
    }

    .review-rating{
        color:rgb(141, 141, 141);
        font-size: 15px;
        margin-right: 10px;
    }

    .review-title{
        margin: 0px 12px 0px 0px;
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
        margin: 0px 0px 4px 0px;
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

    @media (min-width: 1281px) { 
        
    }

    @media (min-width: 1025px) and (max-width: 1280px) {
        
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
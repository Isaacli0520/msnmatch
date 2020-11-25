<template>
  <v-app>
    <custom-header @submit-review="getCourseInstructor"></custom-header>
    <v-main>
        <v-container v-if="!loaded" fluid fill-height>
            <v-layout 
                align-center
                justify-center>
                <div class="text-center">
                    <v-progress-circular
                    :size="60"
                    :width="6"
                    indeterminate
                    color="teal lighten-1">
                    </v-progress-circular>
                </div>
            </v-layout>
        </v-container>
        <v-container v-if="loaded" fluid grid-list-lg>
            <v-layout>
                <v-flex>
                    <custom-breadcrumb :items="navItems"></custom-breadcrumb>
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
                        <v-btn color="teal darken-1" outlined x-large :href="' /courses/instructors/' + instructor.instructor_pk + '/' ">
                            <v-icon class="instructor-icon" color="black" medium left>fas fa-user-tie</v-icon>{{instructor.name}}
                        </v-btn>
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <!-- <v-layout>
                <v-flex child-flex d-flex>
                    <v-card>
                        <v-card-title>Prerequisite</v-card-title>
                        <v-card-text v-if="course.prerequisite">{{course.prerequisite.substring(13).trim()}}</v-card-text>
                        <v-card-text v-else>No prereq is specified for this course(Please check on SIS)</v-card-text>
                    </v-card>
                </v-flex>
            </v-layout> -->
            <v-layout wrap> <!-- Prereq and Rate -->
                <v-flex xl7 lg7 md6 sm12 xs12 d-flex child-flex>
                    <v-card>
                        <v-card-title>Description</v-card-title>
                        <v-card-text>{{course.description}}</v-card-text>
                    </v-card>
                </v-flex>
                <v-flex xl5 lg5 md6 sm12 xs12 d-flex child-flex>
                    <custom-rating
                        :rating="instructor.rating_instructor"
                        :counter="instructor.rating_instructor_counter"
                        :actiontext="instructor.rating_instructor_users_count + ' users have reviewed this instructor' ">
                    </custom-rating>
                </v-flex>
            </v-layout>
            <v-layout> <!-- Users Taking -->
                <v-flex>
                    <v-card>
                        <v-card-title>Users Planning on Taking {{course.mnemonic}} {{course.number}}</v-card-title>
                        <v-card-text v-if="users_taking.length > 0">
                            <v-chip 
                            color="teal darken-1"
                            text-color="white"
                            class="ma-1"
                            v-for="(user_taking, index) in users_taking"
                            :key="index + '-taking-user'  " 
                            :href=" '/users/'+user_taking.username+'/' ">
                                <v-icon left color="white">account_circle</v-icon>
                                {{ user_taking.name }}
                            </v-chip>
                        </v-card-text>
                        <v-card-text v-else>
                            No user is planning on taking this class
                        </v-card-text>
                    </v-card>
                </v-flex>
            </v-layout>
            <v-layout v-if="taken_users_enable">
                <v-flex>
                    <v-card>
                        <v-card-title>Users Who Have Taken {{course.mnemonic}} {{course.number}}</v-card-title>
                        <v-card-text v-if="users_taken.length > 0">
                            <v-chip 
                            color="teal darken-1"
                            text-color="white"
                            class="ma-1"
                            v-for="(user_taken, index) in users_taken"
                            :key="index +'-taken-user' " 
                            :href=" '/users/'+user_taken.username+'/' "
                            >
                                <v-icon left color="white">account_circle</v-icon>
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
                <v-flex justify-center align-self-center class="instructor-name">
                        <span class="review-title">Reviews</span>
                        <v-btn @click="reviewDialog = true;" color="teal darken-3" fab large dark>
                            <v-icon>edit</v-icon>
                        </v-btn>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <v-layout row wrap>  <!-- Reviews -->
                <v-flex :key="user.course_user_pk + '-review' " v-for="user in users_with_review">
                    <v-card>
                        <v-card-text>
                            <div class="review-text">
                                {{user.text}}
                            </div>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-row>
                                <v-spacer></v-spacer>
                                <v-chip
                                    class="ma-1" color="#336699" outlined small text-color="#336699">
                                    {{user.semester}}
                                </v-chip>
                                <v-chip
                                    class="ma-1" color="teal darken-2" outlined small text-color="teal darken-2">
                                    <span style="margin-top:2px;" class="caption mr-1">Instructor:</span>
                                    <v-rating
                                        v-model="user.rating_instructor"
                                        color="yellow darken-2"
                                        background-color="teal darken-2"
                                        readonly
                                        dense
                                        small
                                        half-increments>
                                    </v-rating>
                                </v-chip>
                                <v-chip
                                    class="ma-1 mr-3" color="teal darken-2" outlined small text-color="teal darken-2">
                                    <span style="margin-top:2px;" class="caption mr-1">Course:</span>
                                    <v-rating
                                        v-model="user.rating_course"
                                        color="yellow darken-2"
                                        background-color="teal darken-2"
                                        readonly
                                        dense
                                        small
                                        half-increments>
                                    </v-rating>
                                </v-chip>
                            </v-row>
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
    </v-main>
    <v-dialog v-model="reviewDialog" max-width="600px">
        <v-card>
            <v-card-title>
                <span class="headline">Submit a Review</span>
            </v-card-title>
            <v-card-text>
                <v-form
                    ref="review_form"
                    v-model="submit_review_form_valid">
                    <v-row wrap>
                        <v-col>
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
                        </v-col>
                        <v-col>
                            <v-select
                                v-model="review_course_instructor_pk"
                                :items="course_instructors"
                                item-text="text"
                                item-value="course_instructor_pk"
                                :rules="[v => !!v || 'Semester is required']"
                                label="Semester"
                                :menu-props="{ offsetY: true }"
                                outlined>
                            </v-select>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-textarea
                                v-model="review_text"
                                label="Write Your Review"
                                auto-grow
                                outlined
                                :rules="reviewTextRules"
                                rows="5"
                                row-height="20"
                            ></v-textarea>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="teal darken-1" outlined v-if="course_instructors.length > 0" :loading="submitReviewBtnLoading" @click="submitReview()">Submit</v-btn>
                <v-btn color="red lighten-1" outlined @click="reviewDialog = false">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
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
        v-model="success_snack"
        color="teal darken-1"
        :timeout="2700">
        Review Submitted
        <template v-slot:action="{ attrs }">
        <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
        </template>
    </v-snackbar>
    </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'
import CustomRating from '../components/CustomRating'
import CustomBreadcrumb from '../components/CustomBreadcrumb'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    data() {
        return {
            loaded:false,
            submitReviewBtnLoading:false,
            submit_review_form_valid:true,
            // Snacks
            failure_snack:false,
            success_snack:false,
            form_invalid_snack:false,

            reviewTextRules:[
                v => !!v || 'Review is required',
                v => (v && v.length <= 2000) || 'Review must be less than 2000 characters',
            ],

            taken_users_enable:false,
            currentSemester:"",
            courseNameLimit:40,
            isLoading: false,
            entries:[],
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
            review_rating_course:1,
            review_rating_instructor:1,
            review_text:"",
            review_course_instructor_pk:null,

            drawer: null,
        }
    },
    components:{
        CustomHeader,
        CustomRating,
        CustomBreadcrumb,
    },
    watch:{
    },
    computed:{
        users_with_review(){
            return this.course_users.filter(obj => {
                return obj.text.length > 0;
            })
        },
        users_taking(){
            var duplicate_keys = []
            var ret_users_taking = []
            for(let i = 0; i < this.course_users.length; i++){
                if(this.course_users[i].take=="taking" && duplicate_keys.indexOf(this.course_users[i].user_pk) == -1){
                    duplicate_keys.push(this.course_users[i].user_pk);
                    ret_users_taking.push(this.course_users[i]);
                }
            }
            return ret_users_taking
            // return this.course_users.filter(obj => {
            //     return obj.take=="taking";
            // })
        },
        users_taken(){
            var duplicate_keys = []
            var ret_users_taken = []
            for(let i = 0; i < this.course_users.length; i++){
                if(this.course_users[i].take=="taken" && duplicate_keys.indexOf(this.course_users[i].user_pk) == -1){
                    duplicate_keys.push(this.course_users[i].user_pk);
                    ret_users_taken.push(this.course_users[i]);
                }
                
            }
            return ret_users_taken;
            // return this.course_users.filter(obj => {
            //     return obj.take=="taken";
            // })
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
        getCurrentSemester(){
            axios.get('/courses/ajax/get_current_semester/',{params: {pk:this.course_pk, }}).then(response => {
                this.currentSemester = response.data.year + response.data.semester;
                this.getCourseInstructor();
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
        sortBySemesterKey(a,b){
            return this.sortBySemester(a["semester"], b["semester"]);
        },
        submitReview(){
            this.$refs.review_form.validate();
            if(!this.submit_review_form_valid){
                this.form_invalid_snack = true;
                return;
            }
            this.submitReviewBtnLoading = true;
            axios.post('/courses/api/submit_review/', {
                "text":this.review_text,
                "rating_course":this.review_rating_course,
                "rating_instructor":this.review_rating_instructor,
                "course_instructor_pk":this.review_course_instructor_pk,
            }).then(response => {
                this.submitReviewBtnLoading = false;
                if(response.data.success){
                    this.getCourseInstructor();
                    this.success_snack = true;
                    this.$refs.review_form.reset()
                }
                else{
                    this.failure_snack = true;
                }
                this.reviewDialog = false;
            });
        },
        getCourseInstructor(){
            axios.get('/courses/api/get_course_instructor/',{params: {course_pk:this.course_pk, instructor_pk:this.instructor_pk, }}).then(response => {
                let data = response.data;
                var tmp_cs_instr = [];
                this.course = data.course;
                document.title = this.course.mnemonic + this.course.number;
                this.course_instructors = data.course_instructors;
                this.course_instructors = this.course_instructors.sort(this.sortBySemesterKey);
                for(let i = 0; i < this.course_instructors.length; i++){
                    if(this.course_instructors[i].semester != this.currentSemester){
                        tmp_cs_instr.push({
                            "course_instructor_pk":this.course_instructors[i].course_instructor_pk,
                            "text":this.course_instructors[i].semester + " " + this.course_instructors[i].topic,
                            });
                    }
                }
                this.course_instructors = tmp_cs_instr;
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
        word-wrap:break-word;
        white-space: pre-line;
    }

    .review-rating{
        color:rgb(141, 141, 141);
        font-size: 15px;
        margin-right: 10px;
    }

    .review-title{
        margin: 0px 12px 0px 0px;
    }

    .instructor-icon{
        padding-right: 5px;
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
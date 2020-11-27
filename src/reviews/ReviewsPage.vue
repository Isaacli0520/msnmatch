<template>
    <v-app>
        <custom-header @submit-review="getReviews"></custom-header>
        <v-main>
            <v-container fluid grid-list-lg>
                <v-row dense>
                    <v-col>
                        <custom-breadcrumb :items="navItems"></custom-breadcrumb>
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col>
                        <span class="cus-headline-text">My Reviews</span>
                    </v-col>
                </v-row>
                <v-row v-if="!reviews_load">
                    <v-col>
                        <div class="text-center">
                            <v-progress-circular
                            :size="60"
                            :width="6"
                            indeterminate
                            color="teal lighten-1">
                            </v-progress-circular>
                        </div>
                    </v-col>
                </v-row>
                <template v-else>
                    <v-row v-if=" reviews_load && reviews.length > 0">
                        <v-col
                            cols=12 sm=12 md=6 lg=6 xl=4
                            :key="index_review + '-review' " 
                            v-for="(review, index_review) in reviews">
                            <review-card @edit-review="editReview" :review="review" :editable="true"></review-card>
                        </v-col>
                    </v-row>
                    <v-row v-else>
                        <v-col>
                            <span class="grey--text" >You have no reviews :(</span>
                        </v-col>
                    </v-row>
                </template>
            </v-container>
        </v-main>
        <v-dialog v-model="reviewDialog" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline">Edit Your Review</span>
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
                                    :loading="cs_instr_load"
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
                    <v-btn color="red darken-1" outlined @click="deleteDialog = true">Delete</v-btn>
                    <v-btn color="teal darken-1" :loading="submitReviewBtnLoading" outlined @click="submitReview()">Submit</v-btn>
                    <v-btn color="blue darken-1" outlined @click="reviewDialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="deleteDialog" persistent max-width="400px">
            <v-card>
                <v-card-title>
                    <span class="headline">Confirmation</span>
                </v-card-title>
                <v-card-text>
                    <span>Do you really want to DELETE this review?</span>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="teal darken-1" outlined @click="deleteReview()">Yes</v-btn>
                    <v-btn color="red lighten-1" outlined @click="deleteDialog = false">No</v-btn>
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
            Invalid Form
            <template v-slot:action="{ attrs }">
                <v-btn color="white" v-bind="attrs" text @click="form_invalid_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="2700">
            {{success_text}}
            <template v-slot:action="{ attrs }">
                <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
            </template>
        </v-snackbar>
    </v-app>
</template>

<script>
import axios from 'axios'
import { CustomHeader, CustomBreadcrumb, ReviewCard } from '../components'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
    data() {
        return {
            // Page Basics
            currentSemester:"",
            navItems:[],
            reviews:[],
            // Snacks
            success_text:"",
            failure_snack:false,
            success_snack:false,
            form_invalid_snack:false,
            // Review Dialog
            submit_review_form_valid:true,
            submitReviewBtnLoading:false,
            reviewDialog:false,
            deleteDialog:false,
            review_text:"",
            review_rating_instructor:0,
            review_rating_course:0,
            review_course_instructor_pk:"",
            review_course_pk:"",
            review_instructor_pk:"",
            course_instructors:[],
            reviewTextRules:[
                v => !!v || 'Review is required',
                v => (v && v.length <= 2000) || 'Review must be less than 2000 characters',
            ],
            cs_instr_load:false,
            reviews_load:false,
        }
    },
    components:{
      CustomHeader,
      CustomBreadcrumb,
      ReviewCard,
    },
    watch: {
    },
    computed:{
    },
    methods: {
        getCurrentSemester(){
            axios.get('/courses/ajax/get_current_semester/',{params: {}}).then(response => {
                this.currentSemester = response.data.year + response.data.semester;
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
        goToHref(text){
            window.location.href = text;
        },
        getReviews(){
            this.reviews_load = false;
            axios.get('/courses/ajax/get_reviews/',{params: {}}).then(response => {
                this.reviews = response.data.reviews;
                this.reviews_load = true;
            });
        },
        getCourseInstructors(course_pk, instructor_pk){
            this.cs_instr_load = true;
            var tmp_cs_instr = [];
            axios.get('/courses/api/get_course_instructors/',{params: {course_pk:course_pk, instructor_pk:instructor_pk}}).then(response => {
                this.course_instructors = response.data.course_instructors.sort(this.sortBySemesterKey);
                for(let i = 0; i < this.course_instructors.length; i++){
                    if(this.course_instructors[i].semester != this.currentSemester){
                        tmp_cs_instr.push({
                            "course_instructor_pk":this.course_instructors[i].course_instructor_pk,
                            "text":this.course_instructors[i].semester + " " + this.course_instructors[i].topic,
                            });
                    }
                }
                this.course_instructors = tmp_cs_instr;
                this.cs_instr_load = false;
            });
        },
        editReview(review){
            this.getCourseInstructors(review.course.pk, review.instructor.pk);
            this.reviewDialog = true;
            this.review_text = review.text;
            this.review_rating_instructor = review.rating_instructor;
            this.review_rating_course = review.rating_course;
            this.review_course_instructor_pk = review.course_instructor_pk;
            this.review_course_pk = review.course.pk;
            this.review_instructor_pk = review.instructor.pk;
        },
        deleteReview(){
            axios.post("/courses/ajax/save_take/",{
                    "course_pk":this.review_course_pk,
                    "instructor_pk":this.review_instructor_pk,
                    "course_instructor_pk":this.review_course_instructor_pk,
                    "semester":"", 
                    "take":"",
                    "delete":true
                }).then(response => {
                if(response.data.success){
                    this.success_text = "Review Deleted";
                    this.success_snack = true;
                    this.getReviews();
                }else{
                    this.failure_snack = true;
                }
            });
            this.deleteDialog = false,
            this.reviewDialog = false;
        },
        submitReview(){
            this.$refs.review_form.validate();
            if(!this.submit_review_form_valid){
                this.form_invalid_snack = true;
                return;
            }
            this.submitReviewBtnLoading = true;
            axios.post("/courses/api/submit_review/", {
                "text":this.review_text,
                "rating_course":this.review_rating_course,
                "rating_instructor":this.review_rating_instructor,
                "course_instructor_pk":this.review_course_instructor_pk,
            }).then(response => {
                this.submitReviewBtnLoading = false;
                if(response.data.success){
                    this.success_text = "Review Edited";
                    this.success_snack = true;
                    this.getReviews();
                    this.$refs.review_form.reset()
                }
                else{
                    this.failure_snack = true;
                }
                this.reviewDialog = false;
            });
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
                text: "My Reviews",
                disabled: true,
                href: '',
            },
        ];
        this.getCurrentSemester();
        this.getReviews();
    },
  };
</script>

<style scoped>

    .review-headline-number{
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 500;
        background-color: rgb(13, 124, 109);
        color:#fff;
        padding: 1px 7px 1px 7px;
        border-radius: 5px 0px 0px 5px;
        line-height: 1.4;
        box-decoration-break: clone;
    }

    .review-headline-text{
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 300;
        background-color: rgb(240, 240, 240);
        color:rgb(0, 0, 0);
        padding: 1px 7px 1px 7px;
        border-radius: 0px 5px 5px 0px;
        line-height: 1.4;
        box-decoration-break: clone;

    }

    .review-text{
        font-size: 16px;
        color: black;
        font-family: "Roboto", sans-serif;
        word-wrap:break-word;
        white-space: pre-line;
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
        padding: 1px 12px 7px 3px;
        border-radius: 5px;
        line-height: 1.0;
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
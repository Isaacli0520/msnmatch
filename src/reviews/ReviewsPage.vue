<template>
    <v-app>
        <custom-header></custom-header>
        <v-content>
            <v-container fluid grid-list-lg>
                <v-layout>
                    <v-flex>
                        <custom-breadcrumb :items="navItems"></custom-breadcrumb>
                    </v-flex>
                </v-layout>
                <v-layout mb-3>
                    <v-flex> 
                        <div>
                            <span class="cus-headline-text">My Reviews</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-container v-if="!reviews_load" fluid fill-height>
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
                <v-layout v-if="reviews_load" wrap>
                    <v-flex d-flex child-flex xs12 sm12 md12 lg12 xl12>
                        <v-layout row wrap v-if="reviews.length > 0">
                            <v-flex 
                                child-flex d-flex
                                xs12 sm12 md6 lg6 xl6
                                :key="index_review + '-review' " 
                                v-for="(review, index_review) in reviews">
                                <v-card>
                                    <v-card-title>
                                        <div class="review-title-text">
                                            <span>{{review.course.mnemonic}} {{review.course.number}}</span>
                                            <span class="grey--text">  {{review.course.title}}</span>
                                        </div>
                                    </v-card-title>
                                    <v-divider></v-divider>
                                    <v-card-text>
                                        <div class="review-text">
                                            {{review.text}}
                                        </div>
                                    </v-card-text>
                                    <v-card-actions style="padding:4px !important;">
                                        <v-layout style="margin:2px !important;">
                                            <v-spacer></v-spacer>
                                        <div>
                                            <v-chip
                                                class="ma-1" color="teal lighten-2" label small text-color="white">
                                                {{review.semester}}
                                            </v-chip>
                                            <v-chip
                                                class="ma-1" color="teal lighten-2" label small text-color="white">
                                                Course: {{ review.rating_course ? review.rating_course : 'N/A' }}
                                            </v-chip>
                                            <v-chip
                                                class="ma-1" color="teal lighten-2" label small text-color="white">
                                                Instructor: {{review.rating_instructor ? review.rating_instructor : 'N/A'}}
                                            </v-chip>

                                            <v-chip
                                                class="ma-1"
                                                outlined
                                                color="red"
                                                @click="editReview(review)"
                                                label 
                                                small>
                                                Edit
                                            </v-chip>
                                        </div>
                                        </v-layout>
                                    </v-card-actions>
                                </v-card>
                            </v-flex>
                        </v-layout>
                        <span v-else>You have no reviews.</span>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
        <v-dialog v-model="reviewDialog" persistent max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline">Edit Your Review</span>
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
                                    :loading="cs_instr_load"
                                    item-text="text"
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
import CustomBreadcrumb from '../components/CustomBreadcrumb'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
	    return {
            currentSemester:"",
            reviewDialog:false,
            navItems:[],
            reviews:[],
            review_text:"",
            review_rating_instructor:0,
            review_rating_course:0,
            review_course_instructor_pk:"",
            review_course_pk:"",
            review_instructor_pk:"",
            course_instructors:[],
            cs_instr_load:false,
            reviews_load:false,
	    }
	},
	components:{
      CustomHeader,
      CustomBreadcrumb,
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
            axios.get('/courses/ajax/get_course_instructors/',{params: {course_pk:course_pk, instructor_pk:instructor_pk}}).then(response => {
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
            this.getCourseInstructors(review.course.course_pk, review.instructor_pk);
            this.reviewDialog = true;
            this.review_text = review.text;
            this.review_rating_instructor = review.rating_instructor;
            this.review_rating_course = review.rating_course;
            this.review_course_instructor_pk = review.course_instructor_pk;
            this.review_course_pk = review.course.course_pk;
            this.review_instructor_pk = review.instructor_pk;
        },
        submitReview(){
            axios.post('/courses/ajax/submit_review/', {
                "text":this.review_text,
                "rating_course":this.review_rating_course,
                "rating_instructor":this.review_rating_instructor,
                "course_pk":this.review_course_pk,
                "instructor_pk":this.review_instructor_pk,
                "course_instructor_pk":this.review_course_instructor_pk,
            }).then(response => {
                if(response.data.success){
                    this.$message({
                        message: 'Review Submitted',
                        type: 'success'
                    });
                    this.getReviews();
                }
                else{
                    this.$message({
                        message: 'Sth is wrong baby~',
                        type: 'error'
                    });
                }
            });
            this.reviewDialog = false;
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

<style>
    .review-title-text{
        font-size: 20px;
    }

    .review-text{
        font-size: 17px;
        color: black;
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
<template>
    <div>
        <!-- Side Navigation Drawer -->
        <v-navigation-drawer
            app
            floating
            hide-overlay
            v-model="drawer"
            :clipped="$vuetify.breakpoint.mdAndUp">
            <v-container v-if="!loaded || user == null" fluid fill-height>
                <v-layout 
                    align-center
                    justify-center>
                    <div>
                        <v-progress-circular
                        :size="60"
                        :width="6"
                        indeterminate
                        color="teal lighten-1">
                        </v-progress-circular>
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="loaded && user">
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
            :clipped-left="$vuetify.breakpoint.mdAndUp"
            app
            dense
            light
            elevation="1">
            <v-app-bar-nav-icon  @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-img max-height="38" max-width="38" :src="urls.brand_pic" alt=""></v-img>
            <v-toolbar-items v-if="$vuetify.breakpoint.mdAndUp">
                <v-btn 
                    :href="urls.courses_url"
                    text>HoosMyProfessor</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.match_url"
                    text>Match</v-btn>
                <v-divider inset vertical></v-divider>
                <v-btn 
                    :href="urls.market_url"
                    text>Market</v-btn>
            </v-toolbar-items>
            <search-course
                v-if="searchBool"></search-course>
            <v-spacer v-if="!searchBool"></v-spacer>
            <!-- App Menu -->
            <v-menu offset-y
                class="mx-auto"
                min-width="170">
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
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
                            <v-icon dense v-text="item.icon"></v-icon>
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
                <template v-slot:activator="{ on }">
                    <v-btn
                        icon
                        v-on="on">
                        <v-icon>fas fa-user-circle</v-icon>
                    </v-btn>
                </template>
                <v-list dense rounded>
                    <v-list-item
                        v-for="(item, index) in user_items"
                        :key="index"
                        @click="navMethod(item)">
                        <v-list-item-icon>
                            <v-icon dense v-text="item.icon"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>{{ item.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-app-bar>
        <v-snackbar
            top
            v-model="form_invalid_snack"
            color="red lighten-1"
            :timeout="2700">
            Form Invalid
            <v-btn color="white" text @click="form_invalid_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red lighten-1"
            :timeout="2700">
            Sth is wrong
            <v-btn color="white" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="success_snack"
            color="teal darken-1"
            :timeout="2700">
            Review Submitted
            <v-btn color="cyan accent-1" text @click="success_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-dialog v-model="submitReviewDialog" scrollable min-width="350px" max-width="600px">
            <v-card>
                <v-card-title>Submit a Review</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                    <v-form
                        ref="review_form"
                        v-model="submit_review_form_valid">
                        <v-row>
                            <v-col>
                            <span>Instructor Rating:</span>
                            <v-rating
                                v-model="review.rating_instructor"
                                color="yellow darken-3"
                                background-color="grey darken-1"
                                medium
                                hover>
                            </v-rating>
                            </v-col>
                            <v-col>
                            <span>Course Rating:</span>
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
                                searchFunction="select"
                                :searchInstructor="false"
                                :flat="true"
                                :light="true"
                                background_color="white"
                                :dense="true"
                                @select-course="selectCourse"
                                :outlined="true">
                            </search-course>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-select
                                    dense
                                    v-model="review_instructor_pk"
                                    :items="instructor_options"
                                    item-text="name"
                                    item-value="instructor_pk"
                                    :disabled="review_course_pk==null"
                                    :loading="instructorSelectLoading"
                                    label="Instructor"
                                    :rules="[v => !!v || 'Instructor is required']"
                                    :menu-props="{ offsetY: true }"
                                    outlined>
                                </v-select>
                            </v-col>
                            <v-col>
                                <v-select
                                    dense
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
                            <v-col>
                                <v-textarea
                                    v-model="review.text"
                                    label="Write Your Review"
                                    auto-grow
                                    outlined
                                    required
                                    :rules="reviewTextRules"
                                    rows="5"
                                    row-height="20">
                                </v-textarea>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="green darken-1" :loading="submitReviewBtnLoading" outlined @click.prevent="submitReview(review)">Create</v-btn>   
                    <v-btn color="blue darken-1" outlined @click="submitReviewDialog = false">Close</v-btn> 
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from 'axios'
import SearchCourse from './SearchCourse'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default{
    props: {
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
            credential:"",
            plannableURL:"",
            username:"",
            taking_courses:[],
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
                { title:"Profile", icon:"fas fa-user" },
                { title:"Edit Profile", icon:"fas fa-user-edit" },
                { title:"My Courses", icon:"fas fa-list-ol" },
                { title:"Log Out", icon:"fas fa-sign-out-alt"},
            ],
            app_items:[
                { title:"Match", icon:"fas fa-user-friends" },
                { title:"Market", icon:"fas fa-search-dollar" },
                { title:"Live Comments", icon:"fas fa-comment" },
            ],
            urls:{
                home_url:"",
                brand_pic:"",
                profile:"",
                update_profile:"",
                logout:"",
                my_courses:"",
                courses_url:"",
                match_url:"",
                comment_url:"",
                market_url:"",
                skills_url:"",
            },
            nav_drawer_items:[
                [{
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
                    "title":"Submit a Review",
                    "icon":"fas fa-pen",
                    "href":"",
                    "target":"",
                },],
                [{
                    "title":"Home",
                    "icon":"fas fa-home",
                    "href":"/courses/",
                    "target":"",
                },
                {
                    "title":"Departments",
                    "icon":"fas fa-list-ol",
                    "href":"/courses/departments/",
                    "target":"",
                },
                {
                    "title":"Plannable",
                    "icon":"fas fa-paper-plane",
                    "href":"https://plannable.org",
                    "target":"_blank",
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
        taking_courses(val){
            var tmp_arr = [];
            for(let i = 0; i < val.length; i++){
                tmp_arr.push(val[i].mnemonic.toLowerCase() + val[i].number+this.courseTypes.indexOf(val[i].type).toString(10))
            }
            this.plannableURL = JSON.stringify(tmp_arr);
        },
    },
    computed:{
        plannableFinalURL(){
            return "https://plannable.org" + "/?courses=" + this.plannableURL + "&username=" + this.username + "&credential=" + this.credential + "";
        }
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
            axios.get('/courses/ajax/get_course/',{params: {pk:this.review_course_pk, }}).then(response => {
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
                this.instructorSelectLoading = false;
            });
        },
        sortCourseNumber(a, b){
            return a.number.toString(10) - b.number.toString(10);
        },
        navAsideMethod(item){
            if(item.text == "HoosMyProfessor"){
                this.goToHref(this.urls.courses_url);
            }
            else if(item.text == "Match"){
                this.goToHref(this.urls.match_url);
            }
        },
        navMethod(item){
            if(item.title=="Profile"){
                this.goToHref(this.urls.profile);
            }
            else if(item.title=="Edit Profile"){
                this.goToHref(this.urls.update_profile);
            }
            else if(item.title=="Log Out"){
                this.goToHref(this.urls.logout);
            }
            else if(item.title=="My Courses"){
                this.goToHref(this.urls.my_courses);
            }
            else if(item.title=="My Reviews"){
                this.goToHref("/courses/reviews/");
            }
            else if(item.title=="Match"){
                this.goToHref(this.urls.match_url);
            }
            else if(item.title=="Market"){
                this.goToHref(this.urls.market_url);
            }
            else if(item.title=="Live Comments"){
                this.goToHref(this.urls.comment_url);
            }
            else if(item.title=="Home"){
                this.goToHref("/courses/");
            }
            else if(item.title=="Departments"){
                this.goToHref("/courses/departments/");
            }
            else if(item.title=="Plannable"){
                this.goToHref(this.plannableFinalURL);
            }
            else if(item.title=="Submit a Review"){
                this.submitReviewDialog = true;
            }
        },
        get_basic_info(){
            axios.get('/courses/ajax/get_basic_info/',{params: {}}).then(response => {
                this.urls = response.data.all_info;
                this.loaded = true;
            });
        },
        goToHref(text){
            window.location.href = text;
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
        getTakingCourses(){
            axios.get('/courses/api/get_user_hmp_header/',{params: {}}).then(response => {
                this.user = response.data.user;
                this.taking_courses = response.data.taking_courses;
            });
        },
    },
    mounted(){
        this.getCredential();
        this.get_basic_info();
        this.getTakingCourses();
    },
}
</script>


<style scoped lang="css">
    .cus-navbar-item{
        font-size: 15px !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    .theme--light.v-app-bar.v-toolbar.v-sheet{
        background-color: white !important;
    }

    .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot .v-label, .theme--light.v-text-field--solo-inverted.v-text-field--solo.v-input--is-focused > .v-input__control > .v-input__slot input {
        color: #000000 !important;
    }

</style>
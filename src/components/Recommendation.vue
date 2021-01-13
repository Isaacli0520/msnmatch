<template>
    <v-dialog 
        :value="value" 
        @input="$emit('input')"
        scrollable 
        transition="fade-transition"
        min-width="330px"
        max-width="700px">
        <v-card
            outlined
            elevation="3"
            :loading="!recommendation_loaded">
            <v-card-title>Recommendations</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-row>
                    <v-col cols="6" md="4">
                        <v-select
                            v-model="year"
                            :items="year_options"
                            label="Year"
                            hide-details
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-col>
                    <v-col cols="6" md="4">
                        <v-select
                            v-model="semester"
                            :items="semester_options"
                            label="Semester"
                            hide-details
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-col>
                    <v-col cols="12" md="4">
                        <v-select
                            v-model="major"
                            :items="major_options"
                            label="Major"
                            hide-details
                            :menu-props="{ offsetY: true }"
                            outlined>
                        </v-select>
                    </v-col>
                </v-row>
                    <div class="recommendation-div" v-if="recommendation_loaded">
                        <v-row dense v-if="rcm_courses.length>0">
                            <v-col 
                                cols="12"
                                :key="index_course + '-rcm-course' " 
                                v-for="(course, index_course) in rcm_courses">
                                <v-card hover :href="'/courses/'+ course.course_pk + '/' ">
                                    <v-card-title style="padding:10px;clear:both;display:block;">
                                        <span class="course-number">{{course.mnemonic}}{{course.number}}</span>
                                        <span class="course-title">{{course.title}}</span>
                                        <span class="course-taken">Taken: {{course.taken}}</span>
                                    </v-card-title>
                                </v-card>
                            </v-col>
                        </v-row>
                        <div v-else>
                            Recommendations are not available for this setting.
                        </div>
                    </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn class="white--text" color="blue darken-1" @click.native="$emit('input')">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios'

export default{
    props:{
        value:{
            type:Boolean,
            default:false,
        },
    },
    data() {
        return {
            init_finished:false,
            user_info_get:false,
            recommendation_loaded:false,
            year:1,
            semester:"",
            major:null,
            major_options:[],
            year_options:[
                {"text":"1","value":1,},
                {"text":"2","value":2,},
                {"text":"3","value":3,},
                {"text":"4","value":4,},
            ],
            semester_options:[
                {"text":"Fall","value":"Fall",},
                {"text":"Spring","value":"Spring",},
            ],
            rcm_courses:[],
        }
    },
    watch: {
        value(val){
            if(val && !this.init_finished){
                this.getCurrentSemester();
                this.getMajorOptions();
                this.init_finished = true;
            }
        },
        year(){
            if(this.user_info_get){
                this.recommendation_loaded = false;
                this.getRecommendations();
            }
        },
        semester(){
            if(this.user_info_get){
                this.recommendation_loaded = false;
                this.getRecommendations();
            }
        },
        major(){
            if(this.user_info_get){
                this.recommendation_loaded = false;
                this.getRecommendations();
            }
        },
    },
    methods:{
        getCurrentSemester(){
            axios.get('/courses/api/get_current_semester/',{params: { }}).then(response => {
                this.semester = response.data.semester;
            });
        },
        getRecommendations(){
            axios.get('/courses/api/get_recommendations/',{params: {year:this.year, semester:this.semester, major:this.major}}).then(response => {
                this.rcm_courses = response.data.rcm_courses;
                this.recommendation_loaded = true;
                this.user_info_get = true;
            });
        },
        getMajorOptions(){
            axios.get('/courses/api/get_major_options/',{params: {}}).then(response => {
                this.major_options = response.data.major_options;
                this.major = response.data.major == "" ? this.major_options[0].value : response.data.major;
                this.semester = response.data.semester == "" ? this.semester_options[0].value : response.data.semester;
                this.year = response.data.year == 0 ? this.year_options[0].value : response.data.year;
                this.getRecommendations();
            });
        },
    },
    mounted(){
        
    },
}

</script>


<style scoped lang="css">
    .course-number{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color:#ffffff;
        padding: 3px 5px;
        margin-right: 5px;
        border-radius: 4px;
        line-height: 1.3;
        font-size: 18px;
        background-color: #00796b;
    }

    .course-title{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.3;
        font-size: 18px;
    }

    .course-taken{
        float: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.3;
        font-size: 14px;
        color:#ffffff;
        padding: 6px 7px;
        margin-right: 5px;
        border-radius: 4px;
        background-color: #ff5c1b;
    }

    @media (min-width: 10px) and (max-width: 767px) {
        .course-number{
            font-size: 16px;
        }

        .course-title{
            font-size: 16px;
        }

        .course-taken{
            font-size: 12px;
        }
    }
</style>
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
            <v-container fluid grid-list-lg>
                <v-layout mb-3>
                    <v-flex> 
                        <div>
                            <span class="cus-headline-text">Hoosmyprofessor</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-layout fill-height wrap>
                    <v-flex child-flex d-flex xs12 sm12 md4 lg4 xl4>
                        <v-card>
                            <v-card-title>Trash Can</v-card-title>
                            <v-card-text>
                                <v-layout row wrap>
                                    <v-flex
                                        style="width:100%;"
                                        :key="index_item + '-trash' " 
                                        v-for="(item, index_item) in trash_items">
                                        <v-list-item
                                            :href="item.href">
                                            <v-list-item-avatar
                                                v-if="item.icon">
                                                <v-icon>{{ item.icon }}</v-icon>
                                            </v-list-item-avatar>
                                            <v-list-item-content>
                                                <v-list-item-title>{{ item.title }}</v-list-item-title>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-flex>
                                </v-layout>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                    <template v-for="i in ['Taking', 'Taken']">
                        <v-flex child-flex d-flex :key="i + '-taking-taken' " xs12 sm6 md4 lg4 xl4>
                            <v-card>
                                <v-card-title>Top 10 {{i}} Courses</v-card-title>
                                <v-card-text>
                                    <v-layout row wrap>
                                        <v-flex
                                            style="width:100%;"
                                            :key="index_course + '-trending-course' " 
                                            v-for="(course, index_course) in trending_courses[i]">
                                            <v-list-item
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
                                        </v-flex>
                                    </v-layout>
                                </v-card-text>
                            </v-card>
                        </v-flex>
                    </template>
                    <v-flex d-flex child-flex xs12 sm12 md12 lg12 xl12>
                        <v-card min-height="65vh">
                            <v-card-title>Recommendations</v-card-title>
                            <v-card-text>
                                <v-layout row wrap>
                                    <v-flex d-flex>
                                        <v-select
                                            v-model="year"
                                            :items="year_options"
                                            label="Year"
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                    <v-flex d-flex>
                                        <v-select
                                            v-model="semester"
                                            :items="semester_options"
                                            label="Semester"
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                    <v-flex d-flex>
                                        <v-select
                                            v-model="major"
                                            :items="major_options"
                                            label="Major"
                                            :menu-props="{ offsetY: true }"
                                            outlined>
                                        </v-select>
                                    </v-flex>
                                </v-layout>
                                <v-layout row wrap>
                                    <v-flex
                                        style="width:100%;"
                                        :key="index_course + '-rcm-course' " 
                                        v-for="(course, index_course) in rcm_courses">
                                        <v-list-item
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
                                    </v-flex>
                                </v-layout>
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
            year:1,
            semester:"Fall",
            major:null,
            major_options:[],
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
                },
                {
                    "title":"My Courses",
                    "icon":"fas fa-user-circle",
                    "href":"/users/",
                },
                {
                    "title":"Go to Plannable",
                    "icon":"fas fa-paper-plane",
                    "href":"https://plannable.gitee.io",
                },
                {
                    "title":"Home Page",
                    "icon":"fas fa-home",
                    "href":"/",
                },
            ],
            colors: [
                'primary',
                'secondary',
                'yellow darken-2',
                'red',
                'orange',
            ],
	    }
	},
	components:{
	  CustomHeader,
	},
	watch: {
        year:function(){
            this.getRecommendations();
        },
        semester:function(){
            this.getRecommendations();
        },
        major:function(){
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
            });
        },
        getRecommendations(){
            axios.get('/courses/ajax/get_recommendations/',{params: {year:this.year, semester:this.semester, major:this.major}}).then(response => {
                this.rcm_courses = response.data.rcm_courses;
            });
        },
        getMajorOptions(){
            axios.get('/courses/ajax/get_major_options/',{params: {}}).then(response => {
                this.major_options = response.data.major_options;
                if(response.data.major == ""){
                    this.major = this.major_options[0].value;
                }
                else{
                    this.major = response.data.major;
                }
                this.getRecommendations();
            });
        }
	},
	mounted(){
        this.getTrendingCourses();
        this.getMajorOptions();
	},
  };
</script>

<style>

	.cus-headline-text{
		font-family: "Roboto", sans-serif;
		font-size: 2.1em;
		font-weight: 300;
		color:rgb(0, 0, 0);
		padding: 7px 12px 7px 12px;
		border-radius: 5px;
		line-height: 2.0;
	}

	

</style>
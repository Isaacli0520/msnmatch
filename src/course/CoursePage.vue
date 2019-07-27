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
            <v-layout mb-1>
                <v-flex class="cus-headline-flex"> 
                    <div>
                    <span class="cus-headline-number">{{course.mnemonic}}{{course.number}}</span>
                    <span class="cus-headline-text">{{course.title}}</span>
                    </div>
                </v-flex>
                <v-spacer></v-spacer>
            </v-layout>
            <template v-for="i in 2">
                <v-layout :key="i" mt-2 mb-3>
                    <v-flex> 
                        <div v-if="i==1" class="instructor-banner">Instructors teaching this semester</div>
                        <div v-if="i==2" class="instructor-banner">Past semesters</div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-layout :key="i + 100000" row wrap>
                    <v-flex d-flex 
                    :key="index_instr"
                    v-for="(instructor, index_instr) in i == 1 ? teaching_instructors : not_teaching_instructors">
                    <v-card
                    >
                        <v-card-text>
                            <v-flex align-self-center class="mb-2">
                                <span class="instructor-name">{{ instructor.name }}</span>
                                <v-chip 
                                    v-if="course.take.instructor_pk == instructor.pk"
                                    label
                                    text-color="white"
                                    color="teal darken-3"
                                    class="ma-1">
                                    {{course.take.take}}
                                </v-chip>
                            </v-flex>
                            <v-spacer></v-spacer>
                            <span v-if="instructor.topic.length>0" class="grey--text subtitle-1">Topic: {{ instructor.topic }}</span>
                            <div>
                                <div>
                                    <span class="text--primary">Semesters taught: {{instructor.semesters.length}}</span>
                                </div>
                                <div>
                                    <!-- <template v-if="instructor.rating_instructor>0"> -->
                                    <span class="text--primary">Rating: </span>
                                    <v-rating
                                        v-model="instructor.rating_instructor"
                                        color="yellow darken-3"
                                        background-color="grey darken-1"
                                        readonly
                                        small
                                        >
                                    </v-rating>
                                    <!-- </template> -->
                                </div>
                            </div>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn
                            text
                            color="deep-purple accent-4"
                            @click="goToHref('/courses/'+course.course_pk+'/'+instructor.pk+'/')"
                            >
                            Learn More
                            </v-btn>
                            <v-btn
                                @click="openDialogTake(instructor)"
                                color="deep-purple accent-4" 
                                text
                                >
                                Taking/Taken
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                    </v-flex>
                </v-layout>
            </template>
        </v-container>
        <v-dialog v-model="dialogTake" scrollable min-width="350px" max-width="500px">
            <v-card>
                <v-card-title>Select Semester</v-card-title>
                <v-divider></v-divider>
                <v-card-text style="height: 300px;">
                    <v-checkbox 
                        v-model="takeCourse" 
                        :key="item.value.instructor_pk + item.value.semester" 
                        v-for="item in takeItemsComputed" 
                        :value-comparator="takeCompare" 
                        :label="item.label" 
                        :value="item.value"
                        color="black"
                        ></v-checkbox>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="dialogTake = false">Close</v-btn>
                    <v-btn color="blue darken-1" text @click="takeSave()">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-content>
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
        course:{
            "course_pk": 0,
            "mnemonic": "",
            "number": "",
            "title": "",
            "category":"",
            "take": {
                "instructor":"",
                "semester":"",
                "take":"",
            },
            "department":{
                "name":"",
                "department_pk":"",
            },
            "instructors":[],
        },
        currentSemester:"2019Fall",

        navItems:[],

        takeCourse:null,
        takeItems:[],
        takeItemKey:"", 
        dialogTake: false,
        source: "/lessons/",
        
      }
    },
    components:{
        CustomHeader,
    },
    watch: {
      
    },
    computed:{
        takeItemsComputed(){
            return this.takeItems.filter(obj => {
                return obj.value.instructor_pk == this.takeItemKey;
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
        course_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
        course_edit_url: function(){
            return '/courses/' + this.course_pk + '/edit/';
        },
    },
    methods: {
        takeCompare(a,b){
            if (a == null || b == null){
                return false;
            }
            return (a.course_pk == b.course_pk && a.instructor_pk == b.instructor_pk && a.semester == b.semester && a.take == b.take);

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
        openDialogTake(instructor){
            this.takeItemKey = instructor.pk;
            this.dialogTake = true;
        },
        takeSave(){
            if(this.takeCourse != null){
                var params = {
                    'course_pk':this.takeCourse.course_pk,
                    'instructor_pk':this.takeCourse.instructor_pk,
                    'semester':this.takeCourse.semester, 
                    'take':this.takeCourse.take,
                    'delete':false,
                }
            }
            else{
                var params = {
                    'course_pk':this.course.course_pk,
                    'instructor_pk':"",
                    'semester':"", 
                    'take':"",
                    'delete':true,
                }
            }
            axios.post('/courses/ajax/save_take/',
            params,).then(response => {
                if(response.data.success){
                    this.$message({
                        message: 'Updated',
                        type: 'success'
                    });
                }
                this.getCourse();
                // if(!params.delete){
                //     this.takeCourse.instructor_pk = response.data.now.instructor_pk;
                //     this.takeCourse.semester = response.data.now.semester;
                //     this.takeCourse.take = response.data.now.take;
                //     this.course.take.instructor_pk = response.data.now.instructor_pk;
                //     this.course.take.semester = response.data.now.semester;
                //     this.course.take.take = response.data.now.take;
                // }
                // else{
                //     this.course.take = {
                //         "instructor_pk":"",
                //         "course_pk":"",
                //         "semester":"",
                //         "take":"",
                //     }
                // }
            });
            this.dialogTake = false;
        },
        getCourse(){
            axios.get('/courses/ajax/get_course/',{params: {pk:this.course_pk, }}).then(response => {
                this.course = response.data.course;
                document.title = this.course.mnemonic + this.course.number;
                this.takeItems = [];
                for(let i = 0; i < this.course.instructors.length; i++){
                    this.course.instructors[i].semesters = this.course.instructors[i].semesters.sort(this.sortBySemester);
                    for(let j = 0; j < this.course.instructors[i].semesters.length; j++){
                        var tmp_label = " Taken"
                        var tmp_take = "taken"
                        if(this.course.instructors[i].semesters.indexOf(this.currentSemester) != -1){
                            tmp_label = (j == 0 ? " Currently Taking" : " Taken");
                            tmp_take = (j == 0 ? "taking" : "taken")
                        }
                        this.takeItems.push({
                            "label":this.course.instructors[i].semesters[j] + tmp_label,
                            "value":{
                                "semester":this.course.instructors[i].semesters[j],
                                "instructor_pk":this.course.instructors[i].pk,
                                "course_pk":this.course.course_pk,
                                "take": tmp_take,
                            }
                        });
                    }
                }

                for(let k = 0; k < this.takeItems.length; k++){
                    if(this.takeItems[k].value.instructor_pk == this.course.take.instructor_pk && this.takeItems[k].value.semester == this.course.take.semester){
                        this.takeCourse = this.takeItems[k].value;
                    }
                }

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
                        disabled: true,
                        href: '/courses/'+this.course.course_pk + "/",
                    },
                ];
                
          });
        },
        goToHref(text){
            window.location.href = text;
        },
    },
    mounted(){
        this.getCourse();
    },
  };
</script>

<style>
    .instructor-name{
        font-family: "Roboto", sans-serif;
        font-size: 1.6em;
        font-weight: 500;
    }

    .v-breadcrumbs li{
        font-size:20px !important;
    }

    .cus-breadcrumbs{
        padding-left: 4px !important;
    }

    .taking{
        background-color: rgb(11, 105, 92);
        padding: 5px 6px 6px 6px;
        color:#fff;
        border-radius: 5px;
        margin: 0px 0px 0px 6px;
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 500;
    }

    .taken{
        background-color: rgb(40, 123, 247);
        padding: 5px 6px 6px 6px;
        color:#fff;
        border-radius: 5px;
        margin: 0px 0px 0px 6px;
        font-family: "Roboto", sans-serif;
        font-size: 1.3em;
        font-weight: 500;
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

    .instructor-banner{
        font-family: "Roboto", sans-serif;
        font-size: 1.6em;
        font-weight: 500;
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

        .instructor-banner{
            font-size: 1.3em;
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
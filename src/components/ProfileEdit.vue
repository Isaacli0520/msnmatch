<template>
    <div>
        <v-layout 
            style="min-height:300px;"
            v-if="!loaded"
            align-center
            justify-center>
            <div v-if="!loaded">
                <v-progress-circular
                :size="60"
                :width="6"
                indeterminate
                color="teal lighten-1">
                </v-progress-circular>
            </div>
        </v-layout>
        <v-card v-if="edit_user && loaded">
            <v-card-title>Edit Your Profile</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-form
                    method="post"
                    ref="edit_form"
                    v-model="edit_user_form_valid">

                    <v-text-field
                        v-model="edit_user.first_name"
                        :rules="firstnameRules"
                        label="First Name*"
                        required
                        ></v-text-field>

                    <v-text-field
                        v-model="edit_user.last_name"
                        :rules="lastnameRules"
                        label="Last Name*"
                        required
                        ></v-text-field>

                    <v-text-field
                        v-model="edit_user.location"
                        :rules="locationRules"
                        label="Location"
                        ></v-text-field>

                    <v-select
                        v-model="edit_user.sex"
                        :items="genders"
                        label="Gender"
                        ></v-select>

                    <v-select
                        v-model="edit_user.graduate_year"
                        :items="graduate_years"
                        :rules="[v => !!v || 'Graduate Year is required']"
                        label="Graduate Year*"
                        required
                        ></v-select>

                    <v-select
                        v-model="edit_user.major"
                        :items="majors"
                        :rules="[v => !!v || 'Major is required (or intended major)']"
                        label="Major*"
                        required
                        ></v-select>

                    <v-select
                        v-model="edit_user.major_two"
                        :items="majors"
                        label="Second Major"
                        ></v-select>

                    <v-select
                        v-model="edit_user.minor"
                        :items="minors"
                        label="Minor"
                        ></v-select>

                    <!-- <v-text-field
                    v-model="edit_user.wechat"
                    :rules="wechatRules"
                    label="WeChat ID"
                    ></v-text-field> -->

                    <div class="mb-3">
                        Your Bio allows you to convey more and different information about yourself 
                        than tags and pictures. So please spend more time writing it and let others
                        know you better.
                    </div>

                    <v-textarea
                        v-model="edit_user.bio"
                        label="Bio*"
                        outlined
                        :rules="bioRules"
                        required
                        :counter="3000"
                        rows="10"
                        row-height="20"
                        ></v-textarea>

                    <v-file-input 
                        v-model="edit_user_image"
                        outlined 
                        dense
                        accept="image/*"
                        label="Upload an image"
                        ></v-file-input>

                    <v-file-input 
                        v-model="edit_user_video"
                        outlined
                        dense
                        accept="video/mp4,video/x-m4v,video/*"
                        label="Upload a video"
                        ></v-file-input>

                    <!-- <div style="font-size: 1.25rem;
                        font-weight: 500;
                        color:rgb(0,0,0,1);
                        letter-spacing: 0.0125em;
                        line-height: 2rem;
                        padding:0px 0px 5px 0px">
                        For Roommate Match
                    </div>
                    <v-textarea
                        v-model="edit_user.rm_bio"
                        label="Roommate Bio"
                        outlined
                        :rules="rmBioRules"
                        required
                        :counter="1000"
                        rows="3"
                        row-height="20"
                        />

                    <v-textarea
                        v-model="edit_user.rm_schedule"
                        label="找室友之作息安排"
                        outlined
                        :rules="rmBioRules"
                        required
                        :counter="1000"
                        rows="3"
                        row-height="20"
                        /> -->
                </v-form>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" outlined :disabled="!submitBtnEnable" :loading="editUserBtnLoading" @click.prevent="editUser(edit_user, edit_user_image, edit_user_video)">{{editBtnName}}</v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    props: {
        editBtnName:{
            type:String,
            default:"Edit",
        },
        username:{
            type:String,
            default:"",
        },
    },
    data() {
        return {
            loaded:false,
            submitBtnEnable: true,
            edit_user:null,
            editUserBtnLoading:false,
            edit_user_form_valid:false,
            edit_user_image:null,
            edit_user_video:null,
            firstnameRules: [
                v => !!v || 'First Name is required',
                v => (v && v.length <= 30) || 'First Name must be less than 30 characters',
            ],
            lastnameRules: [
                v => !!v || 'Last Name is required',
                v => (v && v.length <= 150) || 'Last Name must be less than 150 characters',
            ],
            bioRules: [
                v => !!v || 'Bio is required',
                v => (v && v.length <= 3000) || 'Bio must be less than 3000 characters',
            ],
            locationRules: [
                v => (!v || (v && v.length <= 30)) || 'Location must be less than 30 characters',
            ],
            wechatRules: [
                v => (!v || (v && v.length <= 255)) || 'WeChat ID must be less than 255 characters',
            ],
            rmBioRules: [
                v => (!v ||(v && v.length <= 1000)) || 'Must be less than 1000 characters',
            ],
            graduate_years:[    
                {'value':'2018', 'text':'2018'},
                {'value':'2019', 'text':'2019'},
                {'value':'2020', 'text':'2020'},
                {'value':'2021', 'text':'2021'},
                {'value':'2022', 'text':'2022'},
                {'value':'2023', 'text':'2023'},
                {'value':'2024', 'text':'2024'},
                {'value':'2025', 'text':'2025'},
                {'value':'2026', 'text':'2026'},
                {'value':'2027', 'text':'2027'},
            ],
            genders:[
                {'value':'Female', 'text':'Female'},
                {'value':'Male', 'text':'Male'},
                {'value':'Other', 'text':'Other'},
            ],
            majors: [
                {'value':'', 'text':'None'},
                {"values":"Aerospace Engineering", "text":"Aerospace Engineering"},
                {"values":"African American and African Studies", "text":"African American and African Studies"},
                {"values":"American Studies", "text":"American Studies"},
                {"values":"Anthropology", "text":"Anthropology"},
                {"values":"Archaeology", "text":"Archaeology"},
                {"values":"Architectural History", "text":"Architectural History"},
                {"values":"Architecture", "text":"Architecture"},
                {"values":"Astronomy", "text":"Astronomy"},
                {"values":"Bachelor of Interdisciplinary Studies", "text":"Bachelor of Interdisciplinary Studies"},
                {"values":"Bachelor of Professional Studies in Health Sciences Management", "text":"Bachelor of Professional Studies in Health Sciences Management"},
                {"values":"Biology", "text":"Biology"},
                {"values":"Biomedical Engineering", "text":"Biomedical Engineering"},
                {"values":"Chemical Engineering", "text":"Chemical Engineering"},
                {"values":"Chemistry", "text":"Chemistry"},
                {"values":"Civil Engineering", "text":"Civil Engineering"},
                {"values":"Classics", "text":"Classics"},
                {"values":"Cognitive Science", "text":"Cognitive Science"},
                {"values":"Commerce", "text":"Commerce"},
                {"values":"Common First Year in the School of Architecture", "text":"Common First Year in the School of Architecture"},
                {"values":"Comparative Literature", "text":"Comparative Literature"},
                {"values":"Computer Engineering", "text":"Computer Engineering"},
                {"values":"Computer Science", "text":"Computer Science"},
                {"values":"Dance", "text":"Dance"},
                {"values":"Drama", "text":"Drama"},
                {"values":"Early Childhood Education (BSEd)", "text":"Early Childhood Education (BSEd)"},
                {"values":"East Asian Languages, Literatures and Culture", "text":"East Asian Languages, Literatures and Culture"},
                {"values":"Economics", "text":"Economics"},
                {"values":"Electrical Engineering", "text":"Electrical Engineering"},
                {"values":"Elementary Education (BSEd)", "text":"Elementary Education (BSEd)"},
                {"values":"Engineering Science", "text":"Engineering Science"},
                {"values":"English", "text":"English"},
                {"values":"Environmental Sciences", "text":"Environmental Sciences"},
                {"values":"Environmental Thought and Practice", "text":"Environmental Thought and Practice"},
                {"values":"Five-Year Teacher Education Program", "text":"Five-Year Teacher Education Program"},
                {"values":"French", "text":"French"},
                {"values":"German", "text":"German"},
                {"values":"German Studies", "text":"German Studies"},
                {"values":"Global Studies", "text":"Global Studies"},
                {"values":"Global Sustainability Minor", "text":"Global Sustainability Minor"},
                {"values":"Historic Preservation Minor", "text":"Historic Preservation Minor"},
                {"values":"History", "text":"History"},
                {"values":"History of Art", "text":"History of Art"},
                {"values":"Human Biology", "text":"Human Biology"},
                {"values":"Interdisciplinary Major in Computer Science", "text":"Interdisciplinary Major in Computer Science"},
                {"values":"Interdisciplinary Major of Global Studies", "text":"Interdisciplinary Major of Global Studies"},
                {"values":"Jewish Studies", "text":"Jewish Studies"},
                {"values":"Kinesiology (BSEd)", "text":"Kinesiology (BSEd)"},
                {"values":"Landscape Architecture Minor", "text":"Landscape Architecture Minor"},
                {"values":"Latin American Studies", "text":"Latin American Studies"},
                {"values":"Linguistics", "text":"Linguistics"},
                {"values":"Materials Science and Engineering", "text":"Materials Science and Engineering"},
                {"values":"Mathematics", "text":"Mathematics"},
                {"values":"Mechanical Engineering", "text":"Mechanical Engineering"},
                {"values":"Media Studies", "text":"Media Studies"},
                {"values":"Medieval Studies", "text":"Medieval Studies"},
                {"values":"Middle Eastern and South Asian Languages and Cultures", "text":"Middle Eastern and South Asian Languages and Cultures"},
                {"values":"Music", "text":"Music"},
                {"values":"Neuroscience", "text":"Neuroscience"},
                {"values":"Nursing", "text":"Nursing"},
                {"values":"Philosophy", "text":"Philosophy"},
                {"values":"Physics", "text":"Physics"},
                {"values":"Political and Social Thought", "text":"Political and Social Thought"},
                {"values":"Political Philosophy, Policy, and Law", "text":"Political Philosophy, Policy, and Law"},
                {"values":"Politics", "text":"Politics"},
                {"values":"Psychology", "text":"Psychology"},
                {"values":"Religious Studies", "text":"Religious Studies"},
                {"values":"Slavic Languages and Literatures", "text":"Slavic Languages and Literatures"},
                {"values":"Sociology", "text":"Sociology"},
                {"values":"Spanish", "text":"Spanish"},
                {"values":"Special Education (BSEd)", "text":"Special Education (BSEd)"},
                {"values":"Speech Communication Disorders (BSEd)", "text":"Speech Communication Disorders (BSEd)"},
                {"values":"Statistics", "text":"Statistics"},
                {"values":"Studio Art", "text":"Studio Art"},
                {"values":"Systems Engineering", "text":"Systems Engineering"},
                {"values":"Urban and Environmental Planning", "text":"Urban and Environmental Planning"},
                {"values":"Women, Gender & Sexuality", "text":"Women, Gender & Sexuality"},
                {"values":"Youth & Social Innovation (BSEd)", "text":"Youth & Social Innovation (BSEd)"},
                {"values":"Other", "text":"Other"},
            ],
            minors:[
                {'value':'', 'text':'None'},
                {"values":"Aerospace Engineering", "text":"Aerospace Engineering"},
                {"values":"African American and African Studies", "text":"African American and African Studies"},
                {"values":"American Studies", "text":"American Studies"},
                {"values":"Anthropology", "text":"Anthropology"},
                {"values":"Archaeology", "text":"Archaeology"},
                {"values":"Architectural History", "text":"Architectural History"},
                {"values":"Architecture", "text":"Architecture"},
                {"values":"Astronomy", "text":"Astronomy"},
                {"values":"Bachelor of Interdisciplinary Studies", "text":"Bachelor of Interdisciplinary Studies"},
                {"values":"Bachelor of Professional Studies in Health Sciences Management", "text":"Bachelor of Professional Studies in Health Sciences Management"},
                {"values":"Biology", "text":"Biology"},
                {"values":"Biomedical Engineering", "text":"Biomedical Engineering"},
                {"values":"Chemical Engineering", "text":"Chemical Engineering"},
                {"values":"Chemistry", "text":"Chemistry"},
                {"values":"Civil Engineering", "text":"Civil Engineering"},
                {"values":"Classics", "text":"Classics"},
                {"values":"Cognitive Science", "text":"Cognitive Science"},
                {"values":"Commerce", "text":"Commerce"},
                {"values":"Common First Year in the School of Architecture", "text":"Common First Year in the School of Architecture"},
                {"values":"Comparative Literature", "text":"Comparative Literature"},
                {"values":"Computer Engineering", "text":"Computer Engineering"},
                {"values":"Computer Science", "text":"Computer Science"},
                {"values":"Dance", "text":"Dance"},
                {"values":"Drama", "text":"Drama"},
                {"values":"Early Childhood Education (BSEd)", "text":"Early Childhood Education (BSEd)"},
                {"values":"East Asian Languages, Literatures and Culture", "text":"East Asian Languages, Literatures and Culture"},
                {"values":"Economics", "text":"Economics"},
                {"values":"Electrical Engineering", "text":"Electrical Engineering"},
                {"values":"Elementary Education (BSEd)", "text":"Elementary Education (BSEd)"},
                {"values":"Engineering Science", "text":"Engineering Science"},
                {"values":"English", "text":"English"},
                {"values":"Environmental Sciences", "text":"Environmental Sciences"},
                {"values":"Environmental Thought and Practice", "text":"Environmental Thought and Practice"},
                {"values":"Five-Year Teacher Education Program", "text":"Five-Year Teacher Education Program"},
                {"values":"French", "text":"French"},
                {"values":"German", "text":"German"},
                {"values":"German Studies", "text":"German Studies"},
                {"values":"Global Studies", "text":"Global Studies"},
                {"values":"Global Sustainability Minor", "text":"Global Sustainability Minor"},
                {"values":"Historic Preservation Minor", "text":"Historic Preservation Minor"},
                {"values":"History", "text":"History"},
                {"values":"History of Art", "text":"History of Art"},
                {"values":"Human Biology", "text":"Human Biology"},
                {"values":"Interdisciplinary Major in Computer Science", "text":"Interdisciplinary Major in Computer Science"},
                {"values":"Interdisciplinary Major of Global Studies", "text":"Interdisciplinary Major of Global Studies"},
                {"values":"Jewish Studies", "text":"Jewish Studies"},
                {"values":"Kinesiology (BSEd)", "text":"Kinesiology (BSEd)"},
                {"values":"Landscape Architecture Minor", "text":"Landscape Architecture Minor"},
                {"values":"Latin American Studies", "text":"Latin American Studies"},
                {"values":"Linguistics", "text":"Linguistics"},
                {"values":"Materials Science and Engineering", "text":"Materials Science and Engineering"},
                {"values":"Mathematics", "text":"Mathematics"},
                {"values":"Mechanical Engineering", "text":"Mechanical Engineering"},
                {"values":"Media Studies", "text":"Media Studies"},
                {"values":"Medieval Studies", "text":"Medieval Studies"},
                {"values":"Middle Eastern and South Asian Languages and Cultures", "text":"Middle Eastern and South Asian Languages and Cultures"},
                {"values":"Music", "text":"Music"},
                {"values":"Neuroscience", "text":"Neuroscience"},
                {"values":"Nursing", "text":"Nursing"},
                {"values":"Philosophy", "text":"Philosophy"},
                {"values":"Physics", "text":"Physics"},
                {"values":"Political and Social Thought", "text":"Political and Social Thought"},
                {"values":"Political Philosophy, Policy, and Law", "text":"Political Philosophy, Policy, and Law"},
                {"values":"Politics", "text":"Politics"},
                {"values":"Psychology", "text":"Psychology"},
                {"values":"Religious Studies", "text":"Religious Studies"},
                {"values":"Slavic Languages and Literatures", "text":"Slavic Languages and Literatures"},
                {"values":"Sociology", "text":"Sociology"},
                {"values":"Spanish", "text":"Spanish"},
                {"values":"Special Education (BSEd)", "text":"Special Education (BSEd)"},
                {"values":"Speech Communication Disorders (BSEd)", "text":"Speech Communication Disorders (BSEd)"},
                {"values":"Statistics", "text":"Statistics"},
                {"values":"Studio Art", "text":"Studio Art"},
                {"values":"Systems Engineering", "text":"Systems Engineering"},
                {"values":"Urban and Environmental Planning", "text":"Urban and Environmental Planning"},
                {"values":"Women, Gender & Sexuality", "text":"Women, Gender & Sexuality"},
                {"values":"Youth & Social Innovation (BSEd)", "text":"Youth & Social Innovation (BSEd)"},
                {"values":"Other", "text":"Other"},
                {"values":"American Sign Language", "text":"American Sign Language"},
                {"values":"Bioethics", "text":"Bioethics"},
                {"values":"Global Studies in Education Minor", "text":"Global Studies in Education Minor"},
                {"values":"Health and Wellbeing Minor", "text":"Health and Wellbeing Minor"},
                {"values":"Minor in Data Science", "text":"Minor in Data Science"},
                {"values":"Minor in Data Analytics", "text":"Minor in Data Analytics"},
                {"values":"Public Policy and Leadership Minor", "text":"Public Policy and Leadership Minor"},
            ],
                // {'value':'Accelerated B.A./Master of Public Policy (MPP) Program', 'text':'Accelerated B.A./Master of Public Policy (MPP) Program'},
                // {'value':'Accounting', 'text':'Accounting'},
                // {'value':'Aerospace Engineering', 'text':'Aerospace Engineering'},
                // {'value':'African American & African Studies', 'text':'African American & African Studies'},
                // {'value':'American Studies', 'text':'American Studies'},
                // {'value':'Anthropology', 'text':'Anthropology'},
                // {'value':'Architectural History', 'text':'Architectural History'},
                // {'value':'Architecture', 'text':'Architecture'},
                // {'value':'Art History', 'text':'Art History'},
                // {'value':'Art, Studio', 'text':'Art, Studio'},
                // {'value':'Astronomy', 'text':'Astronomy'},
                // {'value':'Astronomy-Physics', 'text':'Astronomy-Physics'},
                // {'value':'B.A. in Public Policy and Leadership', 'text':'B.A. in Public Policy and Leadership'},
                // {'value':'B.S./M.S. in Teaching', 'text':'B.S./M.S. in Teaching'},
                // {'value':'Bachelor of Science in Nursing (BSN)', 'text':'Bachelor of Science in Nursing (BSN)'},
                // {'value':'Biology', 'text':'Biology'},
                // {'value':'Biomedical Engineering', 'text':'Biomedical Engineering'},
                // {'value':'Chemical Engineering', 'text':'Chemical Engineering'},
                // {'value':'Chemistry', 'text':'Chemistry'},
                // {'value':'Chinese Language & Literature', 'text':'Chinese Language & Literature'},
                // {'value':'Civil Engineering', 'text':'Civil Engineering'},
                // {'value':'Classics', 'text':'Classics'},
                // {'value':'Cognitive Science', 'text':'Cognitive Science'},
                // {'value':'Commerce', 'text':'Commerce'},
                // {'value':'Comparative Literature', 'text':'Comparative Literature'},
                // {'value':'Computer Engineering', 'text':'Computer Engineering'},
                // {'value':'Computer Science', 'text':'Computer Science'},
                // {'value':'Drama', 'text':'Drama'},
                // {'value':'East Asian Studies', 'text':'East Asian Studies'},
                // {'value':'Economics', 'text':'Economics'},
                // {'value':'Electrical Engineering', 'text':'Electrical Engineering'},
                // {'value':'Engineering Science', 'text':'Engineering Science'},
                // {'value':'English', 'text':'English'},
                // {'value':'Environmental Sciences', 'text':'Environmental Sciences'},
                // {'value':'Environmental Thought & Practice', 'text':'Environmental Thought & Practice'},
                // {'value':'Finance', 'text':'Finance'},
                // {'value':'French', 'text':'French'},
                // {'value':'German', 'text':'German'},
                // {'value':'Global Studies', 'text':'Global Studies'},
                // {'value':'History', 'text':'History'},
                // {'value':'Human Biology', 'text':'Human Biology'},
                // {'value':'Information Technology', 'text':'Information Technology'},
                // {'value':'Italian', 'text':'Italian'},
                // {'value':'Japanese Language & Literature', 'text':'Japanese Language & Literature'},
                // {'value':'Jewish Studies', 'text':'Jewish Studies'},
                // {'value':'Kinesiology', 'text':'Kinesiology'},
                // {'value':'Latin American Studies', 'text':'Latin American Studies'},
                // {'value':'Linguistics', 'text':'Linguistics'},
                // {'value':'Management', 'text':'Management'},
                // {'value':'Marketing', 'text':'Marketing'},
                // {'value':'Mathematics', 'text':'Mathematics'},
                // {'value':'Mechanical Engineering', 'text':'Mechanical Engineering'},
                // {'value':'Media Studies', 'text':'Media Studies'},
                // {'value':'Medieval Studies', 'text':'Medieval Studies'},
                // {'value':'Middle Eastern and South Asian Languages and Cultures', 'text':'Middle Eastern and South Asian Languages and Cultures'},
                // {'value':'Music', 'text':'Music'},
                // {'value':'Neuroscience', 'text':'Neuroscience'},
                // {'value':'Philosophy', 'text':'Philosophy'},
                // {'value':'Physics', 'text':'Physics'},
                // {'value':'Political Philosophy, Policy, and Law', 'text':'Political Philosophy, Policy, and Law'},
                // {'value':'Political and Social Thought', 'text':'Political and Social Thought'},
                // {'value':'Politics', 'text':'Politics'},
                // {'value':'Psychology', 'text':'Psychology'},
                // {'value':'RN to BSN', 'text':'RN to BSN'},
                // {'value':'Religious Studies', 'text':'Religious Studies'},
                // {'value':'Slavic Languages and Literatures', 'text':'Slavic Languages and Literatures'},
                // {'value':'Sociology', 'text':'Sociology'},
                // {'value':'South Asian Studies', 'text':'South Asian Studies'},
                // {'value':'Spanish', 'text':'Spanish'},
                // {'value':'Speech Communications Disorders Major', 'text':'Speech Communications Disorders Major'},
                // {'value':'Statistics', 'text':'Statistics'},
                // {'value':'Systems Engineering', 'text':'Systems Engineering'},
                // {'value':'Teacher Education', 'text':'Teacher Education'},
                // {'value':'Urban & Environmental Planning', 'text':'Urban & Environmental Planning'},
                // {'value':'Women, Gender, and Sexuality', 'text':'Women, Gender, and Sexuality'},
                // {'value':'Youth & Social Innovation Major', 'text':'Youth & Social Innovation Major'},]
        }
    },
    components:{
    },
    computed:{
    },
    watch:{

    },
    methods: {
        editUser(user, edit_user_image, edit_user_video){
            this.$refs.edit_form.validate();
            if(!this.edit_user_form_valid)
                return;
            this.editUserBtnLoading = true;
            let formData = new FormData();
            formData.append('picture', edit_user_image);
            formData.append('video', edit_user_video);
            for(var key in user){
                if(key != "picture" && key != "video"){
                    formData.append(key, user[key]);
                }
            }
            if(edit_user_video)
                this.$emit("enable-snack", "video_snack");
            axios.post('/users/api/edit_user/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                this.editUserBtnLoading = false;
                if(response.data.success){
                    // this.submitBtnEnable = false;
                    this.$emit("edit-success", this.username);
                }else{
                    this.$emit("enable-snack", "failure_snack");
                }
            });
        },
        getProfile(username){
            axios.get('/users/api/get_profile/',{params: {username:username}}).then(response => {
                if(response.data.success){
                    this.edit_user = response.data.user;
                }
                this.loaded = true;
            });
        },
    },
    mounted(){
        this.getProfile(this.username);
    },
};
</script>

<style scoped>

    .cus-table{
        table-layout: fixed;
        width:100%;
    }

    tr td:first-child{
        color: rgb(156, 154, 154);
    }

    tr td:last-child{
        color: rgb(0, 0, 0);
    }

    .left-tr{
        width:24%;
    }

    .right-td{
        width:76%;
    }

    .description-td{
        padding: 6px 16px 15px 16px !important;
        /* font-family: "Times New Roman", Times, serif !important; */
    }

    .table-title{
        font-size:20px !important;
        font-weight: 700 !important;
    }

    .v-card__title{
        font-weight: 600 !important;
    }

    .v-card__text td{
        font-family: "Times New Roman", Times, serif !important; 
        font-size: 16px !important;
        padding: 6px 16px;
    }


    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {

    }


    @media (min-width: 10px) and (max-width: 767px) {
        .left-tr{
            width:28% !important;
        }

        .right-td{
            width:72% !important;
        }
        
    }


</style>
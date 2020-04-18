<template>
    <v-app>
        <match-header></match-header>
        <v-content>
            <v-container v-if="!loaded" fluid fill-height>
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
            <v-container v-if="!edit_user && loaded" fluid fill-height>
                <v-layout 
                    align-center
                    justify-center>
                    <div class="item-not-exist">
                        User does not exist~~
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="edit_user && loaded" fluid grid-list-lg>
                <v-row>
                    <v-col offset="0" offset-sm="0" offset-md="2" offset-lg="3" offset-xl="4" 
                     cols="12" sm="12" md="8" lg="6" xl="4">
                        <v-card>
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
                                    label="First Name"
                                    required
                                    ></v-text-field>

                                    <v-text-field
                                    v-model="edit_user.last_name"
                                    :rules="lastnameRules"
                                    label="Last Name"
                                    required
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
                                    label="Graduate Year"
                                    required
                                    ></v-select>

                                    <v-select
                                    v-model="edit_user.major"
                                    :items="majors"
                                    :rules="[v => !!v || 'Major is required (or intended major)']"
                                    label="Major"
                                    required
                                    ></v-select>

                                    <v-select
                                    v-model="edit_user.major_two"
                                    :items="majors"
                                    label="Second Major"
                                    ></v-select>

                                    <v-select
                                    v-model="edit_user.minor"
                                    :items="majors"
                                    label="Minor"
                                    ></v-select>

                                    <v-text-field
                                    v-model="edit_user.wechat"
                                    :rules="wechatRules"
                                    label="WeChat ID"
                                    ></v-text-field>

                                    <v-textarea
                                    v-model="edit_user.bio"
                                    label="Bio"
                                    outlined
                                    :rules="bioRules"
                                    required
                                    :counter="1000"
                                    rows="4"
                                    row-height="20"
                                    ></v-textarea>

                                    <v-file-input 
                                    v-model="edit_user_image"
                                    accept="image/*"
                                    label="Upload an image"
                                    ></v-file-input>
                                </v-form>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="green darken-1" outlined :loading="editUserBtnLoading" @click.prevent="editUser(edit_user, edit_user_image)">Edit</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red darken-1"
            :timeout="3200">
            Sth is wrong
            <v-btn color="white" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
    </v-app>
</template>

<script>
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
        return {
            loaded:false,
            failure_snack: false,
            edit_user:null,
            editUserBtnLoading:false,
            edit_user_form_valid:false,
            edit_user_image:null,
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
                v => (v && v.length <= 1000) || 'Last Name must be less than 1000 characters',
            ],
            wechatRules: [
                v => (!v || (v && v.length <= 255)) || 'WeChat ID must be less than 255 characters',
            ],
            graduate_years:[    
                {'value':'2018', 'text':'2018'},
                {'value':'2019', 'text':'2019'},
                {'value':'2020', 'text':'2020'},
                {'value':'2021', 'text':'2021'},
                {'value':'2022', 'text':'2022'},
                {'value':'2023', 'text':'2023'},
                {'value':'2024', 'text':'2024'},
            ],
            genders:[
                {'value':'Male', 'text':'Male'},
                {'value':'Female', 'text':'Female'},
            ],
            majors: [
                {'value':'', 'text':'None'},
                {'value':'Accelerated B.A./Master of Public Policy (MPP) Program', 'text':'Accelerated B.A./Master of Public Policy (MPP) Program'},
                    {'value':'Accounting', 'text':'Accounting'},
                    {'value':'Aerospace Engineering', 'text':'Aerospace Engineering'},
                    {'value':'African American & African Studies', 'text':'African American & African Studies'},
                    {'value':'American Studies', 'text':'American Studies'},
                    {'value':'Anthropology', 'text':'Anthropology'},
                    {'value':'Architectural History', 'text':'Architectural History'},
                    {'value':'Architecture', 'text':'Architecture'},
                    {'value':'Art History', 'text':'Art History'},
                    {'value':'Art, Studio', 'text':'Art, Studio'},
                    {'value':'Astronomy', 'text':'Astronomy'},
                    {'value':'Astronomy-Physics', 'text':'Astronomy-Physics'},
                    {'value':'B.A. in Public Policy and Leadership', 'text':'B.A. in Public Policy and Leadership'},
                    {'value':'B.S./M.S. in Teaching', 'text':'B.S./M.S. in Teaching'},
                    {'value':'Bachelor of Science in Nursing (BSN)', 'text':'Bachelor of Science in Nursing (BSN)'},
                    {'value':'Biology', 'text':'Biology'},
                    {'value':'Biomedical Engineering', 'text':'Biomedical Engineering'},
                    {'value':'Chemical Engineering', 'text':'Chemical Engineering'},
                    {'value':'Chemistry', 'text':'Chemistry'},
                    {'value':'Chinese Language & Literature', 'text':'Chinese Language & Literature'},
                    {'value':'Civil Engineering', 'text':'Civil Engineering'},
                    {'value':'Classics', 'text':'Classics'},
                    {'value':'Cognitive Science', 'text':'Cognitive Science'},
                    {'value':'Commerce', 'text':'Commerce'},
                    {'value':'Comparative Literature', 'text':'Comparative Literature'},
                    {'value':'Computer Engineering', 'text':'Computer Engineering'},
                    {'value':'Computer Science', 'text':'Computer Science'},
                    {'value':'Drama', 'text':'Drama'},
                    {'value':'East Asian Studies', 'text':'East Asian Studies'},
                    {'value':'Economics', 'text':'Economics'},
                    {'value':'Electrical Engineering', 'text':'Electrical Engineering'},
                    {'value':'Engineering Science', 'text':'Engineering Science'},
                    {'value':'English', 'text':'English'},
                    {'value':'Environmental Sciences', 'text':'Environmental Sciences'},
                    {'value':'Environmental Thought & Practice', 'text':'Environmental Thought & Practice'},
                    {'value':'Finance', 'text':'Finance'},
                    {'value':'French', 'text':'French'},
                    {'value':'German', 'text':'German'},
                    {'value':'Global Studies', 'text':'Global Studies'},
                    {'value':'History', 'text':'History'},
                    {'value':'Human Biology', 'text':'Human Biology'},
                    {'value':'Information Technology', 'text':'Information Technology'},
                    {'value':'Italian', 'text':'Italian'},
                    {'value':'Japanese Language & Literature', 'text':'Japanese Language & Literature'},
                    {'value':'Jewish Studies', 'text':'Jewish Studies'},
                    {'value':'Kinesiology', 'text':'Kinesiology'},
                    {'value':'Latin American Studies', 'text':'Latin American Studies'},
                    {'value':'Linguistics', 'text':'Linguistics'},
                    {'value':'Management', 'text':'Management'},
                    {'value':'Marketing', 'text':'Marketing'},
                    {'value':'Mathematics', 'text':'Mathematics'},
                    {'value':'Mechanical Engineering', 'text':'Mechanical Engineering'},
                    {'value':'Media Studies', 'text':'Media Studies'},
                    {'value':'Medieval Studies', 'text':'Medieval Studies'},
                    {'value':'Middle Eastern and South Asian Languages and Cultures', 'text':'Middle Eastern and South Asian Languages and Cultures'},
                    {'value':'Music', 'text':'Music'},
                    {'value':'Neuroscience', 'text':'Neuroscience'},
                    {'value':'Philosophy', 'text':'Philosophy'},
                    {'value':'Physics', 'text':'Physics'},
                    {'value':'Political Philosophy, Policy, and Law', 'text':'Political Philosophy, Policy, and Law'},
                    {'value':'Political and Social Thought', 'text':'Political and Social Thought'},
                    {'value':'Politics', 'text':'Politics'},
                    {'value':'Psychology', 'text':'Psychology'},
                    {'value':'RN to BSN', 'text':'RN to BSN'},
                    {'value':'Religious Studies', 'text':'Religious Studies'},
                    {'value':'Slavic Languages and Literatures', 'text':'Slavic Languages and Literatures'},
                    {'value':'Sociology', 'text':'Sociology'},
                    {'value':'South Asian Studies', 'text':'South Asian Studies'},
                    {'value':'Spanish', 'text':'Spanish'},
                    {'value':'Speech Communications Disorders Major', 'text':'Speech Communications Disorders Major'},
                    {'value':'Statistics', 'text':'Statistics'},
                    {'value':'Systems Engineering', 'text':'Systems Engineering'},
                    {'value':'Teacher Education', 'text':'Teacher Education'},
                    {'value':'Urban & Environmental Planning', 'text':'Urban & Environmental Planning'},
                    {'value':'Women, Gender, and Sexuality', 'text':'Women, Gender, and Sexuality'},
                    {'value':'Youth & Social Innovation Major', 'text':'Youth & Social Innovation Major'},]
        }
	},
	components:{
        MatchHeader,
	},
	watch: {
        
	},
	computed:{
        username: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 3];
        },
	},
	methods: {
        editUser(user, edit_user_image){
            this.$refs.edit_form.validate();
            if(!this.edit_user_form_valid)
                return;
            this.editUserBtnLoading = true;
            let formData = new FormData();
            formData.append('picture', edit_user_image);
            for(var key in user){
                if(key != "picture"){
                    formData.append(key, user[key]);
                }
            }
            axios.post('/users/api/edit_user/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                this.editUserBtnLoading = false;
                if(response.data.success){
                    window.location.href = '/users/'+this.username;
                }else{
                    this.failure_snack = true;
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

<style>
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


    td:not(.cus-td):not(.description-text){
        /* font-family: "Times New Roman", Times, serif !important;  */
        /* font-size: 15px !important; */
        /* padding: 4px 16px; */
    }

    .dialog-head-text{
        /* font-family: "Times New Roman", Times, serif !important;  */
        padding-left:31px;
        font-size: 28px !important;
        font-weight:700 !important;
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
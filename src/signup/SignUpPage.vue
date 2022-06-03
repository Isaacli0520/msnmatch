<template>
  <v-app>
    <v-main>
      <v-container class="content-div" fill-height>
        <v-row>
          <v-col offset-sm="0" offset-md="2" offset-lg="3" offset-xl="4" sm="12" md="8" lg="6" xl="4">
            <v-card v-if="signup_success">
              <v-card-title>Final Step</v-card-title>
              <v-divider />
              <v-card-text> Please go to your email and click the activation link to complete the registration</v-card-text>
            </v-card>
            <v-card v-if="!signup_success">
              <v-card-title>Sign Up</v-card-title>
              <v-divider />
              <v-card-text>
                <h3 v-if="error !== ''" style="color:red;">{{error}}</h3>
                <v-form
                  method="post"
                  ref="edit_form"
                  v-model="edit_user_form_valid">

                  <v-text-field
                    v-model="edit_user.email"
                    :rules="emailRules"
                    label="Email*"
                    hint="Must be UVa email"
                    required
                    ></v-text-field>

                  <v-text-field
                    v-model="edit_user.password1"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="password1Rules"
                    :type="show1 ? 'text' : 'password'"
                    label="Password*"
                    hint="At least 8 characters"
                    counter
                    @click:append="show1 = !show1"
                  ></v-text-field>

                  <v-text-field
                    v-model="edit_user.password2"
                    :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="password2Rules"
                    :type="show2 ? 'text' : 'password'"
                    label="Password Again*"
                    hint="At least 8 characters"
                    counter
                    @click:append="show2 = !show2"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-divider />
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" outlined :loading="editUserBtnLoading" @click.prevent="signUpUser(edit_user)">Submit</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
  data() {
    return {
      signup_success: false,
      error: '',
      edit_user: {
        email: '',
        password1: '',
        password2: '',
      },
      editUserBtnLoading:false,
      edit_user_form_valid:false,
      show1: false,
      show2: false,
      emailRules: [
        v => !!v || 'Email is required',
        v => (v && v.length <= 30) || 'Email must be less than 30 characters',
        v => /^[a-z]+[0-9][a-z]+@virginia.edu$/g.test(v) || 'Must be UVa Email (@virginia.edu)'
      ],
      password1Rules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 8) || 'Password must be at least 8 characters long',
      ],
      
    }
  },
  computed:{
    password2Rules(){
      return [
        v => !!v || 'Please enter the password again',
        v => (v && v === this.edit_user.password1) || 'Password must be the same',
      ]
    },
  },
  methods: {
    signUpUser(user){
      this.error = '';
      this.$refs.edit_form.validate();
      if(!this.edit_user_form_valid)
        return;
      this.editUserBtnLoading = true;
      let formData = new FormData();
      for(const key in user){
        formData.append(key, user[key])
      }
      const match = this.edit_user.email.match(/^([a-z]+[0-9][a-z]+)@virginia.edu$/)
      if (match === null || match[1] === undefined) return

      formData.append('username', match[1])
      axios.post('/users/api/signup_user/',formData,
      {
        headers:{
          'Content-Type': 'multipart/form-data',
        }
      }).then(response => {
        this.editUserBtnLoading = false;
        if(response.data.success){
          this.signup_success = true
        }else{
          this.error = response.data.message
        }
      });
    },
  },
};
</script>

<style scoped>
  .content-div::before{
    content: ' ';
    position: fixed;
    background: url('../assets/static/css/images/cloud_bg_new_02.jpg') no-repeat center center;
    background-size: cover;
    will-change: transform;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
</style>
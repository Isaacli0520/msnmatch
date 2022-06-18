<template>
  <v-app>
    <match-header
      @del-from-fav="deleteFromFav"
      :headerUpdate="headerUpdate"></match-header>
    <v-main class="content-div">
      <v-container class="fill-height" v-if="!loaded">
        <v-row justify="center" align="center">
          <v-progress-circular
            :size="60"
            :width="6"
            indeterminate
            color="teal lighten-1"/>
        </v-row>
      </v-container>
      <v-container v-else>
        <div class="top-part-wrapper">
          <v-row justify="center">
            <div style="text-align: center;">
              <h1 class="title-text">MATCH</h1>
            </div>
          </v-row>
          <v-row>
            <div class="search-tags mb-3">
              <span :key="index" v-for="(tag,index) in tags"
                class="search-tag">
                <span>{{tag}}</span>
                <span class="search-tag-remove">
                  <v-icon color="teal lighten-2" style="margin-bottom:2px;" small @click="del_tag(tag)">mdi-close-thick</v-icon>
                </span>
              </span>
            </div>
          </v-row>
          <v-row justify="center">
            <div style="max-width:600px;width:80%;">
              <div class="search-form mt-1">          
                <input 
                  @keydown="onKeydown" 
                  v-model="query" 
                  autocomplete="off" 
                  id="myInput" 
                  type="text" 
                  name="class" 
                  placeholder=" &quot;Marvel&quot;, &quot;major:Math&quot;, &quot;loc:Beijing&quot; " 
                  class="search-input" 
                  aria-label="Search">
              </div>
              <div style="font-size:12px;color:grey;margin-top:8px;">
                *Type a tag or a filter (major:Commerce) and press Enter to filter users
              </div>
            </div>
          </v-row>
          <v-row style="margin-top:3px;">
            <div class="checkbox-div">
              <v-checkbox v-model="tags" hide-details class="mr-2" value="role:Mentor" label="Mentor"></v-checkbox>
              <v-checkbox v-model="tags" hide-details class="mr-2" value="role:Mentee" label="Mentee"></v-checkbox>
            </div>
          </v-row>
          <v-row justify="center">
            <div style="text-align:center; margin-top:13px; margin-bottom:10px;">
              <template v-if="request_user.role == '' ">
                <v-btn style="margin-right: 10px;" outlined color="teal lighten-1" :loading="mentorBtnLoading" @click="openRoleDialog('Mentor')">Be A Mentor</v-btn>
                <v-btn outlined color="teal lighten-1" @click="openRoleDialog('Mentee')">Be A Mentee</v-btn>
              </template>
              <template v-else>
                <v-btn outlined color="teal lighten-1" @click="get_users_by_sim();clicked=true;">Click Me!</v-btn>
              </template>
              <v-btn style="margin-left: 10px;" outlined color="teal lighten-1" @click="openStatsDialog();">Stats</v-btn>
              <v-btn
                style="margin-left: 10px;"
                outlined
                color="teal lighten-1"
                @click="new_ui=!new_ui;"
              >
                {{ new_ui ? "Compact" : "Normal"}}
                <v-icon right dark>{{ new_ui ? "mdi-grid" : "mdi-grid-large" }}</v-icon>
              </v-btn>
            </div>
          </v-row>
          <v-row justify="center">
            <div v-if="clicked" style="text-align:center;">
              <small class="muted-text">*The scores are calculated based on mutual tags with some normalization</small>
            </div>
          </v-row>
          <v-row justify="center">
            <div v-if="clicked" style="text-align:center;">
              <small class="muted-text">*They are just for fun😁</small>
            </div>
          </v-row>
          <v-row  v-if="clicked && new_ui" justify="center">
            <div style="text-align:center;">
              <small class="muted-text">*Scores are not displayed in compact view</small>
            </div>
          </v-row>
        </div>
        <!-- Main User List -->
        <v-row>
          <v-col
            v-for="user_idx in user_idxs" :key="user_idx"
            cols="12" sm="6" md="4" lg="4" xl="3">
            <user-card
              class="fill-height"
              :new_ui="new_ui"
              :user_index="user_idx"
              :user="users[user_idx]" @open-user-dialog="openUserDialog"></user-card>
          </v-col>
        </v-row>
      </v-container>
      <user-dialog
        v-if="d_user"
        :add_to_fav="request_user.role!='' && request_user.role != d_user.role"
        :edit="request_user.username == d_user.username"
        :user="d_user"
        @add-to-fav="addToFav"
        @del-from-fav="deleteFromFav"
        v-model="userDialog"></user-dialog>
    </v-main>
    <v-dialog v-if="loaded" v-model="roleDialog" scrollable min-width="350px" max-width="800px">
      <v-stepper v-model="current_step">
        <v-stepper-header>
          <v-stepper-step :complete="current_step > 1" step="1">
            Basic Info
          </v-stepper-step>
          <v-stepper-step :complete="current_step > 2" step="2">
            Add Tags
          </v-stepper-step>
          <v-stepper-step :complete="current_step > 3" step="3">
            Be a {{dialogRole}}!
          </v-stepper-step>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content step="1">
            <v-card class="stepper-card">
              <profile-edit 
                editBtnName="Edit & Continue"
                :username="request_user.username" 
                @edit-success="editSuccess" 
                @enable-snack="enableSnack" />
            </v-card>
            <v-btn class="stepper-continue-btn" outlined @click="roleDialog=false;">Cancel</v-btn>
          </v-stepper-content>
          <v-stepper-content step="2">
            <v-card class="stepper-card">
              <v-card-title>Add Your Interests</v-card-title>
              <v-divider/>
              <div class="ma-4">
                <h4 class="stepper-tags-text">Add your interests by clicking on the tags below.</h4>
                <h4 class="stepper-tags-text">You must add at least 3 tags to continue.</h4>
                <h4 class="stepper-tags-text">You can always add more tags on the Tags page.</h4>
                <h2 class="mt-3 your-tags">Your Tags</h2>
                <div class="skill-tags mb-3">
                  <template v-for="skills_of_type in user_skills">
                    <tag-span v-for="skill in skills_of_type.skills"
                      :key="skill.id"
                      :skill="skill"
                      clickable="delete"
                      @add-skill="addSkill"
                      @del-skill="deleteSkill"
                    />
                  </template>
                </div>
                <div :key="index" v-for="(skills_of_type, index) in all_skills">
                  <h3 class="skill-type-text">{{skill_type_names[skills_of_type.type]}}</h3>
                  <div class="skill-tags">
                    <tag-span v-for="skill in skills_of_type.skills"
                      :key="skill.id"
                      :skill="skill"
                      :clickable="'add'"
                      @add-skill="addSkill"
                      @del-skill="deleteSkill"
                    />
                  </div>
                </div>
              </div>
            </v-card>
            <v-btn class="stepper-continue-btn" outlined color="primary" :disabled="user_skills_count < 3" @click="current_step=3">Continue</v-btn>
            <v-btn class="stepper-continue-btn" outlined color="light-blue darken-1" dark @click="current_step = current_step - 1">Back</v-btn>
            <v-btn class="stepper-continue-btn" outlined @click="roleDialog=false;">Cancel</v-btn>
          </v-stepper-content>
          <v-stepper-content step="3">
            <v-card class="stepper-card">
              <div v-if="dialogRole == 'Mentor'" class="ma-4">
                <p style="font-size:19x;font-weight:600;">成为Mentor需要做到什么？</p>
                <p>1.第一时间联系你的Mentee，让TA感受到夏村大家庭的温暖和友好，并尽量在国内就开始与新生进行线上线下的交流。</p>
                <p>2.能够耐心地解决新生的问题，主动向新生分享自己的资源和经历。</p>
                <p>3.给予新生支持，鼓励新生尝试新的事物，融入美国校园，并积极带领新手感受夏村的生活</p>
                <p>4.帮助一起建设MSN Hoos My Professor网站，分享学术方面的经历，从而帮助建立新生选课的指南。</p>
                <p style="font-size:19x;font-weight:600;">Be a Mentor</p>
                <p>如果你觉得自己可以做到以上几点</p>
                <p>那么点击Yes即可成为Mentor!</p>
                <p>Do you really want to be a <strong>{{dialogRole}}</strong>?</p>
              </div>
              <div v-else class="ma-4">
                <p style="font-size:19px;font-weight:600;">Do you really want to be a Mentee?</p>
                <p>Click <strong>YES</strong> to become a Mentee!</p>
                <p style="font-size:14px; margin-bottom:0px !important;" class="muted-text">*Note that your role can only be changed by the mentor program chair once you've made your choice.</p>
              </div>
            </v-card>
            <v-btn class="stepper-continue-btn" outlined color="primary" :loading="roleBtnLoading" @click="setRole(dialogRole)">Yes</v-btn>
            <v-btn class="stepper-continue-btn" outlined color="light-blue darken-1" dark @click="current_step = current_step - 1">Back</v-btn>
            <v-btn class="stepper-continue-btn" outlined @click="roleDialog=false;">Cancel</v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-dialog>
    <v-dialog v-model="statsDialog" scrollable min-width="350px" max-width="800px">
      <v-card>
        <v-card-title>Stats</v-card-title>
        <v-divider></v-divider>
        <v-tabs
          v-model="tag_tab"
          color="teal darken-1"
          show-arrows
          grow
        >
          <v-tab
            v-for="(skills_of_type, _big_skill_idx) in all_users_skills"
            :key="_big_skill_idx"
          >
            {{ skills_of_type.type }}
          </v-tab>
        </v-tabs>
        <v-tabs-items
          style="overflow:scroll;"
          v-model="tag_tab"
          >
          <v-tab-item
            v-for="(skills_of_type, _big_skill_idx) in all_users_skills"
            :key="_big_skill_idx" 
          >
            <v-sheet
              color="white"
              style="padding:10px 20px;"
              elevation="1"
            >
              <div class="tag-percent"
                :key="_skill_idx"
                v-for="(skill, _skill_idx) in skills_of_type.skills">
                <label  class="tag-percent__label">
                  <span 
                    :style="`background-color:${variables[skills_of_type.type.split(' ').join('-')+'-color']}`" 
                    class="tag-percent__span"
                  >
                    {{skill.name}}
                  </span>
                </label>
                <v-progress-linear
                  class="tag-percent__value"
                  rounded
                  dark
                  :value="100 * skill.count / skills_of_type.max"
                  :color="variables[skills_of_type.type.split(' ').join('-')+'-color']"
                  height="25"
                  style="margin-top:5px;"
                >
                  <template v-slot>
                    <div style="width:100%;">
                    <div :style="`text-align:center;width:${100*skill.count / skills_of_type.max}%;`">{{ skill.count }}</div>
                    </div>
                  </template>
                </v-progress-linear>
              </div>
            </v-sheet>
          </v-tab-item>
        </v-tabs-items>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="red darken-1"
            text
            @click="statsDialog=false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar
      top
      v-model="success_snack"
      color="teal darken-1"
      :timeout="1800">
      {{success_text}}
      <template v-slot:action="{ attrs }">
        <v-btn color="cyan accent-1" v-bind="attrs" text @click="success_snack = false"> Close </v-btn>
      </template>
    </v-snackbar>
    <v-snackbar
      top
      v-model="failure_snack"
      color="red lighten-1"
      :timeout="2700">
      {{failure_text}}
      <template v-slot:action="{ attrs }">
        <v-btn color="white" v-bind="attrs" text @click="failure_snack = false"> Close </v-btn>
      </template>
    </v-snackbar>
    <v-snackbar
      top
      v-model="video_snack"
      color="purple lighten-1"
      :timeout="3200">
      Video may take longer to upload. Be patient :)
      <template v-slot:action="{ attrs }">
        <v-btn color="white" v-bind="attrs" text @click="video_snack = false"> Close </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import Vue from "vue"
import axios from 'axios'
import MatchHeader from '../components/MatchHeader'
import UserDialog from '../components/UserDialog'
import UserCard from '../components/UserCard'
import ProfileEdit from '../components/ProfileEdit'
import TagSpan from '../components/TagSpan'
import variables from '../sass/variables.scss'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
  data() {
    return {
      variables:variables,
      loaded:false,
      clicked:false,
      new_ui:false,
      tag_tab:null,
      // Header
      headerUpdate: false,
      // Search Bar
      query:"",
      tags:[],
      // Users
      request_user:null,
      users:[],
      user_idxs:[],
      backup_user_idxs: [],
      backup_all_users: [],
      // Dialog
      dialogRole:"Mentor",
      mentorBtnLoading:false,
      roleBtnLoading:false,
      userDialog:false,
      roleDialog:false,
      dialog_user_index:-1,
      statsDialog:false,
      // Fuzz Search
      fuzz: null,
      options:null,
      // Snacks
      failure_text:"",
      success_text:"",
      failure_snack:false,
      success_snack:false,
      video_snack:false,
      // Stepper
      current_step:1,
      // Tags
      all_skills:[],
      user_skills:[],
      skill_type_names:{
        "Game":"Game",
        "Academic":"Academic Interests",
        "Film and TV":"Film and TV",
        "Sport":"Sport",
        "Music":"Music",
        "Language":"Language",
        "General":"General",
        "Books":"Books",
        "MBTI":"MBTI",
      },
    }
  },
  components:{
    MatchHeader,
    UserCard,
    UserDialog,
    ProfileEdit,
    TagSpan,
  },
  watch: {
    tags(val){
      this.user_list_filter(val);
    },
  },
  computed:{
    d_user(){
      if(this.dialog_user_index < 0)
        return null;
      else
        return this.users[this.dialog_user_index];
    },
    user_skills_count(){
      if(Object.keys(this.user_skills).length == 0)
        return 0
      return Object.values(this.user_skills).map(arr => arr.length).reduce((a, b) => a + b);
    },
    all_users_skills() {
      if (this.backup_all_users.length === 0) 
        return [[]]
      const users_arr = Object.values(this.backup_all_users)
      const skills = users_arr[0].skills.map((skills_of_type) => ({ ...skills_of_type, skills: {} }))
      for (const user of users_arr) {
        for (const skills_of_type of user.skills) {
          for (const skill of skills_of_type.skills) {
            if (skills[skills_of_type.index].skills[skill.id] === undefined)
              skills[skills_of_type.index].skills[skill.id] = { ...skill, count: 0 }
            skills[skills_of_type.index].skills[skill.id].count += 1
          }
        }
      }
      for (const skills_of_type of skills) {
        skills[skills_of_type.index].skills = Object.values(skills_of_type.skills).sort((a, b) => b.count - a.count)
        skills[skills_of_type.index].max = Math.max(...skills[skills_of_type.index].skills.map((skill) => skill.count))
      }
      return skills
    },
  },
  methods: {
    openStatsDialog() {
      this.statsDialog = true;
    },
    getSkills(){
      axios.get('/users/api/get_all_and_user_skills/').then(response => {
        this.all_skills = response.data.all_skills;
        this.user_skills = response.data.user_skills;
        this.loaded = true;
      });
    },
    addSkill(skill){
      axios.post("/skills/api/user_add_skill/", {
        "id":skill.id,
        "name":skill.name,
      }).then(response => {
        if(response.data.success){
          let tmp_skill = JSON.parse(JSON.stringify(skill));
          tmp_skill.id = response.data.id;

          let skills_of_type = this.all_skills.filter((item) => item.type === skill.type)
          if (skills_of_type.length === 0) return
          skills_of_type = skills_of_type[0]

          let all_skill_pos = this.all_skills[skills_of_type.index].skills.map((item) => item.id).indexOf(tmp_skill.id);
          this.user_skills[skills_of_type.index].skills.splice(-1, 0, tmp_skill);
          if(all_skill_pos != -1)
            this.all_skills[skills_of_type.index].skills.splice(all_skill_pos, 1);
          // this.success_text = "Tag Added"
          // this.success_snack = true;
        }else{
          this.failure_text = "Sth is wrong";
          this.failure_snack = true;
        }
      });
    },
    deleteSkill(skill){
      axios.post("/skills/api/user_del_skill/", {
        "id":skill.id,
      }).then(response => {
        if(response.data.success){
          let skills_of_type = this.user_skills.filter((item) => item.type === skill.type)
          if (skills_of_type.length === 0) return
          skills_of_type = skills_of_type[0]
          let user_skill_pos = this.user_skills[skills_of_type.index].skills.map((item) => item.id).indexOf(skill.id);
          if(user_skill_pos != -1)
            this.user_skills[skills_of_type.index].skills.splice(user_skill_pos, 1);
          if (skill.type != "Custom"){
            this.all_skills[skills_of_type.index].skills.push(skill);
          }
          // this.success_text = "Tag Deleted"
          // this.success_snack = true;
        }else{
          this.failure_text = "Sth is wrong";
          this.failure_snack = true;
        }
      });
    },
    enableSnack(snack){
      if(snack == "video_snack")
        this.video_snack = true;
      else if(snack == "failure_snack"){
        this.failure_text = "Sth is wrong";
        this.failure_snack = true;
      }
    },
    editSuccess(){
      this.current_step = 2;
    },
    addToFav(user){
      this.changeFav(user, true);
    },
    deleteFromFav(user){
      this.changeFav(user, false);
    },
    changeFav(user, boolVal){
      this.users[user.pk].follow = boolVal;
      this.backup_all_users[user.pk].follow = boolVal;
      this.headerUpdate = !this.headerUpdate;
    },
    setRole(role){
      this.roleBtnLoading = true;
      axios.post('/users/api/choose_role/',{"role":role}).then(response => {
        this.roleDialog = false;
        this.roleBtnLoading = false;
        if(response.data.success){
          this.success_text = "恭喜你成为" + role + "!";
          this.success_snack = true;
          this.headerUpdate = !this.headerUpdate;
          this.getAllUsers();
        }
        else if(response.data.message == "You don't have enough course comments."){
          this.failure_text = "你大概是没填够三条大于15字的HoosMyProfessor课程评价";
          this.failure_snack = true;
        }
        else{
          this.failure_text = "Sth is wrong. 你似乎发现了神奇的bug";
          this.failure_snack = true;
        }
      });
      
    },
    checkMentorRequirements(){
      return axios.get('/users/api/check_mentor_requirements/',{params: {}}).then(response => {
        this.mentorBtnLoading = false;
        return response.data.valid;
      });
    },
    openRoleDialog(role){
      if(role == "Mentor"){
        this.mentorBtnLoading = true;
        this.checkMentorRequirements().then(valid =>{
          if(!valid){
            this.failure_text = "你本学期大概是没填够三条大于15字的HoosMyProfessor课程评价";
            this.failure_snack = true;
          }
          else{
            this.dialogRole = role;
            this.roleDialog = true;
            this.getSkills();
          }
        });
      }
      else{
        this.dialogRole = role;
        this.roleDialog = true;
        this.getSkills();
      }
    },
    add_tag(tag){
      this.tags.push(tag);
    },
    del_tag(tag){
      this.tags.splice(this.tags.indexOf(tag), 1);
    },
    onKeydown(e) {
      if(e.keyCode == 13 && this.query.length > 1){
        this.add_tag(this.query);
        this.query = ""
      }
    },
    openUserDialog(index){
      this.dialog_user_index = index;
      // this.d_user = JSON.parse(JSON.stringify(user));
      if(this.dialog_user_index != -1){
        Vue.nextTick().then(function(){
          document.getElementsByClassName('v-dialog')[0].scrollTop = 0;
        })
      }
      this.userDialog = true;
    },
    closeUserDialog(){
      this.userDialog = false;
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
    },
    getAllUsers(){
      axios.get('/users/api/get_all_users/',{params: {}}).then(response => {
        this.backup_all_users = JSON.parse(JSON.stringify(response.data.users));
        this.users = JSON.parse(JSON.stringify(response.data.users));
        this.backup_user_idxs = Object.keys(this.users);
        this.shuffleArray(this.backup_user_idxs);
        this.user_idxs = this.backup_user_idxs.slice()
        this.request_user = response.data.request_user;
        this.loaded = true;
      });
    },
    fuzzy_search(tmp_user_idxs, key_arr, field_query){
      if(tmp_user_idxs.length == 0)
        return [];
      var return_all_users = [];
      const ref = this;
      for(let i = 0; i < key_arr.length; i++){
        let result = tmp_user_idxs.reduce((prev, pk) => {
          prev[pk] = ref.users[pk][key_arr[i]];
          return prev;
        }, {});
        
        let score_result = this.fuzz.extract(field_query, result, this.options);
        score_result = score_result.map((x) => x[2])
        return_all_users = return_all_users.concat(score_result);
        // console.log(key_arr[i],"---",return_all_users);
      }
      return Array.from(new Set(return_all_users));
    },
    fuzzy_search_skill(tmp_user_idxs, field_query){
      if (tmp_user_idxs.length == 0)
        return [];
      var return_all_users = {};
      for(let i = 0;i < tmp_user_idxs.length; i++){
        let tmp_skills = this.users[tmp_user_idxs[i]].skills;
        let tmp_skill_arr = tmp_skills.flatMap((skills_of_type) => skills_of_type.skills.map((skill) => skill.name));
        if(tmp_skill_arr.length > 0){
          let score_result = this.fuzz.extract(field_query, tmp_skill_arr, this.options);
          if(score_result.length > 0){
            return_all_users[tmp_user_idxs[i]] = score_result.length;
          }
        }
      }
      return return_all_users;
    },
    user_list_filter(tags){
      var tmp_user_idxs = this.backup_user_idxs.slice()
      var ref = this;
      let searchTag = false;
      tags.forEach(function(tag) {
        let colon_index = tag.indexOf(":");
        if(colon_index != -1 && colon_index != tag.length){
          let field_tag = tag.substring(0, colon_index).toLowerCase();
          let field_query = tag.substring(colon_index + 1).toLowerCase();
          // console.log("TAG:", field_tag)
          // console.log("Query:", typeof field_query)
          if(field_tag === "name"){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['first_name','last_name'], field_query);
          }
          else if(["role"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['role'], field_query);
          }
          else if(["first_name", "first name", "first"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['first_name'], field_query);
          }
          else if(["last_name", "last name", "last"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['last_name'], field_query);
          }
          else if(["gender","sex"].indexOf(field_tag) != -1){
            let tmp_scorer = ref.options.scorer;
            ref.options.scorer = ref.fuzz.token_sort_ratio;
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['sex'], field_query);
            ref.options.scorer = tmp_scorer;
          }
          else if(["birth date", "birth_date", "birthdate","birth","date"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['birth_date'], field_query);
          }
          else if(["loc", "location"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['location'], field_query);
          }
          else if(["major"].indexOf(field_tag) != -1){
            let tmp_cutoff = ref.options.cutoff;
            ref.options.cutoff = 90;
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['major', 'major_two', 'minor'], field_query);
            ref.options.cutoff = tmp_cutoff;
          }
          else if(["year"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['year'], field_query);
          }
          else if(["bio"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['bio'], field_query);
          }
          else if(["email"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['email'], field_query);
          }
          else if(["wechat"].indexOf(field_tag) != -1){
            tmp_user_idxs = ref.fuzzy_search(tmp_user_idxs, ['wechat'], field_query);
          }
        }
        else{
          searchTag = true
          let tmp_kv_users = ref.fuzzy_search_skill(tmp_user_idxs, tag.toLowerCase());
          tmp_user_idxs = Object.entries(tmp_kv_users)
                .map(([key, value]) => ({ pk: key, tag_num: value }))
                .sort((a, b) => a.tag_num - b.tag_num)
                .map((item) => item.pk)
        }
      });
      if (!searchTag) this.shuffleArray(tmp_user_idxs);
      this.user_idxs = tmp_user_idxs;
    },
    get_users_by_sim(){
      let req_user = this.users[this.request_user.pk];
      let other_users_pks = this.user_idxs.filter(pk => pk !== this.request_user.pk);
      for(const pk of other_users_pks){
        this.users[pk]["score"] = parseFloat((this.similarity_between(req_user, this.users[pk])*100).toFixed(2));
      }
      const ref = this;
      this.user_idxs = this.user_idxs.sort((a, b) => {
        return ref.users[b].score - ref.users[a].score
      })
    },
    similarity_between(a, b){
      if (!("skills" in a) || !("skills" in b)){
        return 0;
      }
      let a_skills = a.skills;
      let b_skills = b.skills;
      let total_length = 0;
      let a_length = 0;
      let b_length = 0;
      let sims = [];
      for (const skills_of_type of a_skills) {
        total_length += this.scaler(skills_of_type.skills.length);
        a_length += skills_of_type.skills.length;
      }
      b_length = b_skills.reduce((x, y) => x + y.skills.length, 0)
      for (let i = 0; i < a_skills.length; i++) {
        if(a_skills[i].skills.length > 0 && b_skills[i].skills.length > 0){
          let a_tmp_names = a_skills[i].skills.map(obj => obj.name);
          let b_tmp_names = b_skills[i].skills.map(obj => obj.name);
          let tmp_skill_list = Array.from(new Set(a_tmp_names.concat(b_tmp_names)));
          let a_vec = tmp_skill_list.map(obj => a_tmp_names.indexOf(obj) !== -1 ? 1 : 0)
          let b_vec = tmp_skill_list.map(obj =>  b_tmp_names.indexOf(obj) !== -1 ? 1 : 0)
          let cosine_scaler = 1-(Math.abs(a_tmp_names.length/a_length - b_tmp_names.length/b_length) + Math.abs(a_tmp_names.length - b_tmp_names.length)/tmp_skill_list.length)/2;
          sims.push(this.cosine_sim(a_vec, b_vec) * (cosine_scaler) * this.scaler(a_tmp_names.length)/total_length);
        }
      }
      return sims.reduce(function(a,b){ return a + b; }, 0);
    },
    cosine_sim(u,v){
      if(u.length != v.length){
        // console.log("what the f*** are you doing?(Cosine)");
        return 0;
      }
      let uv = 0;
      let u_len = 0;
      let v_len = 0;
      for(let i = 0; i < u.length;i++){
        uv += u[i]*v[i];
        u_len += u[i]*u[i];
        v_len += v[i]*v[i]
      }
      return uv/Math.sqrt(u_len)/Math.sqrt(v_len);
    },
    scaler(x){
      return Math.pow((x+1),(2/3.0))-Math.pow((x+1),(-1/8.0));
    },
  },
  mounted(){
    this.fuzz = require('fuzzball');
    this.options = {
      scorer: this.fuzz.partial_ratio,
      cutoff: 80,
    },
    this.getAllUsers();
  },
};
</script>

<style>

  .tag-percent {
    display: flex;
  }

  .tag-percent__span{
    font-size: 14px;
    padding: 2px 8px;
    border-radius: 5px;
    margin: 5px 7px 5px 0px;
    font-family: Gill Sans, sans-serif;
    color: #fff;
  }

  .tag-percent__label {
    width: 200px;
    display: inline-flex;
    justify-content: flex-end;
    align-items: flex-start;
    flex: 0 0 auto;
    box-sizing: border-box;
  }

  /* .tag-percent__value {
    
  } */

  .stepper-tags-text{
    font-weight: 500 !important;
    color:#7e7e7e;
    font-family: Roboto,sans-serif !important;
  }

  .stepper-continue-btn{
    margin: 10px 5px 2px 3px;
    float: right;
  }

  .your-tags{
    color: #8f39ff;
    font-family: Palatino, URW Palladio L, serif;
  }

  .skill-type-text{
    color: #32a49a;
    font-family: Palatino, URW Palladio L, serif;
  }

  .skill-tags{
    display: flex;
    flex-flow: row wrap;
    width:100%;
    margin: 5px 0px 20px 0px;
  }

  .stepper-card{
    margin: 5px;
    overflow: scroll;
    min-height: 300px;
    max-height: 450px;
  }

  .content-div::before{
    content: ' ';
    position: fixed;
    background: url('../assets/static/css/images/cloud_bg_new_02.jpg') no-repeat center center;
    /* background-attachment: fixed; */
    /* background-position: center center; */
    background-size: cover;
    will-change: transform;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }

  .top-part-wrapper{
    padding: 45px 0px 30px 0px;
    color:#000000;
    width:100%;
  }

  .checkbox-div{
    margin: 0 auto;
    width: 80%;
    max-width: 600px;
    display: flex;
    flex-flow: row wrap;
  }
  .muted-text{
    color:rgb(158, 158, 158) !important;
  }

  .title-text{
    color:#32a49a; 
    font-size:45px;
    letter-spacing: 0.06em;
    font-weight: 300;
    font-family: "Roboto Light", sans-serif;
  }

  .all-buttons{
    margin: 5px 0px 0px 0px;
    text-align: center;
  }

  .search-tags{
    display: flex;
    flex-flow: row wrap;
    width:80%;
    max-width: 600px;
    margin: 12px auto;
  }

  .search-tag{
    color:#32a49a;
    /* background-color: #F2B69D 70%; */
    box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
    padding: 5px 5px 5px 9px;
    border-radius: 5px;
    margin: 5px 7px 5px 0px;
  }

  .search-tag-remove{
    margin:0px 1px 0px 4px;
  }

  span.search-tag-remove:hover{
    color: #494949;
  }

  .search-form {
    /* border:1px solid #728181; */
    position: relative;
    /* top: 50%;
    left: 50%; */
    margin: 0 auto;
    /* width: 80%;
    max-width: 600px; */
    height: 40px;
    border-radius: 5px;
    box-shadow: 0 2px 5px 0 rgba(0,0,0,.16), 0 2px 10px 0 rgba(0,0,0,.12);
    /* transform: translate(-50%, -50%); */
    background: #fff;
    transition: all 0.3s ease;
  }

  .search-icon{
    padding:12px 10px 9px 14px;
  }

  .search-input {
    position: absolute;
    top: 10px;
    left: 15px;
    font-size: 14px;
    background: none;
    color: #5a6674;
    width: 85%;
    height: 20px;
    border: none;
    appearance: none;
    outline: none;
  }

  .v-stepper__content{
    padding: 16px;
  }

  @media (min-width: 1025px) {
    
  }


  @media (min-width: 768px) and (max-width: 1024px) {
    
  }

  @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
    
  }


  @media (min-width: 10px) and (max-width: 767px) {
    .stepper-card{
      margin: 2px;
      max-height: 380px;
    }

    .v-stepper__content{
      padding: 12px;
    }

    .stepper-continue-btn{
      margin: 10px 2px 1px 4px;
    }

    .title-text{
      font-size:35px !important;
    }
  }

</style>
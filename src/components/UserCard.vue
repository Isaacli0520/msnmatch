<template>
  <v-card
    v-if="!new_ui"
    color="white"
    light
    :elevation="3"
    :ripple="false"
    @click="openUserDialog()">
    <v-img 
      :aspect-ratio="1"
      :src="user.picture">
    </v-img>
    <v-divider></v-divider>
    <div style="padding-top: 10px; padding-bottom:0px;">
      <div class="title-div">
        <span class="cus-title" style="float:left;">{{full_name}}</span>
        <span v-if="'matched' in user && user.matched" class="card-tag match-tag">Matched</span>
        <span v-if="(user.video && user.video.length)" class="card-tag video-tag">Video</span>
        <span v-if="!superadmin && user.follow" class="card-tag fav-tag">Fav</span>
        <span v-if="display_role" :class="['card-tag', user.role=='Mentor' ? 'mentor-tag':'', user.role=='Mentee' ? 'mentee-tag':'']">{{user.role}}</span>
      </div>
    </div>
    <div class="major-div">
      <div class="cus-subtitle" v-if="user.major">{{ user.major }}</div>
      <div class="cus-subtitle" v-if="user.major_two">{{ user.major_two }}</div>
      <div class="cus-sim" v-if="user.score !== 0">Score:{{ user.score }}%</div>
    </div>
  </v-card>
  <v-card
    v-else
    color="white"
    light
    rounded="lg"
    :ripple="false"
    :elevation="3"
    @click="openUserDialog()"
  >
    <div class="d-flex flex-no-wrap justify-space-between">
      <div class="card-left-div">
        <div>
          <div class="cus-title-new" >{{full_name}}</div>
          <!-- <v-card-subtitle v-if="user.major">{{ user.major }}</v-card-subtitle> -->
          <div class="cus-subtitle-new" v-if="user.major">{{ user.major }}</div>
          <div class="cus-subtitle-new" v-if="user.major_two">{{ user.major_two }}</div>
        </div>
        <div class="bottom-tags">
          <span v-if="'matched' in user && user.matched" class="card-tag match-tag">Matched</span>
          <span v-if="user.video && user.video.length" class="card-tag video-tag">Video</span>
          <span v-if="!superadmin && user.follow" class="card-tag fav-tag">Fav</span>
          <span v-if="display_role" :class="['card-tag', user.role=='Mentor' ? 'mentor-tag':'', user.role=='Mentee' ? 'mentee-tag':'']">{{user.role}}</span>
        </div>
      </div>
      <v-avatar
        size="170"
        rounded
        class="cus-avatar"
      >
        <v-img 
          :aspect-ratio="1"
          :src="user.picture">
        </v-img>
      </v-avatar>
    </div>
  </v-card>
</template>

<script>

export default{
  props: {
    new_ui: {
      type:Boolean,
      default:false,
    },
    superadmin:{
      type:Boolean,
      default:false,
    },
    user:{
      type:Object,
      default:null,
    },
    user_index:{
      type:String,
      default:"0",
    },
    display_role:{
      type:Boolean,
      default:true,
    }
  },
  data(){
    return{
    }
  },
  components:{
  },
  watch:{
  },
  computed:{
    full_name(){
      if(this.isChinese(this.user.first_name) && this.isChinese(this.user.last_name)){
        return this.user.last_name + this.user.first_name;
      }
      else{
        return this.user.first_name + " " + this.user.last_name
      }
    },
  },
  methods:{
    openUserDialog(){
      this.$emit('open-user-dialog', this.user_index);
    },
    isChinese(str){
      return /[\u3400-\u9FBF]/.test(str);
    }
  },
  mounted(){
  },
}
</script>


<style scoped>
  .title-div{
    display:block; 
    height:28px; 
    line-height:28px;
    clear:both;
    padding: 0px 16px 0px 16px;
  }

  .cus-avatar {
    box-shadow: -1px 0px 3px -2px rgb(0 0 0 / 20%), -1px 0px 4px 0px rgb(0 0 0 / 14%), -1px 0px 8px 0px rgb(0 0 0 / 12%) !important;
    border-radius:0px 8px 8px 0px !important;
  }

  .cus-title-new{
    padding: 12px 0px 4px 14px;
    font-family: "Roboto", sans-serif !important;
    font-weight: 700 !important;
    align-items: center;
    font-size: 19px;
    letter-spacing: 0.0125em;
  }

  .cus-subtitle-new {
    font-weight: 300 !important;
    font-size:13px !important;
    color: rgb(117, 117, 117);
    letter-spacing: 0.007em;
    padding: 2px 8px 0px 14px;
  }

  .cus-title{
    font-family: "Roboto", sans-serif !important;
    font-weight: 700 !important;
    align-items: center;
    font-size: 18px;
    letter-spacing: 0.0125em;
  }

  .card-left-div {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .bottom-tags {
    align-self: flex-start;
    line-height: 28px;
    padding: 12px;
  }

  .card-tag{
    float: right;
    font-family: "Roboto", sans-serif !important;
    font-weight: 700 !important;
    align-items: center;
    font-size: 13px;
    letter-spacing: 0.0125em;
    padding: 0px 6px 0px 6px;
    color: white;
    border-radius: 5px;
  }

  .card-tag + .card-tag {
    margin-right: 3px;
  }

  .match-tag{
    background-color: #ffc13c;
  }

  .video-tag{
    background: rgb(50,39,228);
    background: linear-gradient(45deg, rgba(50,39,228,1) 0%, rgba(255,0,251,1) 100%);
  }

  .fav-tag{
    background-color: rgb(255, 78, 55);
  }
  .mentee-tag{
    background: #00C853;
  }
  .mentor-tag{
    background: #2979FF;
  }

  .cus-sim{
    font-weight: 700 !important;
    font-size:15px !important;
    color: rgb(255, 168, 37);
    letter-spacing: 0.007em;
    padding: 2px 16px 0px 16px;
  }

  .cus-subtitle{
    font-weight: 400 !important;
    font-size:15px !important;
    color: rgb(117, 117, 117);
    letter-spacing: 0.007em;
    padding: 2px 16px 0px 16px;
  }

  .major-div{
    display:block;
    padding-bottom:10px !important;
  }

</style>
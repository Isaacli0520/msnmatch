<template>
    <v-card
        color="white"
        light
        :elevation="3"
        :ripple="false"
        @click=openUserDialog>
        <v-img 
            aspect-ratio="1.5"
            contain
            :src="user.picture">
        </v-img>
        <!-- <img :src="user.picture" style="width:100%;"> -->
        <v-divider></v-divider>
        <!-- <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title> -->
        <div style="padding-top: 10px; padding-bottom:0px;">
            <div class="title-div">
                <span class="cus-title" style="float:left;">{{user.first_name + " " + user.last_name}}</span>
                <span v-if="user.follow" class="role-title fav-title" style="float:right;">Fav</span>
                <span v-if="display_role" :class="['role-title', user.role=='Mentor' ? 'mentor-title':'', user.role=='Mentee' ? 'mentee-title':'']" style="float:right;">{{user.role}}</span>
            </div>
        </div>
        <div class="major-div">
            <div class="cus-subtitle" v-if="user.major">{{ user.major }}</div>
            <div class="cus-subtitle" v-if="user.major_two">{{ user.major_two }}</div>
            <div class="cus-sim" v-if="user.score">Score:{{ user.score }}%</div>
        </div>
    </v-card>
</template>

<script>

export default{
    props: {
        user:{
            type:Object,
            default:null,
        },
        user_index:{
            type:Number,
            default:-1,
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
        
    },
    methods:{
        openUserDialog(){
            this.$emit('open-user-dialog', this.user_index);
        },
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

    .cus-title{
        font-family: "Roboto", sans-serif !important;
        font-weight: 700 !important;
        align-items: center;
        font-size: 18px;
        letter-spacing: 0.0125em;
    }

    .role-title{
        font-family: "Roboto", sans-serif !important;
        font-weight: 700 !important;
        align-items: center;
        font-size: 13px;
        letter-spacing: 0.0125em;
        padding: 0px 6px 0px 6px;
        margin-left:3px;
        color: white;
        border-radius: 5px;
    }

    .fav-title{
        background-color: rgb(255, 78, 55);
    }

    .mentee-title{
        background-color: rgb(61, 199, 80);
    }

    .mentor-title{
        background-color: rgb(65, 194, 211);
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
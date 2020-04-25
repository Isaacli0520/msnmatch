<template>
    <v-card
        color="white"
        light
        :ripple="false"
        @click=openUserDialog>
        <v-img 
        aspect-ratio="1.5"
        contain
        :src="user.picture">
        </v-img>
        <v-divider></v-divider>
        <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title>
        <div class="cus-subtitle" v-if="user.major">{{ user.major }}</div>
        <div class="cus-subtitle major-two" v-if="user.major_two">{{ user.major_two }}</div>
        <!-- <v-card-text v-if="item.sold">
            <div class="item-tags">
                <span class="item-tag item-tag-sold">Sold</span>
                <template v-if="!item.sold">
                    <span v-if="item.condition=='New'" class="item-tag item-tag-new">New</span>
                    <span v-if="item.condition=='Slightly Used'" class="item-tag item-tag-slightly-used">Slightly Used</span>
                    <span v-if="item.pickup" class="item-tag item-tag-pickup">Pickup</span>
                    <span v-if="item.delivery" class="item-tag item-tag-delivery">Delivery</span>
                </template>
            </div>
        </v-card-text> -->
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


<style lang="css">
    .v-card__title{
        font-family: "Roboto", sans-serif !important;
        font-weight: 700 !important;
        padding-bottom: 0px;
        padding-top: 10px;
    }

    .cus-subtitle{
        font-weight: 400 !important;
        font-size:15px !important;
        color: rgb(117, 117, 117);
        letter-spacing: 0.007em;
        padding: 0px 16px 3px 16px;
    }

    .major-two{
        padding: 0px 16px 10px 16px !important;
    }


    .item-tags{
        margin: -3px 0px 0px 0px;
        display: flex;
        flex-flow: row wrap;
        width:100%;
    }

    .item-tag{
        font-size: 12px;
        font-weight: 700;
        padding: 2px 6px 2px 6px;
        margin: 5px 4px 0px 0px;
        border-radius: 4px;
    }

</style>
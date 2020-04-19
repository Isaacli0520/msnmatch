<template>
    <v-card
        color="white"
        light
        :ripple="false"
        @click=openUserDialog(user)>
        <v-img 
        aspect-ratio="1.5"
        contain
        :src="user.picture">
        </v-img>
        <v-divider></v-divider>
        <v-card-title>{{user.first_name + " " + user.last_name}}</v-card-title>
        <v-card-subtitle class="cus-subtitle">{{ user.major ? user.major : "None" }}</v-card-subtitle>
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
        openUserDialog(user){
            this.$emit('open-user-dialog', user);
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
    }

    .cus-subtitle{
        /* font-weight: 600 !important; */
        font-size:17px !important;
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
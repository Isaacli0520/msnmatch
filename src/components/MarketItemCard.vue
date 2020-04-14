<template>
    <v-card
        color="white"
        light
        @click=openItemDialog()>
        <v-img 
        aspect-ratio="1.5"
        contain
        :src="item.image">
        </v-img>
        <v-divider></v-divider>
        <v-card-title>{{shortenString(item.name)}}</v-card-title>
        <v-card-subtitle class="cus-subtitle">${{item.price}}</v-card-subtitle>
        <!-- <v-card-text>
            <div class="item-tags">
                <span v-if="item.sold" class="item-tag item-tag-sold">Sold</span>
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
        item:{
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
        openItemDialog(){
            this.$emit('open-item-dialog');
        },
        shortenString(str){
            if(str.length >= 16){
                return str.substr(0, 16) + "...";
            }
            else{
                return str
            }
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

    .item-tag-pickup{
        color:#ffffff;
        background: rgba(74, 185, 236, 0.993);
    }

    .item-tag-slightly-used{
        color:#ffffff;
        background: rgba(248, 197, 28, 0.993);
    }

    .item-tag-new{
        color:#ffffff;
        background: rgba(255, 111, 28, 0.993);
    }

    .item-tag-sold{
        color:#ffffff;
        background: rgba(158, 63, 202, 0.993);
    }

    .item-tag-delivery{
        color:#ffffff;
        background: rgba(37, 190, 17, 0.993);
    }
</style>
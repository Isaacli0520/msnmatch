<template>
    <v-dialog v-model="itemDialog" v-if='d_item' min-width="350px">
        <v-card>
            <v-card-text>
            <v-row>
                <v-col cols="12" sm="6" md="7" lg="7" xl="7">
                    <v-card>
                        <v-img
                            aspect-ratio="1.3"
                            contain  
                            :src="d_item.image">
                        </v-img>
                        <v-divider></v-divider>
                        <v-card-title>{{d_item.name}}</v-card-title>
                    </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="5" lg="5" xl="5">
                    <v-card style="margin-bottom:15px;">
                        <v-card-title>Item Details</v-card-title>
                        <v-divider></v-divider>
                        <v-card-text>
                            <table class="cus-table">
                                <tbody>
                                    <tr>
                                        <td>Price</td>
                                        <td style="font-size:17px !important; color:black !important;" class="cus-td">${{ d_item.price }}</td>
                                    </tr>
                                    <tr>
                                        <td>Condition</td>
                                        <td class="cus-td">{{ condition_dict[d_item.condition] }}</td>
                                    </tr>
                                    <!-- <tr>
                                        <td>Category</td>
                                        <td>{{ category_dict[d_item.category] }}</td>
                                    </tr> -->
                                    <tr>
                                        <td>Pickup</td>
                                        <td :class="['cus-td',d_item.pickup ? 'available' : 'unavailable']">{{ d_item.pickup ? 'Available' : 'Not Available' }}</td>
                                    </tr>
                                    <tr>
                                        <td>Delivery</td>
                                        <td :class="['cus-td',d_item.delivery ? 'available' : 'unavailable']">{{ d_item.delivery ? 'Available' : 'Not Available' }}</td>
                                    </tr>
                                    <tr>
                                        <td style="vertical-align:top; padding: 4px 16px 15px 16px !important;">Description</td>
                                        <td class="description-td description-text">{{ d_item.description }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </v-card-text>
                    </v-card>
                    <v-card>
                        <v-card-title>Seller Info</v-card-title>
                        <v-divider></v-divider>
                        <v-card-text>
                            <table class="cus-table">
                                <tbody>
                                    <tr>
                                        <td>Seller</td>
                                        <td>{{ d_item.seller_name }}</td>
                                    </tr>
                                    <tr v-if="d_item.wechat">
                                        <td>WeChat ID</td>
                                        <td>{{ d_item.wechat }}</td>
                                    </tr>
                                    <tr>
                                        <td>Email</td>
                                        <td>{{ d_item.email }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="red darken-1" v-if="edit" outlined @click="openDeleteDialog">Delete</v-btn>
                            <v-btn color="green darken-1" v-if="edit" outlined @click="openSoldDialog">Sold</v-btn>
                            <v-btn color="green darken-1" v-if="edit" outlined @click="openEditDialog">Edit</v-btn>
                            <!-- <v-btn color="purple darken-1" v-if="!edit" outlined @click="goToItem(d_item)">Detail</v-btn> -->
                            <v-btn color="blue darken-1" outlined @click="closeDialog">Close</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script>

export default{
    props: {
        d_item:{
            type:Object,
            default:null,
        },
        itemDialog:{
            type:Boolean,
            default:false,
        },
        edit:{
            type:Boolean,
            default:false,
        }
    },
    data(){
        return{
            condition_dict:{
                "slightlyused":"Slightly Used",
                "new":"New",
                "dysfunctional":"Dysfunctional",
                "used":"Used",
            },
            category_dict:{
                "electronics":"Electronics",
                "housing":"Housing",
                "pets":"Pets",
                "miscellaneous":"Miscellaneous",
                "furniture":"Furniture",
                "clothing":"Clothing",
                "textbooks":"Textbooks",
                "schoolsupplies":"School Supplies"
            }

        }
    },
    components:{
    },
    watch:{
    },
    computed:{
        verticalBool () {
            switch (this.$vuetify.breakpoint.name) {
            case 'xs': return false
            case 'sm': return false
            case 'md': return true
            case 'lg': return true
            case 'xl': return true
            }
            return false;
        },
    },
    methods:{
        openEditDialog(){
            this.$emit('open-edit-dialog', this.d_item);
        },
        openSoldDialog(){
            this.$emit('open-sold-dialog', this.d_item);
        },
        openDeleteDialog(){
            this.$emit('open-delete-dialog', this.d_item);
        },
        closeDialog(){
            this.$emit('close-dialog');
        },
        goToItem(item){
            window.location.href = "/market/item/" + item.id;
        }
    },
    mounted(){
    },
}
</script>


<style lang="css">
    
    .cus-table{
         /* font-family: "Times New Roman", Times, serif !important; */
    }

    .theme--light.v-card > .v-card__text, .theme--light.v-card .v-card__subtitle{
        color: rgba(0, 0, 0, 1);
    }

    tr td:first-child{
        color: rgb(134, 132, 132);
    }

    tr td:last-child{
        color: rgb(0, 0, 0);
    }

    .description-td{
        padding: 4px 16px 15px 16px !important;
        /* font-family: "Times New Roman", Times, serif !important; */
    }

    .available{
        color: rgb(14, 179, 14) !important;
    }

    .unavailable{
        color: rgb(172, 168, 168) !important;
    }

    .table-title{
        font-size:20px !important;
        font-weight: 700 !important;
    }
    .cus-td{
        font-weight: 600 !important;
    }

    .v-card__title{
        font-weight: 600 !important;
    }

    .v-card__text td{
        font-family: "Roboto", sans-serif !important;
        font-size: 15px !important;
        padding: 4px 16px;
    }

    td:not(.cus-td):not(.description-text){
        font-size: 15px !important;
        padding: 4px 16px;
    }

    .dialog-head-text{
        /* font-family: "Times New Roman", Times, serif !important;  */
        padding-left:31px;
        font-size: 28px !important;
        font-weight:700 !important;
    }
</style>
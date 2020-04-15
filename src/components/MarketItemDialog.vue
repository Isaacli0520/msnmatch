<template>
    <v-dialog v-model="itemDialog" v-if='d_item' min-width="350px">
        <v-card>
            <v-row no-gutters>
                <!-- xs="12" sm="12" md="8" lg="8" xl="8" -->
                <v-col cols="12" sm="6" md="8" lg="8" xl="8" class="img-col">
                <v-img
                aspect-ratio="1.3"
                contain  
                :src="d_item.image">
                </v-img>
                </v-col>
                <!-- xs="12" sm="12" md="4" lg="4" xl="4" -->
                <v-col cols="12" sm="6" md="4" lg="4" xl="4">
                <div>
                    <v-card-title class="dialog-head-text">{{d_item.name}}</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <div style="padding:0px 5px 8px 16px;" class="table-title">Item Details</div>
                        <table class="cus-table">
                            <tbody>
                                <tr>
                                    <td>Price</td>
                                    <td style="font-size:18px !important; color:red !important;" class="cus-td">${{ d_item.price }}</td>
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
                        <v-divider></v-divider>
                        <div style="padding:13px 5px 8px 16px;" class="table-title">Seller Info</div>
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
                        <v-btn color="yellow darken-1" v-if="edit" outlined @click="openSoldDialog">Sold</v-btn>
                        <v-btn color="green darken-1" v-if="edit" outlined @click="openEditDialog">Edit</v-btn>
                        <v-btn color="blue darken-1" outlined @click="closeDialog">Close</v-btn>
                    </v-card-actions>
                </div>
                </v-col>
            </v-row>
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
    },
    mounted(){
    },
}
</script>


<style lang="css">
    .img-col{
        border-right: 1px solid rgb(226, 224, 224);
        border-bottom: 1px solid rgb(226, 224, 224);
    }
    
    .cus-table{
         /* font-family: "Times New Roman", Times, serif !important; */
    }

    .description-td{
        padding: 4px 16px 15px 16px !important;
        /* font-family: "Times New Roman", Times, serif !important; */
    }

    .available{
        color: rgb(14, 179, 14);
    }

    .unavailable{
        color: rgb(172, 168, 168);
    }

    .table-title{
        font-size:20px !important;
        font-weight: 700 !important;
    }
    .cus-td{
        font-weight: 600 !important;
    }

    .v-card__text td{
        font-size: 15px !important;
        padding: 4px 16px;
    }

    td:not(.cus-td):not(.description-text){
        font-family: "Times New Roman", Times, serif !important; 
        font-size: 15px !important;
        padding: 4px 16px;
    }

    .dialog-head-text{
        /* font-family: "Times New Roman", Times, serif !important;  */
        font-size: 28px !important;
        font-weight:700 !important;
    }
</style>
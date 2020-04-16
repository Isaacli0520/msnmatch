<template>
    <v-app>
        <market-header></market-header>
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
            <v-container v-if="!item && loaded" fluid fill-height>
                <v-layout 
                    align-center
                    justify-center>
                    <div class="item-not-exist">
                        Item does not exist~~
                    </div>
                </v-layout>
            </v-container>
            <v-container v-if="item && loaded" fluid grid-list-lg>
                <v-row >
                    <v-col cols="12" sm="6" md="5" lg="5" xl="5">
                        <v-card>
                            <v-img
                            aspect-ratio="1.3"
                            contain  
                            :src="item.image">
                            </v-img>
                            <v-card-title>{{item.name}}</v-card-title>
                        </v-card>
                    </v-col>
                    <v-col cols="12" sm="6" md="7" lg="7" xl="7">
                        <v-card style="margin-bottom:15px;">
                            <v-card-title>Item Details</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                <table class="cus-table">
                                    <tbody>
                                        <tr>
                                            <td>Price</td>
                                            <td style="font-size:17px !important; color:black !important;" class="cus-td">${{ item.price }}</td>
                                        </tr>
                                        <tr>
                                            <td>Condition</td>
                                            <td class="cus-td">{{ condition_dict[item.condition] }}</td>
                                        </tr>
                                        <!-- <tr>
                                            <td>Category</td>
                                            <td>{{ category_dict[item.category] }}</td>
                                        </tr> -->
                                        <tr>
                                            <td>Pickup</td>
                                            <td :class="['cus-td',item.pickup ? 'available' : 'unavailable']">{{ item.pickup ? 'Available' : 'Not Available' }}</td>
                                        </tr>
                                        <tr>
                                            <td>Delivery</td>
                                            <td :class="['cus-td',item.delivery ? 'available' : 'unavailable']">{{ item.delivery ? 'Available' : 'Not Available' }}</td>
                                        </tr>
                                        <tr>
                                            <td style="vertical-align:top; padding: 4px 16px 15px 16px !important;">Description</td>
                                            <td class="description-td description-text">{{ item.description }}</td>
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
                                            <td>{{ item.seller_name }}</td>
                                        </tr>
                                        <tr v-if="item.wechat">
                                            <td>WeChat ID</td>
                                            <td>{{ item.wechat }}</td>
                                        </tr>
                                        <tr>
                                            <td>Email</td>
                                            <td>{{ item.email }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import MarketHeader from '../components/MarketHeader'

  export default {
	data() {
        return {
            loaded:false,
            item:null,
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
                "furniture":"Furniture",
                "miscellaneous":"Miscellaneous",
                "clothing":"Clothing",
                "textbooks":"Textbooks",
                "schoolsupplies":"School Supplies"
            }
        }
	},
	components:{
        MarketHeader,
	},
	watch: {

	},
	computed:{
        item_pk: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
        getItem(item_pk){
            axios.get('/market/api/get_item/',{params: {"item_pk":item_pk}}).then(response => {
                if(response.data.success){
                    this.item = response.data.item;
                }
                this.loaded = true;
            });
        }
	},
	mounted(){
        this.getItem(this.item_pk);
	},
  };
</script>

<style>
    .v-card__title{
        font-weight: 600 !important;
    }

    tr td:first-child{
        color: rgb(134, 132, 132);
    }

    tr td:last-child{
        color: rgb(0, 0, 0);
    }

    .item-not-exist{
        font-size: 25px;
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
        padding-left:31px;
        font-size: 28px !important;
        font-weight:700 !important;
    }

</style>
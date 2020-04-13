<template>
    <v-app>
        <market-header></market-header>
        <v-content>
            <v-container fluid grid-list-lg>
                <v-layout mb-3 mr-3>
                    <v-flex > 
                        <div>
                            <span class="cus-headline-text">Market</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-layout mb-3>
                    <v-row dense>
                        <v-col
                        v-for="(item, i) in items"
                        :key="i"
                        cols="3"
                        >
                        <v-card
                            color="white"
                            light
                            @click=openItemDialog(item)
                        >
                            <v-img 
                            aspect-ratio="1.5"
                            contain
                            :src="item.image">
                            </v-img>
                            <v-card-title>{{shortenString(item.name)}}</v-card-title>
                            <v-card-subtitle >${{item.price}}</v-card-subtitle>
                            <v-card-text>
                                <div class="item-tags">
                                    <span v-if="item.condition=='New'" class="item-tag item-tag-new">New</span>
                                    <span v-if="item.condition=='Slightly Used'" class="item-tag item-tag-slightly-used">Slightly Used</span>
                                    <span v-if="item.pickup" class="item-tag item-tag-pickup">Pickup</span>
                                    <span v-if="item.delivery" class="item-tag item-tag-delivery">Delivery</span>
                                </div>
                            </v-card-text>
                        </v-card>
                        </v-col>
                    </v-row>
                </v-layout>
            </v-container>
            <v-dialog v-model="itemDialog" v-if='d_item' scrollable min-width="350px">
                <v-card>
                    <!-- <div class="d-flex flex-no-wrap justify-space-between"> -->
                    <v-layout>
                        <v-flex xs12 sm12 md8 lg8 xl8>
                        <v-img 
                        aspect-ratio="1.3"
                        contain  
                        :src="d_item.image">
                        </v-img>
                        </v-flex>
                        <v-divider vertical ml-3></v-divider>
                        <v-flex xs12 sm12 md4 lg4 xl4>
                        <div>
                            <v-card-title class="head-text">{{d_item.name}}</v-card-title>
                            <v-card-text>
                                <v-simple-table>
                                    <template v-slot:default>
                                    <tbody>
                                        <tr>
                                            <td>Price</td>
                                            <td>{{ d_item.price }}</td>
                                        </tr>
                                        <tr>
                                            <td>Condition</td>
                                            <td>{{ d_item.condition }}</td>
                                        </tr>
                                        <tr>
                                            <td>Pickup</td>
                                            <td>{{ d_item.pickup ? 'Available' : 'Not Available' }}</td>
                                        </tr>
                                        <tr>
                                            <td>Delivery</td>
                                            <td>{{ d_item.delivery ? 'Available' : 'Not Available' }}</td>
                                        </tr>
                                        <tr>
                                            <td>Description</td>
                                            <td>{{ d_item.description }}</td>
                                        </tr>
                                    </tbody>
                                    </template>
                                </v-simple-table>
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" text @click="itemDialog = false">Close</v-btn>
                            </v-card-actions>
                        </div>
                        </v-flex>
                    </v-layout>
                    <!-- </div> -->
                </v-card>
            </v-dialog>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import MarketHeader from '../components/MarketHeader'

  export default {
	data() {
        return {
            itemDialog:false,
            items:[],
            d_item:null,
        }
	},
	components:{
        MarketHeader,
	},
	watch: {

	},
	computed:{
        category: function(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
        shortenString(str){
            if(str.length >= 16){
                return str.substr(0, 16) + "...";
            }
            else{
                return str
            }
        },
        capitalizeFirstLetter(string) {
            return string[0].toUpperCase() + string.slice(1);
        },
        openItemDialog(item){
            this.d_item = item;
            this.itemDialog = true;
        },
        getCategoryItems(){
            axios.get('/market/api/get_category_items/',{params: {"category":this.category}}).then(response => {
                this.items = response.data.items;
            });
        },
	},
	mounted(){
        this.getCategoryItems();
	},
  };
</script>

<style>
    .head-text{
        font-family: "Roboto", sans-serif !important;
		font-weight: 300 !important;
        font-size:28px !important;
        margin-left: 13px;
    }

    .cus-headline-text{
		font-family: "Roboto", sans-serif;
		font-size: 2.1em;
		font-weight: 300;
		color:rgb(0, 0, 0);
		padding: 1px 12px 7px 3px;
		border-radius: 5px;
		line-height: 1.0;
	}

    .item-tags{
        margin: 0px 0px 3px 0px;
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

    .item-tag-delivery{
        color:#ffffff;
        background: rgba(37, 190, 17, 0.993);
    }

    @media (min-width: 1025px) {
        
    }


    @media (min-width: 768px) and (max-width: 1024px) {
        
    }

    @media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
        
    }


    @media (min-width: 10px) and (max-width: 767px) {
        .cus-headline-number{
            font-size: 1.3em;
        }

        .cus-headline-text{
            font-size: 1.3em;
            
        }

        .instructor-name{
            font-size:1.7em;
        }

        .instructor-topic{
            font-size:1.4em;
        }

        .v-breadcrumbs li{
        font-size:14px !important;
    }
    }

</style>
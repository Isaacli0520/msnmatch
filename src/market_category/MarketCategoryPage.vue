<template>
    <v-app>
        <market-header></market-header>
        <v-content>
            <v-container fluid grid-list-lg>
                <v-row mb-3 mr-3>
                    <v-col> 
                        <div class="cus-headline-text">{{categorymap(category)}}</div>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col>
                        <v-select
                        v-model="sortMethod"
                        :items="sortOptions"
                        label="Sort By"
                        hide-details
                        outlined>
                        </v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col
                    style="padding:6px;"
                    v-for="(item, i) in items"
                    :key="i"
                    xs="12"
                    sm="6"
                    md="4"
                    lg="4"
                    xl="2">
                    <market-item-card @open-item-dialog="openItemDialog(item)" :item="item"></market-item-card>
                    </v-col>
                </v-row>
            </v-container>
            <market-item-dialog @close-dialog="itemDialog=false" :d_item="d_item" :itemDialog="itemDialog" ></market-item-dialog>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import MarketHeader from '../components/MarketHeader'
import MarketItemDialog from '../components/MarketItemDialog'
import MarketItemCard from '../components/MarketItemCard'

  export default {
	data() {
        return {
            itemDialog:false,
            items:[],
            sortMethod:"Latest",
            sortOptions:["Latest", "Price: High to Low", "Price: Low to High"],
            d_item:null,
        }
	},
	components:{
        MarketHeader,
        MarketItemDialog,
        MarketItemCard
	},
	watch: {
        sortMethod(val){
            if(val == "Latest"){
                this.items.sort(function(a,b){
                    return b.updated - a.updated;
                });
            }
            else if(val == "Price: High to Low"){
                this.items.sort(function(a,b){
                    return b.price - a.price;
                });
            }
            else if(val == "Price: Low to High"){
                this.items.sort(function(a,b){
                    return a.price - b.price;
                });
            }
        },
	},
	computed:{
        category(){
            let url = window.location.pathname.split('/');
            return url[url.length - 2];
        },
	},
	methods: {
        categorymap(category){
            if(category=="schoolsupplies")
                return "School Supplies"
            else
                return this.capitalizeFirstLetter(category);
        },
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
        getSearchResult(query){
            axios.get('/market/api/item_search_result/',{params: {"query":query, "category":this.category}}).then(response => {
                this.items = response.data.items;
            });
        }
	},
	mounted(){
        let url = new URL(window.location.href);
        let query = url.searchParams.get("q");
        if(query != null)
            this.getSearchResult(query);
        else
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
<template>
    <v-app>
        <market-header
            @accept-disclaimer="getSearchResult(query,category)"
            @update-items="getSearchResult(query, category)"></market-header>
        <v-main>
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
            <v-container v-if="loaded" fluid grid-list-lg>
                <v-row mb-3 mr-3>
                    <v-col> 
                        <div class="cus-headline-text">Market</div>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col>
                        <v-select
                        dense
                        v-model="sortMethod"
                        :items="sortOptions"
                        label="Sort By"
                        hide-details
                        outlined>
                        </v-select>
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col v-for="(item, i) in items" :key="i"
                        cols="12" sm="6" md="4" lg="4" xl="3"
                        >
                        <market-item-card @open-item-dialog="openItemDialog(item)" :item="item"></market-item-card>
                    </v-col>
                </v-row>
            </v-container>
            <market-item-dialog @close-dialog="itemDialog=false" :d_item="d_item" v-model="itemDialog" ></market-item-dialog>
        </v-main>
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
            loaded:false,
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
        query(){
            let url = new URL(window.location.href);
            return url.searchParams.get("q");
        },
        category(){
            let url = new URL(window.location.href);
            return url.searchParams.get("c");
        }
    },
    methods: {
        openItemDialog(item){
            this.d_item = JSON.parse(JSON.stringify(item));
            this.itemDialog = true;
        },
        getAllItems(){
            axios.get('/market/api/get_all_items/',{params: {}}).then(response => {
                this.items = response.data.items;
                this.loaded = true;
            });
        },
        getSearchResult(query, category){
            axios.get('/market/api/item_search_result/',{params: {"query":query, "category":category}}).then(response => {
                this.items = response.data.items;
                this.loaded = true;
            });
        }
    },
    mounted(){
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
        justify-content: center;
        font-family: "Roboto", sans-serif;
        font-size: 2.1em;
        font-weight: 300;
        color:rgb(0, 0, 0);
        padding: 1px 12px 7px 3px;
        border-radius: 5px;
        line-height: 1.0;
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
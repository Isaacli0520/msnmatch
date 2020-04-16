<template>
    <v-app>
        <market-header
            @accept-disclaimer="getMyItems"
            @update-items="getMyItems"></market-header>
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
            <v-container v-if="loaded" fluid grid-list-lg>
                <v-row mb-3 mr-3>
                    <v-col> 
                        <div>
                            <span class="cus-headline-text">My Items</span>
                        </div>
                    </v-col>
                    <!-- <v-spacer></v-spacer>
                    <v-col>
                        <v-btn style="float: right;" color="teal lighten-1" @click="openCreateItemDialog()" outlined d-flex>Sell an Item</v-btn>
                    </v-col> -->
                </v-row>
                <v-row v-if="items.length == 0" mb-3 mr-3>
                    <v-col> 
                        <div>
                            <span class="no-item-text">Go ahead and click "Sell an Item" on the left to sell sth~</span>
                        </div>
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col
                    v-for="(item, i) in items"
                    :key="i"
                    cols="12"
                    sm="6"
                    md="4"
                    lg="4"
                    xl="3"
                    >
                    <market-item-card @open-item-dialog="openItemDialog(item)" :item="item"></market-item-card>
                    </v-col>
                </v-row>
                <template v-if="sold_items.length > 0">
                <v-row mb-3 mr-3>
                    <v-col> 
                        <div>
                            <span class="cus-headline-text">Sold Items</span>
                        </div>
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col
                    v-for="(item, i) in sold_items"
                    :key="i"
                    cols="12"
                    sm="6"
                    md="4"
                    lg="4"
                    xl="3"
                    >
                    <market-item-card @open-item-dialog="openItemDialog(item)" :item="item"></market-item-card>
                    </v-col>
                </v-row>
                </template>
            </v-container>
            <v-dialog v-model="editItemDialog" v-if="edit_item" scrollable min-width="350px" max-width="600px">
                <v-card>
                    <v-card-title>Edit Your Item</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="height: 600px;">
                        <v-form
                            ref="edit_form"
                            v-model="edit_item_form_valid">
                            <v-text-field
                            v-model="edit_item.name"
                            :counter="25"
                            :rules="nameRules"
                            label="Name"
                            required
                            ></v-text-field>

                            <v-text-field
                                v-model="edit_item.price"
                                label="Price (Dollars)"  
                                :rules="[v => (v!=undefined && v >= 0) || 'Price is required']"
                                required
                                type="number"
                            />

                            <v-select
                            v-model="edit_item.condition"
                            :items="conditions"
                            :rules="[v => !!v || 'Condition is required']"
                            label="Condition"
                            required
                            ></v-select>

                            <v-select
                            v-model="edit_item.category"
                            :items="categories"
                            :rules="[v => !!v || 'Category is required']"
                            label="Category"
                            required
                            ></v-select>

                            <v-file-input 
                            v-model="edit_item_image"
                            accept="image/*"
                            label="Upload a different image"></v-file-input>

                            <v-checkbox
                            v-model="edit_item.pickup"
                            label="Pickup"
                            ></v-checkbox>

                            <v-checkbox
                            v-model="edit_item.delivery"
                            label="Delivery"
                            ></v-checkbox>

                            <v-textarea
                                v-model="edit_item.description"
                                label="Description"
                                outlined
                                :rules="descriptionRules"
                                required
                                rows="3"
                                row-height="20"
                            ></v-textarea>
                        </v-form>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="green darken-1" :loading="editItemBtnLoading" outlined @click.prevent="editItem(edit_item, edit_item_image)">Edit</v-btn>
                        <v-btn color="blue darken-1" outlined @click="editItemDialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-dialog v-model="deleteItemDialog" v-if="delete_item" scrollable min-width="200px" max-width="600px">
                <v-card>
                    <v-card-title>Deletion</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="margin-top:21px; font-size:20px;font-weight:500;">
                        Do you really want to delete {{delete_item.name}}?
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="red darken-1" :loading="deleteItemBtnLoading" outlined @click="deleteItem(delete_item)">Delete</v-btn>
                        <v-btn color="blue darken-1" outlined @click="deleteItemDialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-dialog v-model="soldItemDialog" v-if="sold_item" scrollable min-width="200px" max-width="600px">
                <v-card>
                    <v-card-title>Sold</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="margin-top:21px; font-size:20px;font-weight:500;">
                        Is {{sold_item.name}} really sold?
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="yellow darken-1" :loading="soldItemBtnLoading" outlined @click="sellItem(sold_item)">Yes, it is sold</v-btn>
                        <v-btn color="blue darken-1" outlined @click="soldItemDialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <market-item-dialog 
                :edit="true"
                :d_item="d_item" 
                :itemDialog="itemDialog"
                @open-edit-dialog="openEditItemDialog" 
                @open-delete-dialog="openDeleteItemDialog"
                @open-sold-dialog="openSoldItemDialog"
                @close-dialog="itemDialog=false"></market-item-dialog>
        </v-content>
                <v-snackbar
            top
            v-model="delete_snack"
            color="teal darken-1"
            :timeout="3200">
            Item Deleted
        <v-btn color="cyan accent-1" text @click="delete_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="edit_snack"
            color="teal darken-1"
            :timeout="3200">
            Item Edited
        <v-btn color="cyan accent-1" text @click="edit_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="sold_snack"
            color="teal darken-1"   
            :timeout="3200">
            Item Sold
        <v-btn color="cyan accent-1" text @click="sold_snack = false"> Close </v-btn>
        </v-snackbar>
        <v-snackbar
            top
            v-model="failure_snack"
            color="red darken-1"
            :timeout="3200">
            Sth is wrong
        <v-btn color="blue" text @click="failure_snack = false"> Close </v-btn>
        </v-snackbar>
    </v-app>
</template>

<script>
import axios from 'axios'
import MarketHeader from '../components/MarketHeader'
import MarketItemDialog from '../components/MarketItemDialog'
import MarketItemCard from '../components/MarketItemCard'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
        return {
            sold_snack:false,
            edit_snack:false,
            delete_snack:false,
            failure_snack:false,

            loaded:false,
            edit_item_form_valid:true,

            editItemBtnLoading:false,
            deleteItemBtnLoading:false,
            soldItemBtnLoading:false,

            editItemDialog:false,
            soldItemDialog:false,
            deleteItemDialog:false,
            itemDialog:false,

            d_item:null,
            sold_item:null,
            delete_item:null,
            edit_item:null,
            edit_item_image:null,
            conditions:[
                {   
                    'value':'new',
                    'text':'New'
                },
                {   
                    'value':'slightlyused',
                    'text':'Slightly Used'
                },
                {   
                    'value':'used',
                    'text':'Used'
                },
                {   
                    'value':'dysfunctional',
                    'text':'Dysfunctional'
                },
            ],
            categories:[
                {   
                    'value':'electronics',
                    'text':'Electronics'
                },
                {   
                    'value':'textbooks',
                    'text':'Textbooks'
                },
                {   
                    'value':'furniture',
                    'text':'Furniture'
                },
                {   
                    'value':'schoolsupplies',
                    'text':'School supplies'
                },
                {   
                    'value':'clothing',
                    'text':'Clothing'
                },
                {   
                    'value':'housing',
                    'text':'Housing'
                },
                {   
                    'value':'pets',
                    'text':'Pet Supplies'
                },
                {   
                    'value':'miscellaneous',
                    'text':'Miscellaneous'
                },
            ],
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 25) || 'Name must be less than 25 characters',
            ],
            descriptionRules: [
                v => !!v || 'Desctiption is required',
                v => (v && v.length <= 350) || 'Desctiption must be less than 350 characters',
            ],
            items:[],
            sold_items:[],
        }
	},
	components:{
        MarketHeader,
        MarketItemDialog,
        MarketItemCard
	},
	computed:{
	},
	methods: {
        openItemDialog(item){
            this.d_item = item;
            this.itemDialog = true;
        },
        getMyItems(){
            axios.get('/market/api/get_my_items/',{params: {}}).then(response => {
                this.items = response.data.items;
                this.sold_items = response.data.sold_items;
                this.loaded = true;
            });
        },
        openSoldItemDialog(item){
            this.sold_item = item;
            this.itemDialog = false;
            this.soldItemDialog = true;
        },
        openDeleteItemDialog(item){
            this.delete_item = item;
            this.itemDialog = false;
            this.deleteItemDialog = true;
        },
        openEditItemDialog(item){
            this.edit_item = JSON.parse(JSON.stringify(item));
            this.itemDialog = false;
            this.editItemDialog = true;
        },
        sellItem(item){
            this.soldItemBtnLoading = true;
            let formData = new FormData();
            for(var key in item){
                if(key != "image"){
                    formData.append(key, item[key]);
                }
            }
            axios.post('/market/api/sell_item/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                if(response.data.success){
                    this.sold_snack = true;
                    this.soldItemBtnLoading = false;
                    this.getMyItems();
                    this.soldItemDialog = false;
                    this.sold_item = null;
                }else{
                    this.failure_snack = true;
                }
            });
        },
        deleteItem(item){
            this.deleteItemBtnLoading = true;
            let formData = new FormData();
            for(var key in item){
                if(key != "image"){
                    formData.append(key, item[key]);
                }
            }
            axios.post('/market/api/delete_item/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                if(response.data.success){
                    this.delete_snack = true;
                    this.deleteItemBtnLoading = false;
                    this.getMyItems();
                    this.deleteItemDialog = false;
                    this.delete_item = null;
                }else{
                    this.failure_snack = true;
                }
            });
        },
        editItem(item, edit_item_image){
            this.$refs.edit_form.validate();
            if(!this.edit_item_form_valid)
                return;
            this.editItemBtnLoading = true;
            let formData = new FormData();
            formData.append('image', edit_item_image);
            for(var key in item){
                if(key != "image"){
                    formData.append(key, item[key]);
                }
            }
            axios.post('/market/api/edit_item/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                if(response.data.success){
                    this.edit_snack = true;
                    this.editItemBtnLoading = false;
                    this.getMyItems();
                    this.editItemDialog = false;
                    this.edit_item = null;
                    this.edit_item_image = null;
                    // this.$refs.edit_form.resetValidation();
                }else{
                    this.failure_snack = true;
                }
            });
        },
	},
	mounted(){
	},
  };
</script>

<style>
    .item-tags{
        margin: 0px 0px 3px 0px;
        display: flex;
        flex-flow: row wrap;
        width:100%;
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

    .no-item-text{
		font-family: "Roboto", sans-serif;
		font-size: 1.6em;
		font-weight: 300;
		color:rgb(129, 127, 127);
		padding: 1px 12px 7px 3px;
		border-radius: 5px;
		line-height: 1.0;
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
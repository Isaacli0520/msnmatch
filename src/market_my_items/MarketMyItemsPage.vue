<template>
    <v-app>
        <market-header></market-header>
        <v-content>
            <v-container fluid grid-list-lg>
                <v-layout mb-3 mr-3>
                    <v-flex > 
                        <div>
                            <span class="cus-headline-text">My Items</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                    <v-btn @click="openCreateItemDialog()" d-flex>Sell an Item</v-btn>
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
                            @click="openItemDialog(item)"
                        >
                            <v-img 
                            aspect-ratio="1.5"
                            contain
                            :src="item.image">
                            </v-img>
                            <v-card-title v-text="item.name"></v-card-title>
                            <v-card-subtitle >${{item.price}}</v-card-subtitle>
                            <v-card-text>
                                <div class="item-tags">
                                    <span v-if="item.condition=='new'" class="item-tag item-tag-new">New</span>
                                    <span v-if="item.condition=='slightlyused'" class="item-tag item-tag-slightly-used">Slightly Used</span>
                                    <span v-if="item.pickup" class="item-tag item-tag-pickup">Pickup</span>
                                    <span v-if="item.delivery" class="item-tag item-tag-delivery">Delivery</span>
                                </div>
                            </v-card-text>
                        </v-card>
                        </v-col>
                    </v-row>
                </v-layout>
            </v-container>
            <v-dialog v-model="createItemDialog" scrollable min-width="350px" max-width="600px">
                <v-card>
                    <v-card-title>Sell an Item</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="height: 600px;">
                        <v-form
                            ref="form"
                            v-model="create_item_form_valid"
                            lazy-validation>
                            <v-text-field
                            v-model="item.name"
                            :counter="25"
                            :rules="nameRules"
                            label="Name"
                            required
                            ></v-text-field>

                            <v-text-field
                                v-model="item.price"
                                label="Price (Dollars)"
                                :rules="[v => (v!=undefined && v >= 0) || 'Price is required']"
                                required
                                type="number"
                            />

                            <v-select
                            v-model="item.condition"
                            :items="conditions"
                            :rules="[v => !!v || 'Condition is required']"
                            label="Condition"
                            required
                            ></v-select>

                            <v-select
                            v-model="item.category"
                            :items="categories"
                            :rules="[v => !!v || 'Category is required']"
                            label="Category"
                            required
                            ></v-select>

                            <v-file-input 
                            v-model="item.image"
                            label="Image"></v-file-input>

                            <v-checkbox
                            v-model="item.pickup"
                            label="Pickup"
                            ></v-checkbox>

                            <v-checkbox
                            v-model="item.delivery"
                            label="Delivery"
                            ></v-checkbox>

                            <v-textarea
                                v-model="item.description"
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
                        <v-btn color="blue darken-1" text @click="createItemDialog = false">Close</v-btn>
                        <v-btn color="Green darken-1" text @click="createItem()">Create</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
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
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
        return {
            createItemDialog:false,
            create_item_form_valid:true,
            itemDialog:false,
            d_item:null,
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
                    'value':'schoolsupplies',
                    'text':'School supplies'
                },
                {   
                    'value':'pets',
                    'text':'Pets'
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
                    'value':'miscellaneous',
                    'text':'Miscellaneous'
                },
            ],
            item:{
                name:"",
                price:0,
                condition:'new',
                category:'miscellaneous',
                pickup:false,
                delivery:false,
                description:"",
                image:null,
            },
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 25) || 'Name must be less than 25 characters',
            ],
            descriptionRules: [
                v => !!v || 'Desctiption is required',
                v => (v && v.length <= 350) || 'Desctiption must be less than 350 characters',
            ],
            items:[],
        }
	},
	components:{
        MarketHeader,
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
            });
        },
        openCreateItemDialog(){
            this.createItemDialog = true;
        },
        createItem(){
            this.$refs.form.validate();
            if(!this.create_item_form_valid)
                return;
            let formData = new FormData();
            formData.append('image',this.item.image);
            for(var key in this.item){
                formData.append(key, this.item[key]);
            }
            axios.post('/market/api/create_item/',formData,
            {
                headers:{
                    'Content-Type': 'multipart/form-data',
                }
            }).then(response => {
                if(response.data.success){
                    this.$message({
                        message: 'Item Posted',
                        type: 'success'
                    });
                    this.getMyItems();
                    this.createItemDialog = false;
                    this.item = {
                        name:"",
                        price:0,
                        condition:'new',
                        category:'miscellaneous',
                        pickup:false,
                        delivery:false,
                        description:"",
                        image:null,
                    };
                    this.$refs.form.resetValidation();
                }
            });
        },
	},
	mounted(){
        this.getMyItems();
	},
  };
</script>

<style>
    .v-card__title{
        font-family: "Roboto", sans-serif !important;
        font-weight: 700 !important;
    }

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
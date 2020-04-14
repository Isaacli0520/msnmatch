<template>
    <v-dialog v-model="itemDialog" v-if='d_item' min-width="350px">
        <v-card>
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
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-simple-table>
                            <template v-slot:default>
                            <tbody>
                                <tr>
                                    <td>Price</td>
                                    <td>${{ d_item.price }}</td>
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
                        <v-btn color="red darken-1" v-if="edit" outlined @click="openDeleteDialog">Delete</v-btn>
                        <v-btn color="yellow darken-1" v-if="edit" outlined @click="openSoldDialog">Sold</v-btn>
                        <v-btn color="green darken-1" v-if="edit" outlined @click="openEditDialog">Edit</v-btn>
                        <v-btn color="blue darken-1" outlined @click="closeDialog">Close</v-btn>
                    </v-card-actions>
                </div>
                </v-flex>
            </v-layout>
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
        }
    },
    components:{
    },
    watch:{
    },
    computed:{
        
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

</style>
<template>
	<v-app>
		<comments-header></comments-header>
		<v-content>
			<v-container fluid grid-list-lg>
                <v-layout>
                    <v-flex>
                        <span class="title-text">Your Slides</span>
                    </v-flex>
                </v-layout>
                <v-layout row wrap>
                    <v-flex xs12 sm12 md6 lg4 xl4 :key="slide_idx" v-for="(slide, slide_idx) in slides">
                        <v-card>
                            <v-card-title>{{slide.name}}</v-card-title>
                            <v-card-title>{{slide.user.first_name}} {{slide.user.last_name}}</v-card-title>
                            <v-card-text><v-chip color="green darken-1" outlined v-if="slide.active" disabled>Active</v-chip></v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="Red" outlined @click="setSlide(slide.pk)">
                                    Set As Active Slide
                                </v-btn>
                                <v-btn color="blue" outlined @click="goToHref('/comments/'+slide.pk)">
                                    View Slide
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-flex>
                    <v-flex>
                        <v-btn outlined @click="createSlideDialog = true">
                            Create
                        </v-btn>
                    </v-flex>
                </v-layout>
			</v-container>
                <v-dialog v-model="createSlideDialog" scrollable min-width="350px" max-width="600px">
                <v-card>
                    <v-card-title>Create a Slide</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="height: 300px;">
                        <v-layout class="mt-3">
                            <v-flex>
                                <v-textarea
                                    v-model="slide_name"
                                    label="Slide Name"
                                    outlined
                                    :error-messages="slide_name_error_messages"
                                    rows="1"
                                    row-height="20"
                                ></v-textarea>
                                <v-textarea
                                    v-model="slide_url"
                                    label="Slide URL"
                                    outlined
                                    :error-messages="slide_url_error_messages"
                                    rows="1"
                                    row-height="20"
                                ></v-textarea>
                            </v-flex>
                        </v-layout>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="createSlideDialog = false">Close</v-btn>
                        <v-btn color="Green darken-1" text @click="createSlide()">Create</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
		</v-content>
	</v-app>
</template>

<script>
import axios from 'axios'
import CommentsHeader from '../components/CommentsHeader'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

  export default {
	data() {
		return {
            slides:[],
            createSlideDialog:false,
            slide_name:"",
            slide_url:"",
            slide_name_error_messages:[],
            slide_url_error_messages:[],
		}
	},
	components:{
		CommentsHeader,
	},
	watch: {

	},
	computed:{

	},
	methods: {
        createSlide(){
            let error_flag = false;
            if(this.slide_name.length == 0){
                this.slide_name_error_messages.push("Enter a name pls T_T");
                error_flag = true;
            }
            if(this.slide_url.length == 0){
                this.slide_url_error_messages.push("Enter a url pls T_T");
                error_flag = true;
            }
            if(!error_flag){
                axios.post('/comments/api/create_slide/', {
                    "name":this.slide_name,
                    "url":this.slide_url,
                }).then(response => {
                    if(response.data.success){
                        this.$message({
                            message: 'Slide Created',
                            type: 'success'
                        });
                        this.getSlides();
                    }
                });
            }
        },
        setSlide(slide_pk){
            axios.post('/comments/api/set_slide/', {
                "slide_pk":slide_pk,
            }).then(response => {
                if(response.data.success){
                    this.$message({
                        message: 'Slide set as active',
                        type: 'success'
                    });
                    this.getSlides();
                }
            });
        },
        getSlides(){
            axios.get('/comments/api/get_slides/', {}).then(response => {
                this.slides = response.data.slides;
            });
        },
		goToHref(text){
			window.location.href = text;
        },
    },
    created(){
    },
	mounted(){
        this.getSlides();
	},
};
</script>

<style>
    .title-text{
        font-family: "Roboto", sans-serif;
        font-size: 1.6em;
        font-weight: 500;
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
<template>
    <v-app>
        <custom-header></custom-header>
        <v-content>
            <v-container fluid grid-list-lg>
                <v-layout>
                    <v-flex>
                        <v-breadcrumbs class="cus-breadcrumbs" :items="navItems" divider=">"></v-breadcrumbs>
                    </v-flex>
                </v-layout>
                <v-layout mb-3>
                    <v-flex> 
                        <div>
                            <span class="cus-headline-text">My Reviews</span>
                        </div>
                    </v-flex>
                    <v-spacer></v-spacer>
                </v-layout>
                <v-layout wrap>
                    <v-flex d-flex child-flex xs12 sm12 md12 lg12 xl12>
                        <v-layout row wrap v-if="reviews.length > 0">
                            <v-flex 
                                child-flex d-flex
                                xs12 sm12 md6 lg6 xl6
                                :key="index_review + '-review' " 
                                v-for="(review, index_review) in reviews">
                                <v-card>
                                    <v-card-title>
                                        {{review.course.mnemonic}}{{review.course.number}} {{review.course.title}}
                                    </v-card-title>
                                    <v-divider></v-divider>
                                    <v-card-text>
                                        <div class="review-text">
                                            {{review.text}}
                                        </div>
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-layout>
                                            <v-spacer></v-spacer>
                                        <div>
                                            <v-chip
                                                class="ma-1" color="teal lighten-2" label small text-color="white">
                                                {{review.semester}}
                                            </v-chip>
                                            <v-chip
                                                class="ma-1" color="teal lighten-2" label small text-color="white">
                                                Course: {{ review.rating_course ? review.rating_course : 'N/A' }}
                                            </v-chip>
                                            <v-chip
                                                class="ma-1" color="teal lighten-2" label small text-color="white">
                                                Instructor: {{review.rating_instructor ? review.rating_instructor : 'N/A'}}
                                            </v-chip>
                                        </div>
                                        </v-layout>
                                    </v-card-actions>
                                </v-card>
                            </v-flex>
                        </v-layout>
                        <span v-else>You have no reviews.</span>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-content>
    </v-app>
</template>

<script>
import axios from 'axios'
import CustomHeader from '../components/CustomHeader'

  export default {
	data() {
	    return {
            navItems:[],
            reviews:[],
	    }
	},
	components:{
	  CustomHeader,
	},
	watch: {

	},
	computed:{
	  
	},
	methods: {
		goToHref(text){
			window.location.href = text;
        },
        getReviews(){
            axios.get('/courses/ajax/get_reviews/',{params: {}}).then(response => {
                this.reviews = response.data.reviews;
            });
        },
	},
	mounted(){
        this.navItems = [
            {
                text: "Main",
                disabled: false,
                href: '/courses/',
            },
            {
                text: "My Reviews",
                disabled: true,
                href: '',
            },
        ];
        this.getReviews();
	},
  };
</script>

<style>

    .v-breadcrumbs li{
        font-size:20px !important;
    }

    .cus-breadcrumbs{
        padding-left: 4px !important;
    }

	.cus-headline-text{
		font-family: "Roboto", sans-serif;
		font-size: 2.1em;
		font-weight: 300;
		color:rgb(0, 0, 0);
		padding: 7px 12px 7px 3px;
		border-radius: 5px;
		line-height: 2.0;
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
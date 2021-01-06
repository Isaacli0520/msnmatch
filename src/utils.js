// static urls
export var brand_pic = "/static/css/images/brand_compressed.png";

// general urls
export var general_urls = {
    home_url:"/",
    courses_url: "/courses/",
    match_url: "/match/",
    comment_url: "/comments/send/",
    market_url: "/market/",
    skills_url: "/skills/",
    roommate_url: "/roommate/",
    review_url:"/courses/reviews/",
    my_courses_url:"/courses/me",
    department_url:"/courses/departments/",
    logout_url:"/logout/"
};

// general icons
export var general_icons = {
    // misc
    my_courses:"mdi-format-list-text",
    my_reviews:"mdi-book-open-page-variant-outline",
    submit_review:"mdi-pencil-plus-outline",
    departments:"mdi-format-list-numbered",
    add_tags:"mdi-heart-outline",
    // user
    profile:"mdi-account-details-outline",
    edit_profile:"mdi-clipboard-edit-outline",
    logout:"mdi-logout",
    // main
    home:"mdi-home-outline",
    courses:"mdi-message-text-outline",
    match:"mdi-account-multiple",
    market:"mdi-shopping-outline",
    live_comments:"mdi-chat-processing-outline",
    plannable:"mdi-navigation-outline",
    recommendation:"mdi-thumb-up-outline",
};

export function sortBySemester(a, b){
    if(a.substring(0,4) != b.substring(0,4)){
        return b.substring(0,4).toString(10) - a.substring(0,4).toString(10);
    }
    else{
        if(a.substring(4) == b.substring(4)){
            return 0;
        }
        else if(a.substring(4) == "Fall"){
            return -1;
        }
        else{
            return 1;
        }
    }
}
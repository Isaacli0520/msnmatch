<template>
    <footer>
        <section id="footer">
            <div class="container">
            <div class="row text-center text-xs-center text-sm-left text-md-left">
                <div class="col-xs-12 col-sm-6 col-md-4">
                    <h5 style="font-weight: 400;">Quick links</h5>
                    <ul class="list-unstyled quick-links">
                    <li><a href="{% url 'home' %}"><i class="fa fa-angle-double-right"></i>Home</a></li>
                    <li><a href="{% url 'skill_search' %}"><i class="fa fa-angle-double-right"></i>Tags</a></li>
                    <li><a href="{% url 'profile' request.user.username %}"><i class="fa fa-angle-double-right"></i>Profile</a></li>
                    </ul>
                </div>
                <div class="col-xs-12 col-sm-6 col-md-6">
                <h5 style="font-weight: 400;">Get In Touch</h5>
                <ul class="list-unstyled quick-links">
                    <li><span><i class="fa fa-angle-double-right"></i>Mentor Program Chair WeChat ID: zgt19991026</span></li>
                    <li><span><i class="fa fa-angle-double-right"></i>Email: <a href="mailto:msnatuva@gmail.com">msnatuva@gmail.com</a></span></li>
                </ul>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-12 col-sm-12 col-md-12 mt-2 mt-sm-2 text-center text-white">
                <p class="h6">&copy <a class="text-green ml-2" href="https://www.msnatuva.org" target="_blank">2019 Mainland Student Network.</a> All Rights Reserved.</p>
                </div>
                </hr>
            </div>	
            </div>
        </section>
    </footer>
</template>

<script>

export default {
    data: function(){
        return {
        }
    },
}
</script>

<style scoped lang="css">
section {
    padding: 60px 0;
}

section .section-title {
    text-align: center;
    color: #0f9273;
    margin-bottom: 50px;
    text-transform: uppercase;
}
#footer {
    background: rgb(50, 164, 154) !important;
    position: relative;
    clear: both;
    bottom: 0;
    width: 100%;
    margin-top:auto;
}
#footer h5{
	padding-left: 10px;
    border-left: 3px solid #eeeeee;
    padding-bottom: 6px;
    margin-bottom: 20px;
    color:#ffffff;
}
#footer a {
    color: #ffffff;
    text-decoration: none !important;
    background-color: transparent;
    -webkit-text-decoration-skip: objects;
}
#footer ul.social li{
	padding: 3px 0;
}
#footer ul.social li a i {
    margin-right: 5px;
	font-size:25px;
	-webkit-transition: .5s all ease;
	-moz-transition: .5s all ease;
	transition: .5s all ease;
}
#footer ul.social li:hover a i {
	font-size:30px;
	margin-top:-10px;
}
#footer ul.social li a,
#footer ul.quick-links li a{
	color:#ffffff;
}
#footer ul.social li a:hover{
	color:#eeeeee;
}
#footer ul.quick-links li{
    color:#ffffff;
	padding: 3px 0;
	-webkit-transition: .5s all ease;
    -moz-transition: .5s all ease;
	transition: .5s all ease;
}
#footer ul.quick-links li:hover{
	padding: 3px 0;
	margin-left:5px;
	/* font-weight:700; */
}
#footer ul.quick-links li a i{
	margin-right: 5px;
}

#footer ul.quick-links li span i{
    color:#ffffff;
	margin-right: 5px;
}
</style>
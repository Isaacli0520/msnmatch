<template>
    <el-container>
        <el-header>
        </el-header>
    <el-container>
        <el-aside>
            aside
        </el-aside>
        <el-main>
            <el-button @click="goToHref('/match/')">Match</el-button>
            <el-button @click="goToHref('/courses/')">Courses</el-button>
        </el-main>
    </el-container>
        <el-footer>
        </el-footer>
    </el-container>
</template>

<script>
import axios from 'axios'

  export default {
    data() {
      return {
          isCollapse:true,
          recognition: '',
          activeIndex: '1',
          navOptions:[
              {
                  href:"/match/",
                  label:"Match",
              },
              {
                  href:"",
                  label:"Hoosmyprofessor",
              },
              {
                  href:"www.msnatuva.org",
                  label:"MSN",
              },
          ]
      }
    },
    components:{
    },
    computed:{
    },
    methods: {
        goToHref(href){
            console.log("lalala");
            window.location.href = href;
        },
        goToLessons(){
            window.location.href = "/lessons/";
        },
    },
    mounted(){
    },
  };
</script>

<style>


    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: center;
        line-height: 200px;
    }

    .container{
        width: 100%;
        padding: 0;
        margin: 0;
        height: 100%;
        box-sizing: border-box;
        border-bottom: 1px solid #dcdfe6;
    }

    .el-header{
    background-color: rgb(238, 236, 236);
    color: rgb(0, 0, 0);
    text-align: center;
    line-height: 60px;
  }
  .el-footer {
    background-color: rgb(184, 165, 165);
    color: rgb(255, 255, 255);
    text-align: center;
    line-height: 60px;
  }
  
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0 auto;
  }
  
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
  

</style>
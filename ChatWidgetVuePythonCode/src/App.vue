<template>
  <body>
    <img style="width: 100vw; height: 100vh;" :src="selectedImage" alt="">
  <div id="app">
    
    <ChatWidget/>
  </div>
  </body>
</template>

<script>
import ChatWidget from './components/ChatWidget.vue'
import RecruiterImage from "./assets/screen2.png"
import ApplicantImage from "./assets/ss21.jpg"
export default {
  name: 'app',
  components: {
    ChatWidget
  },
  data(){
    return{
      selectedImage:""
    }
  },
  methods:{
    getBgImage(){
      if(window.location.pathname.split('/')[1]=="recruiter"){
        return RecruiterImage
      }else{
        return ApplicantImage
      }      
    }
  },
  created(){
    this.selectedImage = this.getBgImage();
  }
}
</script>

<style>
</style>
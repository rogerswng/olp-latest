<template lang="html">
  <div class="section-main">
    <Header style="position: fixed; z-index: 100;" v-if="entity.type==='doc'"/>
    <Header v-else />
    <div class="content-wrap">
      <div class="section-content">
        <div class="videoplayer-wrap" v-if="entity.type === 'video'">
          <VideoPlayer :videoid="entity.id" :videourl="entity.url" :relatedcourse="relatedCourse" />
        </div>
        <div class="doc-wrap" v-if="entity.type === 'doc'">
          <DocReader :docid="entity.id" :content="entity.content" :courseid="relatedCourse" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header';
import VideoPlayer from '../components/videoplayer';
import DocReader from '../components/docreader';
import axios from 'axios';

export default {
  name: 'Section',
  data () {
    return {
      id: '',
      relatedCourse: '',
      relatedTopic: '',
      entity: {
        id: '',
        type: '',
        url: '',
        content: ''
        // type: 'doc',
        // duration: 1128
      },
      status: 0
    }
  },
  created () {
    console.log(this.$route.params.id);
  },
  mounted () {
    axios.get("http://"+this.BASEURL+"/sectionDetail?sectionId="+this.$route.params.id+"&uid="+this.$getCookie("uid")).then(function(res) {
      console.log(res);
      this.id = this.$route.params.id;
      this.relatedCourse = res.data.relatedCourse;
      this.relatedTopic = res.data.relatedTopic;
      this.entity.id = res.data.entity.id;
      if (res.data.entity.type === 0) {
        this.entity.type = 'video';
        this.entity.url = res.data.entity.url;
      } else if (res.data.entity.type === 1) {
        this.entity.type = 'doc';
        this.entity.url = res.data.entity.url;
        this.entity.content = res.data.entity.content;
      }
      this.status = res.data.status;
    }.bind(this));
  },
  beforeDestroy () {
    var d = {
      sectionId: this.id,
      courseId: this.relatedCourse,
      uid: this.$getCookie("uid")
    }
    axios.post("http://"+this.BASEURL+"/updateSectionProcess",d).then(function(res) {
      alert(res);
    })
  },
  components: {
    'Header': Header,
    'VideoPlayer': VideoPlayer,
    'DocReader': DocReader
  },
  watch: {
    $route: function() {
      window.location.reload();
    }
  }
}
</script>

<style scoped lang="css">
.section-main {
  height: 100%;
  background-color: #f8f8f9;
}
.content-wrap {
  /* height: 100%; */
  background-color: #f8f8f9;
}
.section-content {
  width: 1175px;
  margin: 0 auto;
  padding: 10px 0;
  background-color: #f8f8f9;
  /* margin-top:  */
}
.videoplayer-wrap {
  width: 1175px;
}
.doc-wrap {
  width: 1175px;
  background-color: #f8f8f9;
}
</style>

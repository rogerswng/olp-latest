<template lang="html">
  <div class="section-main">
    <Header />
    <div class="content-wrap">
      <div class="section-content">
        <div class="videoplayer-wrap">
          <VideoPlayer />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/header';
import VideoPlayer from '../components/videoplayer';

export default {
  name: 'Section',
  data () {
    return {

    }
  },
  created () {
    console.log(this.$route.params.id);
  },
  components: {
    'Header': Header,
    'VideoPlayer': VideoPlayer
  }
}
</script>

<style lang="css">
.section-main {
  height: 100%;
  background-color: #f8f8f9;
}
.content-wrap {
  height: 100%;
  background-color: #f8f8f9;
}
.section-content {
  width: 1175px;
  margin: 0 auto;
  padding: 10px 0;
}
.videoplayer-wrap {
  width: 1175px;
}
</style>

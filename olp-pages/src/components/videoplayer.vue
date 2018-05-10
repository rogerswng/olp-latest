<template lang="html">
  <div class="videoplayer-main">
    <div class="video-player">
      <video id="videoElement" width="1024" height="576" controls>
      </video>
    </div>
  </div>
</template>

<script>
import flvjs from 'flv.js';

export default {
  name: 'VideoPlayer',
  data () {
    return {

    }
  },
  mounted () {
    var player = document.getElementById('videoElement');
    console.log("videoelement: "+player);
    if (flvjs.isSupported()) {
      console.log("here!");
      var flvPlayer = flvjs.createPlayer({
        type: 'mp4',
        url: '/static/test400k.mp4'
      });
      flvPlayer.attachMediaElement(player);
      flvPlayer.load();
    }
  }
}
</script>

<style lang="css">

</style>

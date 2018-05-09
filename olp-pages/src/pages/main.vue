<template lang="html">
  <div class="main">
    <Header />
  </div>
</template>

<script>
import Header from '../components/header';

export default {
  name: 'Main',
  data () {
    return {

    }
  },
  components: {
    'Header': Header
  }
}
</script>

<style lang="css">
.main {
  background-color: #f8f8f9;
  height: 100%;
}
</style>

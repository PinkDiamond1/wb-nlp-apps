<template>
  <div>
    <!-- <h1>{{ page_title }}</h1> -->
    <br />
    <b-container fluid>
      <!-- <iframe
        src="https://agoldst.github.io/dfr-browser/demo/"
        frameborder="0"
        height="800px"
        width="100%"
      ></iframe> -->

      <iframe
        src="/dfr/#/model/list"
        frameborder="0"
        height="800px"
        width="100%"
      ></iframe>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "TopicBrowser",
  props: {
    page_title: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

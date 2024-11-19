<template>
    <div>
        Article: {{ articleId }}
    </div>
</template>
  
  <script>
  import { useRoute } from 'vue-router';
  import { onMounted, ref, getCurrentInstance } from 'vue';

  export default {
    setup() {
      const route = useRoute();
      const articleId = route.params.id;

      return {
        articleId,
      };
    },
  };
  </script>
  
  <style scoped>

  </style>
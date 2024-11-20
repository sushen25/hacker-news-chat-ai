<template>
    <div class="container text-center mt-4">
    <h1>Article: {{ articleId }}</h1>
    <div class="row justify-content-center">
      <div class="col-12 col-md-12">
        <div v-if="article.url">
            <iframe
            :src="article.url"
            class="embed-responsive embed-responsive-16by9 border rounded"
            style="width: 100%; height: 500px;"
            frameborder="0"
            allowfullscreen
            ></iframe>
        </div>
        <div>
            <h2>{{ article.title }}</h2>
            <p>{{ article.summary }}</p>
            <p>{{ article.content }}</p>
        </div>
        
      </div>
    </div>
  </div>
</template>
  
  <script>
  import { useRoute } from 'vue-router';
  import { onMounted, ref, getCurrentInstance } from 'vue';

  export default {
    setup() {
        const { proxy } = getCurrentInstance();
        const route = useRoute();
        const articleId = route.params.id;
        const article = ref("");

        const fetchArticle = async () => {
            console.log("Fetching article with id:", articleId);
            proxy.$axios
            .get(`/get_post/${articleId}`)
            .then((response) => {
                console.log("Article:", response.data);
                article.value = response.data;
            }).catch((err) => {
                console.error("Error:", err);
            });
        };

        onMounted(() => {
            fetchArticle();
        });

        return {
            articleId,
            article
        };
    },
  };
  </script>
  
  <style scoped>

  </style>